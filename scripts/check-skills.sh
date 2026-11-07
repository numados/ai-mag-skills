#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

python3 - <<'PY'
import json
import re
from pathlib import Path

root = Path('.')
manifest_path = root / '.claude-plugin' / 'plugin.json'
readme_path = root / 'README.md'
skills = sorted(root.glob('skills/*/*/SKILL.md'))
errors = []
names = []

if not skills:
    errors.append('no skills found under skills/<category>/<name>/SKILL.md')

for path in skills:
    if path.parts[-3] == '.':
        errors.append(f'{path}: invalid catalog path')
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        errors.append(f'{path}: first line must be YAML frontmatter')
        continue
    end = text.find('\n---', 4)
    if end == -1:
        errors.append(f'{path}: YAML frontmatter is not closed')
        continue
    frontmatter = text[4:end].splitlines()
    values = {}
    for line in frontmatter:
        match = re.match(r'^(name|description):\s*(.*)$', line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"\'')
    name = values.get('name', '')
    description = values.get('description', '')
    if not name:
        errors.append(f'{path}: missing frontmatter name')
    elif not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
        errors.append(f'{path}: invalid skill name {name!r}')
    elif not name.startswith('mag-'):
        errors.append(f'{path}: public skill name must start with mag-: {name!r}')
    elif name in names:
        errors.append(f'{path}: duplicate skill name {name!r}')
    else:
        names.append(name)
    if not description:
        errors.append(f'{path}: missing frontmatter description')

try:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
except Exception as exc:
    errors.append(f'{manifest_path}: cannot parse JSON: {exc}')
else:
    actual = sorted('./' + str(path.parent) for path in skills)
    declared = sorted(manifest.get('skills', []))
    if declared != actual:
        errors.append(f'{manifest_path}: skills list does not match disk')
    for entry in declared:
        if not entry.startswith('./'):
            errors.append(f'{manifest_path}: entry must start with ./: {entry}')
        if not (root / entry[2:] / 'SKILL.md').is_file():
            errors.append(f'{manifest_path}: missing SKILL.md for {entry}')

for path in skills:
    link = str(path)
    if link not in readme_path.read_text(encoding='utf-8'):
        errors.append(f'{readme_path}: missing link for {link}')

if errors:
    for error in errors:
        print(f'FAIL {error}')
    raise SystemExit(1)

print(f'OK {len(skills)} skills, manifests, and README links are valid')
PY
