#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$TEST_DIR/.." && pwd)"
VALIDATOR="${SOURCE_VALIDATOR:-$PLUGIN_ROOT/skills/research-with-receipts/scripts/validate_sources.py}"
FIXTURES="$TEST_DIR/fixtures/source-gate"
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

python3 "$VALIDATOR" "$FIXTURES/valid.json"
python3 "$VALIDATOR" "$FIXTURES/valid-month-date.json"
python3 "$VALIDATOR" "$FIXTURES/valid-global-ip.json"

expect_fail() {
  local fixture="$1"
  local expected="$2"
  local output="$SCRATCH/$(basename "$fixture").out"

  if python3 "$VALIDATOR" "$FIXTURES/$fixture" >"$output" 2>&1; then
    echo "FAIL: $fixture unexpectedly passed"
    exit 1
  fi
  if ! grep -Fq "$expected" "$output"; then
    echo "FAIL: $fixture did not report expected error: $expected"
    sed -n '1,120p' "$output"
    exit 1
  fi
}

expect_fail "invalid-search-url.json" "use source S1 cannot use a search-result URL"
expect_fail "invalid-version-bool.json" "ledger version must be the integer 1"
expect_fail "invalid-version-float.json" "ledger version must be the integer 1"
expect_fail "invalid-compact-date.json" "scope.date_start must be a valid YYYY-MM-DD date"
expect_fail "invalid-publication-year-zero.json" "source S1 publication_date contains an invalid year"
expect_fail "invalid-search-url-country.json" "use source S1 cannot use a search-result URL"
expect_fail "invalid-google-scholar.json" "use source S1 cannot use a search-result URL"
expect_fail "invalid-homepage.json" "use source S1 cannot use a homepage URL"
expect_fail "invalid-homepage-query.json" "use source S1 cannot use a homepage URL"
expect_fail "invalid-space-url.json" "source S1 URL cannot contain whitespace or control characters"
expect_fail "invalid-port-url.json" "source S1 URL has an invalid port"
expect_fail "invalid-empty-host-label.json" "source S1 URL has an invalid hostname"
expect_fail "invalid-double-dot-host.json" "source S1 URL has an invalid hostname"
expect_fail "invalid-leading-hyphen-host.json" "source S1 URL has an invalid hostname"
expect_fail "invalid-localhost-url.json" "source S1 URL hostname is not public"
expect_fail "invalid-private-ip-url.json" "source S1 URL hostname is not public"
expect_fail "invalid-reserved-host.json" "source S1 URL hostname is reserved for non-public use"
expect_fail "invalid-newline-title.json" "source S1 field 'title' must be single-line and control-free"
expect_fail "invalid-excluded-type.json" "use source S1 has excluded source_type 'press_release'"
expect_fail "invalid-unopened.json" "use source S1 must be opened"
expect_fail "invalid-inaccessible.json" "use source S1 must have access 'full' or 'partial'"
expect_fail "invalid-date-range.json" "use source S1 falls outside the confirmed date range without date_exception"
expect_fail "invalid-date-not-shown-with-range.json" "use source S1 has no publication date inside a bounded date range without date_exception"
expect_fail "invalid-partial-date-boundary.json" "use source S1 has partial publication-date precision that crosses the confirmed date boundary without date_exception"
expect_fail "invalid-scope-mismatch.json" "use source S1 cannot have scope_match 'mismatch'"
expect_fail "invalid-superseded.json" "use source S1 cannot be superseded"
expect_fail "invalid-missing-evidence.json" "use source S1 requires specific evidence from the opened page"
expect_fail "invalid-missing-scope-note.json" "use source S1 requires a scope_note"
expect_fail "invalid-missing-limitations.json" "use source S1 requires limitations or 'none material'"
expect_fail "invalid-field-type.json" "source S1 field 'url' must be a non-empty string"
expect_fail "invalid-enum-types.json" "source S1 field 'source_type' must be a non-empty string"
expect_fail "invalid-duplicate-url.json" "sources S1 and S2 have the same direct URL"
expect_fail "invalid-duplicate-query-order.json" "sources S1 and S2 have the same direct URL"
expect_fail "invalid-duplicate-trailing-dot.json" "sources S1 and S2 have the same direct URL"
expect_fail "invalid-duplicate-default-port.json" "sources S1 and S2 have the same direct URL"
expect_fail "invalid-claim-source.json" "supported claim C1 can reference only use sources; S1 is 'context_only'"

if (
  cd "$TEST_DIR"
  python3 "$VALIDATOR" fixtures/source-gate/valid.json
); then
  echo "FAIL: relative ledger path unexpectedly passed"
  exit 1
fi

echo "PASS: source-admission gate fixtures"
