#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

python3 scripts/sync-skill-resources.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/skill_catalog.py --check
