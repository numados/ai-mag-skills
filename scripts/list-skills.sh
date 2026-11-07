#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

find skills -mindepth 3 -maxdepth 3 -type f -name SKILL.md -print \
  | sed 's|^|./|' \
  | sort
