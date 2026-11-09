#!/usr/bin/env python3
"""Verify that a real client discovers every published skill.

The ``skills`` CLI parses ``SKILL.md`` frontmatter with a full YAML parser.
Frontmatter that this repository's stricter reader accepts but YAML rejects is
therefore silently skipped at install time, while the command still exits 0.
This check turns that silent green into a failure: it reads the CLI listing on
stdin and compares it with the skill directories on disk.

Usage (from the repository root)::

    npx skills@latest add ./ --list | python3 scripts/check_discovery.py

Only the Python 3.9+ standard library is used.
"""

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
# A skill entry is a line whose entire visible content is the name, indented
# under the list.  Matching the whole line, not a substring, keeps a description
# that happens to end with "│    mag-something" from counting as an entry.
_ENTRY = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
# Real skip notices are written by the CLI as a shallow warning line, after a
# box-drawing prefix and a warning glyph.  A description indented under an
# entry is deeper, so requiring a shallow indent keeps prose from matching.
_SKIP_NOTICE = re.compile(
    r"[^\w\s]{0,3}\s{0,3}(?:[⚠✖✗×]\ufe0f?\s*)?skipped\s", re.IGNORECASE
)
# Outside an agent the CLI prints an intro banner line that reads "skills" —
# name-shaped, but not a skill.  Parse only the listing section, delimited by
# its header and the closing hint, so banner text cannot masquerade as an entry.
_LISTING_START = re.compile(r"available\s+skills", re.IGNORECASE)
_LISTING_END = re.compile(r"use\s+--skill|run\s+without\s+--list", re.IGNORECASE)


def _entry_candidate(line):
    """Return the name-shaped remainder of a listing line, or ``None``."""
    return re.sub(r"^[^a-z0-9]+", "", line.strip())


def disk_skills(root):
    """Return the published skill names under ``skills/<category>/<name>/``."""
    return {path.parent.name for path in Path(root).glob("skills/*/*/SKILL.md")}


def listing_section(text):
    """Return the listing lines, excluding banners and trailing hints."""
    lines = _ANSI.sub("", text).splitlines()
    start = next(
        (index for index, line in enumerate(lines) if _LISTING_START.search(line)),
        None,
    )
    if start is None:
        # Unknown layout: fall back to the whole text rather than nothing.
        return lines
    for end in range(start + 1, len(lines)):
        if _LISTING_END.search(lines[end]):
            return lines[start + 1 : end]
    return lines[start + 1 :]


def parse_listing(text):
    """Return discovered skill names from a ``skills add --list`` listing."""
    names = set()
    for line in listing_section(text):
        candidate = _entry_candidate(line)
        if _ENTRY.fullmatch(candidate):
            names.add(candidate)
    return names


def skipped_notices(text):
    """Return the client's skipped-skill warning lines."""
    notices = []
    for line in _ANSI.sub("", text).splitlines():
        if _SKIP_NOTICE.match(line.strip()):
            notices.append(line.strip())
    return notices


def validate(text, root):
    """Return a list of human-readable discovery errors."""
    errors = []
    errors.extend(
        f"client skipped a skill: {notice}" for notice in skipped_notices(text)
    )

    expected = disk_skills(root)
    discovered = parse_listing(text)
    # An empty parse means this verifier no longer understands the client's
    # output, not that every skill is broken.  Reporting "not discovered" for
    # each skill would bury that distinction, so name the real problem first.
    if expected and not discovered:
        errors.append(
            "could not parse any skill names from the client listing "
            "(client output format may have changed)"
        )
    for name in sorted(expected - discovered):
        errors.append(f"skill not discovered by the client: {name}")
    for name in sorted(discovered - expected):
        errors.append(f"client listed a skill that has no SKILL.md on disk: {name}")
    return errors


def main(root, stdin):
    errors = validate(stdin.read(), root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"OK {len(disk_skills(root))} skills discovered by the client")
    return 0


if __name__ == "__main__":
    sys.exit(main(_REPO, sys.stdin))
