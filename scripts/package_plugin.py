#!/usr/bin/env python3
"""Build deterministic public skill and Claude plugin release ZIPs."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path('skills/research-with-receipts')
RUNTIME_FILES = (
    'SKILL.md', 'agents/openai.yaml', 'agents/research-lane-brief.md',
    'references/reader-first-output.md', 'references/search-lane-method.md',
    'references/source-ledger-schema.md', 'scripts/validate_output.py',
    'scripts/validate_sources.py',
)


def write_zip(path: Path, files: dict[str, Path]) -> None:
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, source in sorted(files.items()):
            if source.is_symlink() or not source.is_file():
                raise ValueError(f'Expected regular release file: {source}')
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    with zipfile.ZipFile(path) as archive:
        assert archive.namelist() == sorted(files)
        assert archive.testzip() is None


def main() -> int:
    manifests = [json.loads((ROOT / name / 'plugin.json').read_text())
                 for name in ('.claude-plugin', '.codex-plugin')]
    version = manifests[0]['version']
    assert all(m['version'] == version and m['license'] == 'MIT' for m in manifests)
    runtime = {name: ROOT / RUNTIME / name for name in RUNTIME_FILES}
    plugin = {str(RUNTIME / name): path for name, path in runtime.items()}
    plugin.update({name: ROOT / name for name in ('.claude-plugin/plugin.json', 'README.md', 'LICENSE')})
    skill = {f'research-with-receipts/{name}': path for name, path in runtime.items()}
    skill['research-with-receipts/LICENSE'] = ROOT / 'LICENSE'
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    sums = []
    for stem, files in [('agency-research-plugin', plugin), ('research-with-receipts', skill)]:
        versioned = output / f'{stem}-{version}.zip'
        write_zip(versioned, files)
        alias = output / f'{stem}.zip'
        alias.write_bytes(versioned.read_bytes())
        for path in (versioned, alias):
            sums.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n')
            print(path)
    (output / 'SHA256SUMS.txt').write_text(''.join(sums))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
