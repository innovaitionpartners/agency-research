#!/usr/bin/env python3
"""Validate a Research With Receipts candidate-source ledger.

This gate enforces mechanical source-admission rules. It cannot determine
whether the recorded evidence is true or actually supports the claim.
"""

from __future__ import annotations

import argparse
import calendar
import ipaddress
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


DEFAULT_HTTP_PORT = 80  # IANA default port for HTTP.
DEFAULT_HTTPS_PORT = 443  # IANA default port for HTTPS.
FIRST_CONTROL_CODE = 32  # Unicode code points below SPACE are control characters.
DELETE_CONTROL_CODE = 127  # DEL is also a control character.
MAX_HOSTNAME_LENGTH = 253  # Maximum DNS hostname length without a trailing dot.
MAX_HOST_LABEL_LENGTH = 63  # Maximum length of one DNS label.
MIN_DATE_YEAR = 1  # datetime.date lower bound.
MAX_DATE_YEAR = 9999  # datetime.date upper bound.
RESERVED_NONPUBLIC_SUFFIXES = (".test", ".example", ".invalid")
RESERVED_NONPUBLIC_HOSTS = {"test", "example", "invalid"}

SEARCH_HOSTS = {
    "www.google.com",
    "google.com",
    "www.bing.com",
    "bing.com",
    "search.yahoo.com",
    "duckduckgo.com",
}

SOURCE_TYPES = {
    "government",
    "regulator",
    "academic",
    "standards_body",
    "company_documentation",
    "company_statement",
    "press_release",
    "vendor_material",
    "trade_publication",
    "news",
    "nonprofit",
    "social_post",
    "other",
}

TOP_KEYS = {"version", "scope", "claims", "sources"}
SCOPE_KEYS = {"date_start", "date_end", "geography", "excluded_source_types"}
OPTIONAL_SCOPE_KEYS = {"research_shape", "breadth_exception"}
CLAIM_KEYS = {"id", "text", "kind", "status", "source_ids", "qualification"}
SOURCE_KEYS = {
    "id",
    "title",
    "publisher",
    "publication_date",
    "url",
    "source_type",
    "opened",
    "access",
    "evidence",
    "scope_match",
    "scope_note",
    "limitations",
    "superseded",
    "date_exception",
    "verdict",
    "verdict_reason",
}
OPTIONAL_SOURCE_KEYS = {"evidence_lineage"}

CLAIM_KINDS = {"fact", "inference", "estimate", "anecdote", "uncertain"}
CLAIM_STATUSES = {"supported", "gap"}
ACCESS_VALUES = {"full", "partial", "inaccessible"}
SCOPE_MATCH_VALUES = {"match", "partial", "mismatch", "not_applicable"}
VERDICTS = {"use", "context_only", "reject"}
RESEARCH_SHAPES = {
    "narrow_question",
    "comparison",
    "broad_landscape",
    "how_to",
    "multi_question",
    "other",
}
MONTH_NUMBERS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sept": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}


def canonical_url(value: str) -> str:
    parsed = urlparse(value)
    scheme = parsed.scheme.lower()
    hostname = (parsed.hostname or "").rstrip(".").lower()
    try:
        ipaddress.ip_address(hostname)
        canonical_host = f"[{hostname}]" if ":" in hostname else hostname
    except ValueError:
        canonical_host = hostname.encode("idna").decode("ascii")
    port = parsed.port
    default_port = (scheme == "http" and port == DEFAULT_HTTP_PORT) or (
        scheme == "https" and port == DEFAULT_HTTPS_PORT
    )
    canonical_netloc = canonical_host
    if port is not None and not default_port:
        canonical_netloc = f"{canonical_host}:{port}"
    kept_query = [
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
        and key.lower() not in {"fbclid", "gclid"}
    ]
    return urlunparse(
        (
            scheme,
            canonical_netloc,
            parsed.path.rstrip("/") or "/",
            "",
            urlencode(sorted(kept_query)),
            "",
        )
    )


