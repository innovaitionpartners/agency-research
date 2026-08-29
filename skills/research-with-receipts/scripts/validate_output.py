#!/usr/bin/env python3
"""Validate deterministic Research With Receipts output surfaces.

This checks structure, the candidate-source ledger, and final citation
admission. It cannot determine whether recorded evidence is true or supportive.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from validate_sources import (
    canonical_url,
    direct_url_error,
    is_search_result_url,
    load_and_validate,
)


DEPTH_LINE = re.compile(
    r"^\*\*Depth:\*\* (Quick|Standard|Deep) · \*\*Checked:\*\* (\d{4}-\d{2}-\d{2})$",
    re.MULTILINE,
)
SOURCE_LABEL = re.compile(r"^.+ — .+, (?:date not shown|.*\b\d{4}\b.*)$")
FIELD_LINE = re.compile(r"^([A-Za-z ]+):\s*(.*)$")
ANY_HTTP_URL = re.compile(r"https?://\S+", re.IGNORECASE)
EPISTEMIC_LABELS = {
    "inference": "Inference",
    "estimate": "Estimate",
    "anecdote": "Anecdote",
    "uncertain": "Uncertain",
}
BROAD_MIN_SOURCES = 5
BROAD_MIN_SOURCE_TYPES = 3
BROAD_MIN_LINEAGES = 5

REQUIRED_HEADINGS = {
    "Quick": ["## Answer", "## Limits"],
    "Standard": ["## Bottom line", "## What the evidence shows", "## Limits and gaps"],
    "Deep": [
        "## Bottom line",
        "## Scope and method",
        "## What the evidence shows",
        "## Disagreements and gaps",
        "## Conclusions and recommendations",
        "## Why research stopped",
    ],
}

REQUIRED_RECORD_FIELDS = [
    "Depth",
    "Coverage plan",
    "Date range",
    "Geography or jurisdiction",
    "Source policy",
    "Search lanes",
    "Sources opened",
    "Access escalation",
    "Corroboration",
    "Disconfirming route",
    "Conflicts",
    "Evidence gaps",
    "Critical recheck",
    "Stop rationale",
]


class InputReadError(Exception):
    """Raised when a required UTF-8 artifact cannot be read."""


def read_utf8(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputReadError(f"cannot read UTF-8 {label} file {path}: {exc}") from exc


def ordered_headings(text: str, required: list[str]) -> list[str]:
    errors: list[str] = []
    positions = []
    for heading in required:
        hits = [m.start() for m in re.finditer(rf"(?m)^{re.escape(heading)}$", text)]
        if len(hits) != 1:
            errors.append(f"expected exactly one {heading!r}; found {len(hits)}")
        else:
            positions.append((heading, hits[0]))
    if len(positions) == len(required):
        actual = [heading for heading, _ in sorted(positions, key=lambda item: item[1])]
        if actual != required:
            errors.append("required headings are out of order")
    return errors


def substantive_section_errors(text: str, required: list[str]) -> list[str]:
    """Require visible prose or list content beneath every required H2 heading."""
    errors: list[str] = []
    all_h2 = list(re.finditer(r"(?m)^## [^#].*$", text))
    by_heading = {match.group(0): match for match in all_h2}
    for heading in required:
        match = by_heading.get(heading)
        if match is None:
            continue
        later = [candidate.start() for candidate in all_h2 if candidate.start() > match.start()]
        section_end = min(later) if later else len(text)
        body = text[match.end() : section_end]
        body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        substantive_lines = [
            line
            for line in body.splitlines()
            if line.strip()
            and not line.lstrip().startswith("#")
            and line.strip() not in {"---", "***"}
            and re.fullmatch(r"(?:`{3,}|~{3,}).*", line.strip()) is None
        ]
        if not substantive_lines:
            errors.append(f"required section {heading!r} must contain substantive content")
    return errors


def unescape_markdown_label(value: str) -> str:
    return re.sub(r"\\([\\\[\]\(\)])", r"\1", value)


def extract_inline_links(text: str) -> list[tuple[str, str, int, int, bool]]:
    """Extract inline Markdown links, including escaped labels and balanced URLs."""
    links: list[tuple[str, str, int, int, bool]] = []
    position = 0
    while True:
        link_start = text.find("[", position)
        if link_start == -1:
            return links
        if link_start > 0 and text[link_start - 1] == "!":
            position = link_start + 1
            continue

        cursor = link_start + 1
        label_end = -1
        while cursor < len(text) and text[cursor] != "\n":
            if text[cursor] == "\\" and cursor + 1 < len(text):
                cursor += 2
                continue
            if text[cursor] == "]":
                label_end = cursor
                break
            cursor += 1
        if label_end == -1 or label_end + 1 >= len(text) or text[label_end + 1] != "(":
            position = link_start + 1
            continue

        destination_start = label_end + 2
        if destination_start >= len(text):
            return links

        if text[destination_start] == "<":
            angle_wrapped = True
            destination_end = text.find(">", destination_start + 1)
            if (
                destination_end == -1
                or destination_end + 1 >= len(text)
                or text[destination_end + 1] != ")"
            ):
                position = destination_start
                continue
            url = text[destination_start + 1 : destination_end]
            link_end = destination_end + 2
        else:
            angle_wrapped = False
            cursor = destination_start
            nested_parentheses = 0
            destination_end = -1
            while cursor < len(text) and text[cursor] != "\n":
                character = text[cursor]
                if character == "(":
                    nested_parentheses += 1
                elif character == ")":
                    if nested_parentheses == 0:
                        destination_end = cursor
                        break
                    nested_parentheses -= 1
                cursor += 1
            if destination_end == -1:
                position = destination_start
                continue
            url = text[destination_start:destination_end]
            link_end = destination_end + 1

        raw_label = text[link_start + 1 : label_end]
        links.append(
            (unescape_markdown_label(raw_label), url, link_start, link_end, angle_wrapped)
        )
        position = link_end


def urls_outside_inline_links(
    text: str, links: list[tuple[str, str, int, int, bool]]
) -> list[str]:
    """Find HTTP(S) URLs not contained in an admitted inline citation form."""
    masked = list(text)
    for _, _, start, end, _ in links:
        masked[start:end] = " " * (end - start)
    return [
        match.group(0).rstrip(">.,;:!?")
        for match in ANY_HTTP_URL.finditer("".join(masked))
    ]


def validate_answer(
    path: Path, source_ledger: dict[str, object]
) -> tuple[str | None, list[str], list[str]]:
    text = read_utf8(path, "answer")
    errors: list[str] = []
    warnings: list[str] = []

    depth_matches = list(DEPTH_LINE.finditer(text))
    if len(depth_matches) != 1:
        if not depth_matches:
            return None, ["missing or malformed Depth/Checked line"], warnings
        return None, [f"expected exactly one Depth/Checked line; found {len(depth_matches)}"], warnings
    match = depth_matches[0]
    depth = match.group(1)
    try:
        date.fromisoformat(match.group(2))
    except ValueError:
        errors.append(f"invalid Checked date: {match.group(2)!r}")
    errors.extend(ordered_headings(text, REQUIRED_HEADINGS[depth]))
    errors.extend(substantive_section_errors(text, REQUIRED_HEADINGS[depth]))

    h2_headings = re.findall(r"(?m)^## [^#].*$", text)
    allowed_h2 = set(REQUIRED_HEADINGS[depth])
    if depth == "Standard":
        allowed_h2.add("## What this means")
    for heading in h2_headings:
        if heading not in allowed_h2:
            errors.append(
                f"unexpected level-two heading {heading!r}; use a required section or a level-three subsection"
            )

    if depth == "Deep":
        h1_headings = re.findall(r"(?m)^# [^#].*$", text)
        if len(h1_headings) != 1:
            errors.append(f"Deep output requires exactly one report-title heading; found {len(h1_headings)}")

    if depth == "Standard":
        implications = len(re.findall(r"(?m)^## What this means$", text))
        if implications > 1:
            errors.append("expected at most one '## What this means' heading")

    scope = source_ledger["scope"]
    research_shape = scope.get("research_shape")
    if depth in {"Standard", "Deep"} and not research_shape:
        errors.append(
            f"{depth} output requires scope.research_shape in the source ledger"
        )

    use_sources = [
        source for source in source_ledger["sources"] if source["verdict"] == "use"
    ]
    if research_shape == "broad_landscape":
        lineages = {
            source.get("evidence_lineage", "").strip() for source in use_sources
        }
        lineages.discard("")
        source_types = {source["source_type"] for source in use_sources}
        breadth_errors: list[str] = []
        if any(not source.get("evidence_lineage", "").strip() for source in use_sources):
            breadth_errors.append(
                "every use source in a broad landscape requires evidence_lineage"
            )
        if len(use_sources) < BROAD_MIN_SOURCES:
            breadth_errors.append(
                f"broad landscape requires at least {BROAD_MIN_SOURCES} distinct use sources; found {len(use_sources)}"
            )
        if len(lineages) < BROAD_MIN_LINEAGES:
            breadth_errors.append(
                f"broad landscape requires at least {BROAD_MIN_LINEAGES} evidence lineages; found {len(lineages)}"
            )
        if len(source_types) < BROAD_MIN_SOURCE_TYPES:
            breadth_errors.append(
                f"broad landscape requires at least {BROAD_MIN_SOURCE_TYPES} source types; found {len(source_types)}"
            )
        if breadth_errors:
            breadth_exception = scope.get("breadth_exception", "")
            has_gap = any(
                claim["status"] == "gap" for claim in source_ledger["claims"]
            )
            if not isinstance(breadth_exception, str) or not breadth_exception.strip() or not has_gap:
                errors.extend(breadth_errors)
                errors.append(
                    "a broad-landscape breadth shortfall requires a non-empty scope.breadth_exception and at least one explicit ledger gap"
                )

    approved_sources = {
        canonical_url(source["url"]): source
        for source in source_ledger["sources"]
        if source["verdict"] == "use"
    }
    cited_source_ids: set[str] = set()
    extracted_links = extract_inline_links(text)
    links: list[tuple[str, str]] = []
    for label, url, start, end, angle_wrapped in extracted_links:
        problem = direct_url_error(url)
        if problem:
            errors.append(f"inline link destination is not an explicit valid HTTP(S) URL: {url!r} ({problem})")
            continue
        if any(character in url for character in "()") and not angle_wrapped:
            errors.append(
                f"citation URL containing parentheses must use an angle-wrapped destination: {url}"
            )
        if start == 0 or end >= len(text) or text[start - 1] != "(" or text[end] != ")":
            errors.append(
                f"citation must use the required parenthetical receipt form: {url}"
            )
        links.append((label, url))
    for url in urls_outside_inline_links(text, extracted_links):
        errors.append(f"HTTP(S) URL appears outside an approved inline citation: {url}")
    if not links and "No adequate source found" not in text:
        errors.append("no descriptive source links found")
    for label, url in links:
        if not SOURCE_LABEL.fullmatch(label.strip()):
            errors.append(
                f"citation label lacks title, publisher/author, and date: {label!r}"
            )
        if is_search_result_url(url):
            errors.append(f"search-result URL is not a source receipt: {url}")
        source = approved_sources.get(canonical_url(url))
        if source is None:
            errors.append(f"citation URL is not an approved use source: {url}")
            continue
        cited_source_ids.add(source["id"])
        expected_label = (
            f"{source['title']} — {source['publisher']}, {source['publication_date']}"
        )
        if label.strip() != expected_label:
            errors.append(
                f"citation label does not match approved source {source['id']}: expected {expected_label!r}"
            )

    for source in approved_sources.values():
        if source["id"] not in cited_source_ids:
            errors.append(f"approved use source {source['id']} is not cited in the answer")

    gap_claims = [
        claim for claim in source_ledger["claims"] if claim["status"] == "gap"
    ]
    visible_gap_disclosures = text.count("No adequate source found")
    if visible_gap_disclosures < len(gap_claims):
        claim_word = "claim" if len(gap_claims) == 1 else "claims"
        disclosure_word = "disclosure" if len(gap_claims) == 1 else "disclosures"
        verb = "requires" if len(gap_claims) == 1 else "require"
        errors.append(
            f"{len(gap_claims)} ledger gap {claim_word} {verb} at least "
            f"{len(gap_claims)} visible 'No adequate source found' {disclosure_word}; "
            f"found {visible_gap_disclosures}"
        )

    required_epistemic_kinds = {
        claim["kind"]
        for claim in source_ledger["claims"]
        if claim["status"] == "supported" and claim["kind"] != "fact"
    }
    for kind in sorted(required_epistemic_kinds):
        label = EPISTEMIC_LABELS[kind]
        if not re.search(rf"\*\*{re.escape(label)}(?::)?\*\*", text):
            errors.append(
                f"supported {kind} material requires a visible **{label}** label"
            )

    if "No adequate source found" in text and links:
        warnings.append(
            "insufficiency is declared alongside links; confirm that context is not presented as support for the unsupported claim"
        )
    return depth, errors, warnings


def validate_record(path: Path, expected_depth: str) -> list[str]:
    text = read_utf8(path, "execution record")
    errors: list[str] = []
    if not re.search(r"(?m)^# Research Execution Record$", text):
        errors.append("record is missing '# Research Execution Record'")

    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = FIELD_LINE.match(line)
        if match:
            fields.setdefault(match.group(1), []).append(match.group(2).strip())

    for field in REQUIRED_RECORD_FIELDS:
        values = fields.get(field, [])
        if len(values) != 1:
            errors.append(f"record requires exactly one {field!r} field")
        elif not values[0]:
            errors.append(f"record field {field!r} must not be empty")

    if fields.get("Depth") and fields["Depth"][0] != expected_depth:
        errors.append(
            f"record depth {fields['Depth'][0]!r} does not match answer depth {expected_depth!r}"
        )

    if expected_depth in {"Standard", "Deep"}:
        for field in ("Search lanes", "Disconfirming route", "Stop rationale"):
            value = fields.get(field, [""])[0].lower()
            if value in {"none", "n/a", "not needed"}:
                errors.append(f"{expected_depth} record cannot leave {field!r} as {value!r}")

    if expected_depth == "Deep":
        value = fields.get("Critical recheck", [""])[0].lower()
        if value in {"none", "n/a", "not needed"}:
            errors.append("Deep record requires a substantive critical recheck entry")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("answer", type=Path)
    parser.add_argument("--record", required=True, type=Path)
    parser.add_argument("--sources", required=True, type=Path)
    args = parser.parse_args()

    for path in (args.answer, args.record, args.sources):
        if not path.is_absolute():
            print(f"FAIL: artifact path must be absolute: {path}")
            return 2
        if not path.is_file():
            print(f"FAIL: file not found: {path}")
            return 2

    source_ledger, source_errors = load_and_validate(args.sources)
    if source_errors:
        for error in source_errors:
            print(f"FAIL: source ledger: {error}")
        return 1
    if source_ledger is None:
        print("FAIL: source ledger could not be loaded")
        return 1

    try:
        depth, errors, warnings = validate_answer(args.answer, source_ledger)
        if depth:
            errors.extend(validate_record(args.record, depth))
    except InputReadError as exc:
        print(f"FAIL: {exc}")
        return 2

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(
            "Validation checks structure and recorded source admission; semantic source verification remains required."
        )
        return 1

    print(
        f"PASS: {depth} output structure, approved citations, and execution-record fields are valid."
    )
    print(
        "A pass does not prove that recorded evidence is true, applicable, or supportive."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
