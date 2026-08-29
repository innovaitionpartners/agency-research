#!/usr/bin/env python3
"""Verify that unreadable UTF-8 inputs fail cleanly instead of raising tracebacks."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    validator = Path(sys.argv[1]).resolve()
    fixtures = Path(sys.argv[2]).resolve()
    with tempfile.TemporaryDirectory() as temp_dir:
        invalid_answer = Path(temp_dir) / "invalid-utf8.md"
        invalid_record = Path(temp_dir) / "invalid-record-utf8.md"
        invalid_answer.write_bytes(b"\xff\xfe\x00")
        invalid_record.write_bytes(b"\xff\xfe\x00")
        answer_result = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(invalid_answer),
                "--record",
                str(fixtures / "quick-record-valid.md"),
                "--sources",
                str(fixtures / "source-gate/quick-ledger.json"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        record_result = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(fixtures / "quick-valid.md"),
                "--record",
                str(invalid_record),
                "--sources",
                str(fixtures / "source-gate/quick-ledger.json"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    for label, result, expected in (
        ("answer", answer_result, "FAIL: cannot read UTF-8 answer file"),
        ("execution record", record_result, "FAIL: cannot read UTF-8 execution record file"),
    ):
        if result.returncode != 2:
            print(f"FAIL: invalid UTF-8 {label} returned {result.returncode}, expected 2")
            print(result.stdout)
            print(result.stderr)
            return 1
        if expected not in result.stdout:
            print(f"FAIL: invalid UTF-8 {label} did not produce an actionable read error")
            print(result.stdout)
            print(result.stderr)
            return 1
        if "Traceback" in result.stdout or "Traceback" in result.stderr:
            print(f"FAIL: invalid UTF-8 {label} produced a traceback")
            return 1
    print("PASS: validator reports unreadable UTF-8 inputs cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