def direct_url_error(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return "requires a direct HTTP(S) URL"
    if any(
        character.isspace()
        or ord(character) < FIRST_CONTROL_CODE
        or ord(character) == DELETE_CONTROL_CODE
        for character in value
    ):
        return "URL cannot contain whitespace or control characters"
    try:
        parsed = urlparse(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError as exc:
        if "port" in str(exc).lower():
            return "URL has an invalid port"
        return "requires a valid direct HTTP(S) URL"
    if parsed.scheme.lower() not in {"http", "https"} or not hostname:
        return "requires a direct HTTP(S) URL"
    if parsed.username is not None or parsed.password is not None:
        return "URL cannot contain embedded credentials"
    candidate_host = hostname[:-1] if hostname.endswith(".") else hostname
    if (
        candidate_host == "localhost"
        or candidate_host.endswith(".localhost")
        or candidate_host.endswith(".local")
    ):
        return "URL hostname is not public"
    try:
        ip_address = ipaddress.ip_address(candidate_host)
        if not ip_address.is_global:
            return "URL hostname is not public"
        return None
    except ValueError:
        pass
    if re.fullmatch(r"[0-9.]+", candidate_host):
        return "URL has an invalid hostname"
    try:
        ascii_host = candidate_host.encode("idna").decode("ascii")
    except UnicodeError:
        return "URL has an invalid hostname"
    labels = ascii_host.split(".")
    if (
        not ascii_host
        or len(ascii_host) > MAX_HOSTNAME_LENGTH
        or any(
            not label
            or len(label) > MAX_HOST_LABEL_LENGTH
            or label.startswith("-")
            or label.endswith("-")
            or re.fullmatch(r"[A-Za-z0-9-]+", label) is None
            for label in labels
        )
    ):
        return "URL has an invalid hostname"
    if candidate_host in RESERVED_NONPUBLIC_HOSTS or candidate_host.endswith(
        RESERVED_NONPUBLIC_SUFFIXES
    ):
        return "URL hostname is reserved for non-public use"
    return None


def is_search_result_url(value: str) -> bool:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    if host in SEARCH_HOSTS or host.startswith("search.yahoo."):
        return True
    if host.startswith("scholar.google.") and path.startswith("/scholar"):
        return True
    if host.startswith("news.google.") and path.startswith("/search"):
        return True
    search_hosts = (
        host.startswith("google."),
        host.startswith("www.google."),
        host == "search.brave.com",
        host.endswith(".ecosia.org"),
        host.endswith(".startpage.com"),
        host.startswith("yandex."),
        host.startswith("www.yandex."),
    )
    return path.startswith("/search") and any(search_hosts)


def check_keys(
    value: Any,
    expected: set[str],
    label: str,
    errors: list[str],
    optional: set[str] | None = None,
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return False
    optional = optional or set()
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected - optional)
    if missing:
        errors.append(f"{label} is missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{label} has unexpected keys: {', '.join(extra)}")
    return not missing and not extra


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def single_line_control_free(value: Any) -> bool:
    return isinstance(value, str) and not any(
        character in {"\r", "\n"}
        or ord(character) < FIRST_CONTROL_CODE
        or ord(character) == DELETE_CONTROL_CODE
        for character in value
    )


def parse_ledger_date(value: Any, label: str, errors: list[str]) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        errors.append(f"{label} must be YYYY-MM-DD or null")
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        errors.append(f"{label} must be a valid YYYY-MM-DD date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} must be a valid YYYY-MM-DD date")
        return None


def parse_publication_interval(
    value: Any, label: str, errors: list[str]
) -> tuple[date | None, date | None]:
    """Return the earliest and latest date implied by displayed date precision."""
    if value == "date not shown":
        return None, None
    if not isinstance(value, str):
        errors.append(
            f"{label} must be YYYY-MM-DD, Month YYYY, YYYY-MM, YYYY, or 'date not shown'"
        )
        return None, None

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        parsed = parse_ledger_date(value, label, errors)
        return parsed, parsed

    numeric_month = re.fullmatch(r"(\d{4})-(\d{2})", value)
    named_month = re.fullmatch(r"([A-Za-z]+)\.? (\d{4})", value)
    year_only = re.fullmatch(r"(\d{4})", value)

    year: int
    month: int
    if numeric_month:
        year = int(numeric_month.group(1))
        month = int(numeric_month.group(2))
    elif named_month:
        year = int(named_month.group(2))
        month = MONTH_NUMBERS.get(named_month.group(1).lower(), 0)
    elif year_only:
        year = int(year_only.group(1))
        if year not in range(MIN_DATE_YEAR, MAX_DATE_YEAR + 1):
            errors.append(f"{label} contains an invalid year")
            return None, None
        return date(year, 1, 1), date(year, 12, 31)
    else:
        errors.append(
            f"{label} must be YYYY-MM-DD, Month YYYY, YYYY-MM, YYYY, or 'date not shown'"
        )
        return None, None

    if year not in range(MIN_DATE_YEAR, MAX_DATE_YEAR + 1):
        errors.append(f"{label} contains an invalid year")
        return None, None
    if month not in range(1, 13):
        errors.append(f"{label} contains an invalid month")
        return None, None
    return date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])


