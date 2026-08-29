#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$TEST_DIR/.." && pwd)"
VALIDATOR="${VALIDATOR:-$PLUGIN_ROOT/skills/research-with-receipts/scripts/validate_output.py}"
SOURCE_VALIDATOR="${SOURCE_VALIDATOR:-$PLUGIN_ROOT/skills/research-with-receipts/scripts/validate_sources.py}"
FIXTURES="$TEST_DIR/fixtures"

python3 "$VALIDATOR" "$FIXTURES/quick-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/standard-valid.md" --record "$FIXTURES/standard-record-valid.md" --sources "$FIXTURES/source-gate/standard-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/standard-broad-gap-valid.md" --record "$FIXTURES/standard-record-valid.md" --sources "$FIXTURES/source-gate/broad-gap-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/deep-valid.md" --record "$FIXTURES/deep-record-valid.md" --sources "$FIXTURES/source-gate/deep-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/insufficient-valid.md" --record "$FIXTURES/insufficient-record-valid.md" --sources "$FIXTURES/source-gate/insufficient-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/parentheses-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/parentheses-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/month-date-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/month-date-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/bracket-title-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/bracket-title-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/mixed-gap-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/mixed-gap-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/two-gap-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/two-gap-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/inference-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/inference-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/two-inference-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/two-inference-ledger.json"
python3 "$VALIDATOR" "$FIXTURES/grouped-inference-valid.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/two-inference-ledger.json"

if python3 "$VALIDATOR" "$FIXTURES/quick-valid.md" --record "$FIXTURES/invalid-record-missing-access-escalation.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: execution record without access escalation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-search-link.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: invalid search-result citation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-non-parenthetical-citation.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: non-parenthetical citation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-broad-landscape-thin.md" --record "$FIXTURES/standard-record-valid.md" --sources "$FIXTURES/source-gate/broad-thin-ledger.json"; then
  echo "FAIL: thin broad landscape without a documented evidence gap unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-date.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: invalid checked date unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-extra-heading.md" --record "$FIXTURES/standard-record-valid.md" --sources "$FIXTURES/source-gate/standard-ledger.json"; then
  echo "FAIL: unexpected level-two heading unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-unapproved-link.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: unapproved final citation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-ledger-label.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: citation metadata inconsistent with ledger unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-hidden-unapproved-url.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: URL outside an approved inline citation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-image-citation.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: image syntax used as a source citation unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-uppercase-unapproved-url.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: uppercase-scheme unapproved URL unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-scheme-relative-link.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: scheme-relative source link unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-raw-parentheses-link.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/parentheses-ledger.json"; then
  echo "FAIL: unwrapped parenthesized destination unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-missing-gap-disclosure.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/mixed-gap-ledger.json"; then
  echo "FAIL: ledger gap without visible insufficiency disclosure unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-one-disclosure-for-two-gaps.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/two-gap-ledger.json"; then
  echo "FAIL: one insufficiency disclosure unexpectedly covered two ledger gaps"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-missing-epistemic-label.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/inference-ledger.json"; then
  echo "FAIL: inference claim without visible epistemic label unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-empty-section.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: empty required section unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-comment-only-section.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: comment-only required section unexpectedly passed"
  exit 1
fi

if python3 "$VALIDATOR" "$FIXTURES/invalid-empty-fence-section.md" --record "$FIXTURES/quick-record-valid.md" --sources "$FIXTURES/source-gate/quick-ledger.json"; then
  echo "FAIL: fence-only required section unexpectedly passed"
  exit 1
fi

if (
  cd "$TEST_DIR"
  python3 "$VALIDATOR" fixtures/quick-valid.md --record fixtures/quick-record-valid.md --sources fixtures/source-gate/quick-ledger.json
); then
  echo "FAIL: relative artifact paths unexpectedly passed"
  exit 1
fi

python3 "$TEST_DIR/test-validator-read-errors.py" "$VALIDATOR" "$FIXTURES"

SOURCE_VALIDATOR="$SOURCE_VALIDATOR" bash "$TEST_DIR/run-source-gate-fixtures.sh"

echo "PASS: validator fixtures"
