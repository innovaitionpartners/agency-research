#!/usr/bin/env python3
"""Build a deterministic Agency Research plugin ZIP from tracked source files."""

from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist"
OUTPUT_PATH = OUTPUT_DIR / "agency-research.zip"
EXCLUDED_PREFIXES = ("docs/", "evals/", "tests/", "dist/")
EXCLUDED_FILES = {".gitignore", "AGENTS.md", "scripts/package_plugin.py"}


def tracked_runtime_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        if not line or line in EXCLUDED_FILES or line.startswith(EXCLUDED_PREFIXES):
            continue
        path = ROOT / line
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def main() -> int:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUTPUT_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in tracked_runtime_files():
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())
    print(OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