def load_and_validate(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"cannot read valid JSON from {path}: {exc}"]

    if not check_keys(data, TOP_KEYS, "ledger", errors):
        return data if isinstance(data, dict) else None, errors
    if type(data.get("version")) is not int or data.get("version") != 1:
        errors.append("ledger version must be the integer 1")

    scope = data["scope"]
    scope_ready = check_keys(
        scope, SCOPE_KEYS, "scope", errors, optional=OPTIONAL_SCOPE_KEYS
    )
    date_start: date | None = None
    date_end: date | None = None
    excluded_types: set[str] = set()
    if scope_ready:
        date_start = parse_ledger_date(scope["date_start"], "scope.date_start", errors)
        date_end = parse_ledger_date(scope["date_end"], "scope.date_end", errors)
        if date_start and date_end and date_start > date_end:
            errors.append("scope.date_start cannot be after scope.date_end")
        if not nonempty_string(scope["geography"]):
            errors.append("scope.geography must be a non-empty string")
        research_shape = scope.get("research_shape")
        if research_shape is not None and research_shape not in RESEARCH_SHAPES:
            errors.append(
                "scope.research_shape must be one of: "
                + ", ".join(sorted(RESEARCH_SHAPES))
            )
        breadth_exception = scope.get("breadth_exception")
        if breadth_exception is not None and not isinstance(breadth_exception, str):
            errors.append("scope.breadth_exception must be a string")
        excluded = scope["excluded_source_types"]
        if not isinstance(excluded, list) or not all(isinstance(item, str) for item in excluded):
            errors.append("scope.excluded_source_types must be a list of source_type strings")
        else:
            excluded_types = set(excluded)
            if len(excluded_types) != len(excluded):
                errors.append("scope.excluded_source_types cannot contain duplicates")
            unknown = sorted(excluded_types - SOURCE_TYPES)
            if unknown:
                errors.append(f"scope.excluded_source_types contains unknown values: {', '.join(unknown)}")

    claims = data["claims"]
    sources = data["sources"]
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []

    source_by_id: dict[str, dict[str, Any]] = {}
    canonical_to_id: dict[str, str] = {}
    for index, source in enumerate(sources):
        label = f"source[{index}]"
        if not check_keys(
            source, SOURCE_KEYS, label, errors, optional=OPTIONAL_SOURCE_KEYS
        ):
            continue
        source_id = source["id"]
        if not nonempty_string(source_id):
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if source_id in source_by_id:
            errors.append(f"source id {source_id!r} is duplicated")
            continue
        source_by_id[source_id] = source

        for field in ("title", "publisher", "publication_date", "url", "source_type", "access", "scope_match", "verdict", "verdict_reason"):
            if not nonempty_string(source[field]):
                errors.append(f"source {source_id} field {field!r} must be a non-empty string")
        for field in ("title", "publisher"):
            if nonempty_string(source[field]) and not single_line_control_free(source[field]):
                errors.append(
                    f"source {source_id} field {field!r} must be single-line and control-free"
                )
        for field in ("evidence", "scope_note", "limitations", "date_exception"):
            if not isinstance(source[field], str):
                errors.append(f"source {source_id} field {field!r} must be a string")
        if "evidence_lineage" in source and not isinstance(
            source["evidence_lineage"], str
        ):
            errors.append(f"source {source_id} field 'evidence_lineage' must be a string")

        source_type = source["source_type"] if isinstance(source["source_type"], str) else ""
        access = source["access"] if isinstance(source["access"], str) else ""
        scope_match = source["scope_match"] if isinstance(source["scope_match"], str) else ""
        verdict = source["verdict"] if isinstance(source["verdict"], str) else ""
        if source_type and source_type not in SOURCE_TYPES:
            errors.append(f"source {source_id} has unknown source_type {source_type!r}")
        if access and access not in ACCESS_VALUES:
            errors.append(f"source {source_id} has unknown access {access!r}")
        if scope_match and scope_match not in SCOPE_MATCH_VALUES:
            errors.append(f"source {source_id} has unknown scope_match {scope_match!r}")
        if verdict and verdict not in VERDICTS:
            errors.append(f"source {source_id} has unknown verdict {verdict!r}")
        if not isinstance(source["opened"], bool):
            errors.append(f"source {source_id} field 'opened' must be boolean")
        if not isinstance(source["superseded"], bool):
            errors.append(f"source {source_id} field 'superseded' must be boolean")

        url = source["url"]
        url_text = url if isinstance(url, str) else ""
        url_problem = direct_url_error(url)
        parsed = None
        if url_problem:
            errors.append(f"source {source_id} {url_problem}")
        else:
            parsed = urlparse(url_text)
            canonical = canonical_url(url_text)
            previous = canonical_to_id.get(canonical)
            if previous:
                errors.append(f"sources {previous} and {source_id} have the same direct URL")
            else:
                canonical_to_id[canonical] = source_id

        publication_start, publication_end = parse_publication_interval(
            source["publication_date"], f"source {source_id} publication_date", errors
        )

        if verdict != "use":
            continue
        if parsed is not None and is_search_result_url(url_text):
            errors.append(f"use source {source_id} cannot use a search-result URL")
        if parsed is not None and parsed.path in {"", "/"}:
            errors.append(f"use source {source_id} cannot use a homepage URL")
        if source_type in excluded_types:
            errors.append(
                f"use source {source_id} has excluded source_type {source_type!r}"
            )
        if source["opened"] is not True:
            errors.append(f"use source {source_id} must be opened")
        if access not in {"full", "partial"}:
            errors.append(f"use source {source_id} must have access 'full' or 'partial'")
        if not nonempty_string(source["evidence"]):
            errors.append(f"use source {source_id} requires specific evidence from the opened page")
        if not nonempty_string(source["scope_note"]):
            errors.append(f"use source {source_id} requires a scope_note")
        if not nonempty_string(source["limitations"]):
            errors.append(f"use source {source_id} requires limitations or 'none material'")
        if scope_match == "mismatch":
            errors.append(f"use source {source_id} cannot have scope_match 'mismatch'")
        if source["superseded"] is True:
            errors.append(f"use source {source_id} cannot be superseded")
        outside_start = bool(date_start and publication_end and publication_end < date_start)
        outside_end = bool(date_end and publication_start and publication_start > date_end)
        crosses_start = bool(
            date_start
            and publication_start
            and publication_end
            and publication_start < date_start <= publication_end
        )
        crosses_end = bool(
            date_end
            and publication_start
            and publication_end
            and publication_start <= date_end < publication_end
        )
        if (
            (date_start or date_end)
            and source["publication_date"] == "date not shown"
            and not nonempty_string(source["date_exception"])
        ):
            errors.append(
                f"use source {source_id} has no publication date inside a bounded date range without date_exception"
            )
        if (outside_start or outside_end) and not nonempty_string(source["date_exception"]):
            errors.append(
                f"use source {source_id} falls outside the confirmed date range without date_exception"
            )
        if (crosses_start or crosses_end) and not nonempty_string(source["date_exception"]):
            errors.append(
                f"use source {source_id} has partial publication-date precision that crosses the confirmed date boundary without date_exception"
            )

    claim_ids: set[str] = set()
    referenced_use_ids: set[str] = set()
    for index, claim in enumerate(claims):
        label = f"claim[{index}]"
        if not check_keys(claim, CLAIM_KEYS, label, errors):
            continue
        claim_id = claim["id"]
        if not nonempty_string(claim_id):
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if claim_id in claim_ids:
            errors.append(f"claim id {claim_id!r} is duplicated")
            continue
        claim_ids.add(claim_id)

        if not nonempty_string(claim["text"]):
            errors.append(f"claim {claim_id} text must be a non-empty string")
        claim_kind = claim["kind"] if isinstance(claim["kind"], str) else ""
        claim_status = claim["status"] if isinstance(claim["status"], str) else ""
        if not claim_kind:
            errors.append(f"claim {claim_id} kind must be a non-empty string")
        elif claim_kind not in CLAIM_KINDS:
            errors.append(f"claim {claim_id} has unknown kind {claim_kind!r}")
        if not claim_status:
            errors.append(f"claim {claim_id} status must be a non-empty string")
        elif claim_status not in CLAIM_STATUSES:
            errors.append(f"claim {claim_id} has unknown status {claim_status!r}")
        if not isinstance(claim["qualification"], str):
            errors.append(f"claim {claim_id} qualification must be a string")

        source_ids = claim["source_ids"]
        if not isinstance(source_ids, list) or not all(isinstance(item, str) for item in source_ids):
            errors.append(f"claim {claim_id} source_ids must be a list of source ids")
            continue
        if len(set(source_ids)) != len(source_ids):
            errors.append(f"claim {claim_id} source_ids cannot contain duplicates")

        if claim_status == "gap":
            if source_ids:
                errors.append(f"gap claim {claim_id} cannot reference sources")
            if not nonempty_string(claim["qualification"]):
                errors.append(f"gap claim {claim_id} requires a qualification explaining the evidence gap")
            continue
        if not source_ids:
            errors.append(f"supported claim {claim_id} must reference at least one use source")
            continue
        for source_id in source_ids:
            source = source_by_id.get(source_id)
            if source is None:
                errors.append(f"supported claim {claim_id} references unknown source {source_id}")
                continue
            if source["verdict"] != "use":
                errors.append(
                    f"supported claim {claim_id} can reference only use sources; {source_id} is {source['verdict']!r}"
                )
                continue
            referenced_use_ids.add(source_id)
            if source["scope_match"] == "partial" and not nonempty_string(claim["qualification"]):
                errors.append(
                    f"claim {claim_id} requires qualification when source {source_id} has partial scope match"
                )

    for source_id, source in source_by_id.items():
        if source["verdict"] == "use" and source_id not in referenced_use_ids:
            errors.append(f"use source {source_id} is not attached to any supported claim")

    return data, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()

    if not args.ledger.is_absolute():
        print(f"FAIL: ledger path must be absolute: {args.ledger}")
        return 2
    if not args.ledger.is_file():
        print(f"FAIL: file not found: {args.ledger}")
        return 2
    _, errors = load_and_validate(args.ledger)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(
            "The source gate checks recorded fields and mechanical contract violations; semantic support still requires researcher review."
        )
        return 1

    print("PASS: candidate-source ledger satisfies the deterministic admission gate.")
    print("A pass does not prove that recorded evidence is true or actually supports a claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
