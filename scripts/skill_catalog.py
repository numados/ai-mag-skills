#!/usr/bin/env python3
"""Single owner for skill metadata, the catalog command, and evaluation checks.

This module is the one place that knows how to read the ``name`` and
``description`` frontmatter of a ``SKILL.md``.  It is reused by
``scripts/check-skills.sh`` (``--check``) and by the catalog command
(``python3 scripts/skill_catalog.py``, which prints a deterministic TSV of
``name``, repository-relative ``SKILL.md`` path, and whitespace-normalized
description).

Supported frontmatter subset
----------------------------
The catalog only needs two string fields, ``name`` and ``description``.  This
module intentionally does *not* implement a YAML parser.  It supports exactly:

* Plain single-line scalars (``description: some text``), trimmed.
* Single-line quoted scalars (``'...'`` with ``''`` as an escaped quote, and
  ``"..."`` with the ``\\\\``, ``\\"``, ``\\n``, ``\\t``, ``\\r`` and ``\\0``
  escapes).
* Folded (``>``) and literal (``|``) block scalars, with the ``-`` (strip) and
  ``+`` (keep) chomping indicators.  No indentation indicators (``>2``).

Anything else that could make the value ambiguous is rejected rather than
silently accepted: flow collections (``[ ]``/``{ }``), block sequences
(``- item``), anchors/aliases/tags, multi-line plain or quoted scalars,
duplicate keys, unknown top-level keys, YAML ``null``/boolean keywords, and
malformed or unclosed frontmatter.

Block-scalar notes: content lines are dedented to the first content line's
indentation.  Folded scalars join single line breaks into spaces and turn blank
lines into line breaks; literal scalars preserve every line break.  More-indented
lines are preserved literally.  The exact break count when a more-indented line
is immediately adjacent to a blank line follows a simplified rule; that
combination does not occur in this catalog.

Only Python 3.9+ standard library modules are used.
"""

import argparse
import json
import re
import sys
from pathlib import Path

_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
_DELIMITER = re.compile(r"---[ \t]*\Z")
_KEY_LINE = re.compile(r"([A-Za-z][A-Za-z0-9_-]*):(?:[ \t]*(.*))?\Z")
_BLOCK_HEADER = re.compile(r"([|>])([+-])?[ \t]*\Z")

# A plain scalar may not start with any of these YAML indicator characters.
_UNSUPPORTED_START = set("-?:,[]{}#&*!|>'\"%@`")
# Explicit non-string YAML scalars rejected for a string-only subset.
_NON_STRING_SCALARS = {
    "~", "null", "Null", "NULL",
    "true", "True", "TRUE", "false", "False", "FALSE",
}

_DOUBLE_QUOTE_ESCAPES = {
    "\\": "\\", '"': '"', "n": "\n", "t": "\t", "r": "\r", "0": "\0",
}

_CHOMP = {"-": "strip", "+": "keep"}


class CatalogError(ValueError):
    """Raised when a SKILL.md has malformed or unsupported frontmatter."""


class EvalFileError(ValueError):
    """Raised when an evaluation ``files`` entry cannot be resolved."""


def normalize_whitespace(text):
    """Collapse all whitespace runs to single spaces and trim the ends."""
    return " ".join(text.split())


def skill_paths(root):
    """Return the sorted SKILL.md paths under ``skills/<category>/<name>/``."""
    return sorted(Path(root).glob("skills/*/*/SKILL.md"))


def _indent_width(line):
    width = 0
    for char in line:
        if char in (" ", "\t"):
            width += 1
        else:
            break
    return width


def _strip_block_indent(content, source):
    """Dedent block-scalar content lines to the first content line's indent."""
    base = None
    for line in content:
        if line.strip() != "":
            base = _indent_width(line)
            break
    if base is None:
        return []
    stripped = []
    for line in content:
        if line.strip() == "":
            stripped.append("")
        else:
            width = _indent_width(line)
            if width < base:
                raise CatalogError(
                    f"{source}: block scalar line is less indented than its first content line"
                )
            stripped.append(line[base:])
    return stripped


def _fold_lines(content_lines):
    """Fold a ``>`` block scalar into logical output lines.

    ``content_lines`` are base-indent-stripped: ``""`` marks a blank line, and a
    line starting with a space/tab is a preserved (more-indented) line.
    Returns a list of lines where ``""`` represents a blank output line.
    """
    lines = []
    paragraph = None
    pending_blank = 0

    def flush_paragraph():
        nonlocal paragraph
        if paragraph is not None:
            lines.append(paragraph)
            paragraph = None

    for line in content_lines:
        if line == "":
            pending_blank += 1
            flush_paragraph()
        elif line[0] in (" ", "\t"):
            flush_paragraph()
            if pending_blank:
                lines.extend([""] * pending_blank)
                pending_blank = 0
            lines.append(line)
        else:
            if pending_blank:
                lines.extend([""] * (pending_blank - 1))
                pending_blank = 0
            if paragraph is None:
                paragraph = line
            else:
                paragraph += " " + line
    flush_paragraph()
    if pending_blank:
        lines.extend([""] * pending_blank)
    return lines


def _apply_chomp(lines, chomp):
    """Apply YAML chomping to a list of output lines (``""`` is blank)."""
    if chomp == "keep":
        return "\n".join(lines) + ("\n" if lines else "")
    trimmed = list(lines)
    while trimmed and trimmed[-1] == "":
        trimmed.pop()
    if chomp == "strip":
        return "\n".join(trimmed)
    return "\n".join(trimmed) + ("\n" if trimmed else "")


def _block_value(style, chomp, content, source):
    stripped = _strip_block_indent(content, source)
    if style == "|":
        lines = list(stripped)
    else:
        lines = _fold_lines(stripped)
    return _apply_chomp(lines, chomp)


def _parse_double_quoted(text, source):
    if not text.startswith('"'):
        raise CatalogError(f"{source}: malformed double-quoted scalar")
    out = []
    index = 1
    while index < len(text):
        char = text[index]
        if char == '"':
            if text[index + 1 :].strip():
                raise CatalogError(
                    f"{source}: trailing content after double-quoted scalar"
                )
            return "".join(out)
        if char == "\\":
            index += 1
            if index >= len(text):
                raise CatalogError(f"{source}: trailing backslash in double-quoted scalar")
            escaped = text[index]
            if escaped not in _DOUBLE_QUOTE_ESCAPES:
                raise CatalogError(
                    f"{source}: unsupported escape \\{escaped} in double-quoted scalar"
                )
            out.append(_DOUBLE_QUOTE_ESCAPES[escaped])
        else:
            out.append(char)
        index += 1
    raise CatalogError(
        f"{source}: unsupported multi-line or malformed double-quoted scalar"
    )


def _parse_single_quoted(text, source):
    if not text.startswith("'"):
        raise CatalogError(f"{source}: malformed single-quoted scalar")
    out = []
    index = 1
    while index < len(text):
        char = text[index]
        if char == "'":
            if index + 1 < len(text) and text[index + 1] == "'":
                out.append("'")
                index += 2
                continue
            if text[index + 1 :].strip():
                raise CatalogError(
                    f"{source}: trailing content after single-quoted scalar"
                )
            return "".join(out)
        out.append(char)
        index += 1
    raise CatalogError(
        f"{source}: unsupported multi-line or malformed single-quoted scalar"
    )


def _parse_inline_scalar(rest, source):
    if rest == "":
        return ""
    if rest.startswith('"'):
        return _parse_double_quoted(rest, source)
    if rest.startswith("'"):
        return _parse_single_quoted(rest, source)
    if rest.strip() in _NON_STRING_SCALARS:
        raise CatalogError(f"{source}: unsupported non-string scalar {rest!r}")
    if rest[0] in _UNSUPPORTED_START:
        raise CatalogError(f"{source}: unsupported scalar value {rest!r}")
    return rest.strip()


def parse_frontmatter(text, source="<skill>"):
    """Parse ``name`` and ``description`` from YAML frontmatter.

    Returns ``{"name": str, "description": str}``.  Raises :class:`CatalogError`
    for malformed or unsupported frontmatter.  The description may be empty; the
    catalog-level emptiness policy is applied by :func:`read_skill_metadata`.
    """
    if not text:
        raise CatalogError(f"{source}: empty file")
    lines = text.splitlines()
    if not lines:
        raise CatalogError(f"{source}: empty file")
    if not _DELIMITER.fullmatch(lines[0]):
        raise CatalogError(f"{source}: first line must be a '---' frontmatter marker")

    end = None
    for index in range(1, len(lines)):
        if _DELIMITER.fullmatch(lines[index]):
            end = index
            break
    if end is None:
        raise CatalogError(f"{source}: frontmatter is not closed (missing '---')")

    body = lines[1:end]
    fields = {}
    index = 0
    while index < len(body):
        line = body[index]
        if line.strip() == "":
            index += 1
            continue
        if line[:1] in (" ", "\t"):
            raise CatalogError(
                f"{source}: unexpected indented line outside a block scalar: {line!r}"
            )
        match = _KEY_LINE.match(line)
        if not match:
            raise CatalogError(f"{source}: unsupported frontmatter line: {line!r}")
        key = match.group(1)
        rest = match.group(2) or ""
        if key not in ("name", "description"):
            raise CatalogError(f"{source}: unsupported frontmatter key {key!r}")
        if key in fields:
            raise CatalogError(f"{source}: duplicate frontmatter key {key!r}")

        block = _BLOCK_HEADER.match(rest)
        if block:
            style, chomp_indicator = block.group(1), block.group(2)
            content = []
            index += 1
            while index < len(body):
                candidate = body[index]
                if candidate.strip() == "" or candidate[:1] in (" ", "\t"):
                    content.append(candidate)
                    index += 1
                else:
                    break
            fields[key] = _block_value(
                style, _CHOMP.get(chomp_indicator, "clip"), content, source
            )
            continue

        if rest.startswith("|") or rest.startswith(">"):
            raise CatalogError(f"{source}: unsupported block scalar indicator {rest!r}")

        fields[key] = _parse_inline_scalar(rest, source)
        index += 1

    return fields


def validate_name(name):
    """Return an error string, or ``None`` if the name is acceptable."""
    if not name:
        return "missing frontmatter name"
    if not _NAME_PATTERN.fullmatch(name):
        return f"invalid skill name {name!r}"
    if not name.startswith("mag-"):
        return f"public skill name must start with mag-: {name!r}"
    return None


def read_skill_metadata(path, root):
    """Parse and validate one SKILL.md; return ``(name, description)``.

    Raises :class:`CatalogError` for malformed frontmatter, invalid names, and
    missing/empty descriptions.
    """
    rel = Path(path).relative_to(root).as_posix()
    fields = parse_frontmatter(Path(path).read_text(encoding="utf-8"), rel)
    name = fields.get("name", "")
    error = validate_name(name)
    if error:
        raise CatalogError(f"{rel}: {error}")
    if not normalize_whitespace(fields.get("description", "")):
        raise CatalogError(f"{rel}: missing or empty frontmatter description")
    return name, fields["description"]


def catalog_rows(root):
    """Return sorted ``(name, repo-relative path, normalized description)`` rows."""
    rows = []
    for path in skill_paths(root):
        name, description = read_skill_metadata(path, root)
        rows.append(
            (name, path.relative_to(root).as_posix(), normalize_whitespace(description))
        )
    rows.sort(key=lambda row: row[0])
    return rows


def _validate_manifest(root, skills):
    errors = []
    manifest_path = root / ".claude-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f".claude-plugin/plugin.json: cannot parse JSON: {exc}")
        return errors
    actual = sorted(
        "./" + path.parent.relative_to(root).as_posix() for path in skills
    )
    declared = sorted(manifest.get("skills", []))
    if declared != actual:
        errors.append(".claude-plugin/plugin.json: skills list does not match disk")
    for entry in declared:
        if not entry.startswith("./"):
            errors.append(f".claude-plugin/plugin.json: entry must start with ./: {entry}")
        if not (root / entry[2:] / "SKILL.md").is_file():
            errors.append(f".claude-plugin/plugin.json: missing SKILL.md for {entry}")
    return errors


def _validate_readme(root, skills):
    errors = []
    readme_path = root / "README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"README.md: cannot read: {exc}")
        return errors
    for path in skills:
        rel = path.relative_to(root).as_posix()
        if rel not in readme:
            errors.append(f"README.md: missing link for {rel}")
    return errors


def validate_catalog(root):
    """Validate skill metadata, the plugin manifest, and README links."""
    errors = []
    skills = skill_paths(root)
    if not skills:
        errors.append("no skills found under skills/<category>/<name>/SKILL.md")
    seen_names = []
    for path in skills:
        rel = path.relative_to(root).as_posix()
        try:
            name, _description = read_skill_metadata(path, root)
        except CatalogError as exc:
            errors.append(str(exc))
            continue
        if name in seen_names:
            errors.append(f"{rel}: duplicate skill name {name!r}")
            continue
        seen_names.append(name)
    errors.extend(_validate_manifest(root, skills))
    errors.extend(_validate_readme(root, skills))
    return errors


def skill_names(root):
    """Return the set of skill names found in frontmatter (lenient parsing)."""
    names = set()
    for path in skill_paths(root):
        try:
            fields = parse_frontmatter(
                path.read_text(encoding="utf-8"), path.relative_to(root).as_posix()
            )
        except CatalogError:
            continue
        if fields.get("name"):
            names.add(fields["name"])
    return names


def eval_files(root):
    """Return the sorted ``evals/<category>/<skill>/evals.json`` paths."""
    return sorted(Path(root).glob("evals/*/*/evals.json"))


def resolve_eval_file(root, eval_dir, entry):
    """Resolve one ``files`` entry to an existing path inside the eval directory.

    Two conventions are accepted, resolved deterministically:

    * eval-file-relative (``fixtures/x.cs``), relative to the directory
      containing ``evals.json``;
    * repository-relative (``evals/<category>/<skill>/fixtures/x.cs``), relative
      to the repository root.

    If both conventions resolve to two *different* existing files the entry is
    ambiguous.  A missing entry is an error, and a resolved file outside the
    eval directory is rejected.  Returns the resolved absolute :class:`Path`.
    """
    if not isinstance(entry, str):
        raise EvalFileError(f"files entry is not a string: {entry!r}")
    entry = entry.strip()
    if not entry:
        raise EvalFileError("empty files entry")
    if Path(entry).is_absolute():
        raise EvalFileError(f"absolute files entry is not allowed: {entry!r}")
    root = Path(root).resolve()
    eval_dir = Path(eval_dir).resolve()
    candidates = [
        (eval_dir / entry).resolve(),
        (root / entry).resolve(),
    ]
    existing = []
    for candidate in candidates:
        if candidate.is_file() and candidate not in existing:
            existing.append(candidate)
    if len(existing) > 1:
        raise EvalFileError(
            f"ambiguous files entry {entry!r}: resolves to {existing[0].as_posix()} "
            f"and {existing[1].as_posix()}"
        )
    if not existing:
        raise EvalFileError(f"missing files entry {entry!r}")
    resolved = existing[0]
    if not resolved.is_relative_to(eval_dir):
        raise EvalFileError(f"files entry escapes its eval directory: {entry!r}")
    return resolved


def validate_evals(root):
    """Validate every ``evals/*/*/evals.json`` file and its fixture references."""
    errors = []
    names = skill_names(root)
    for evals_path in eval_files(root):
        rel = evals_path.relative_to(root).as_posix()
        try:
            data = json.loads(evals_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{rel}: cannot parse JSON: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: top-level must be a JSON object")
            continue
        skill_name = data.get("skill_name")
        if not isinstance(skill_name, str) or not skill_name:
            errors.append(f"{rel}: missing or non-string skill_name")
        elif skill_name not in names:
            errors.append(f"{rel}: skill_name {skill_name!r} does not correspond to a skill")
        evals = data.get("evals")
        if not isinstance(evals, list):
            errors.append(f"{rel}: 'evals' must be a list")
            continue
        seen_ids = set()
        for position, entry in enumerate(evals):
            where = f"{rel}: eval #{position}"
            if not isinstance(entry, dict):
                errors.append(f"{where}: entry is not an object")
                continue
            eval_id = entry.get("id")
            if eval_id is None:
                errors.append(f"{where}: missing id")
            elif eval_id in seen_ids:
                errors.append(f"{where}: duplicate id {eval_id!r}")
            else:
                seen_ids.add(eval_id)
            for field in ("prompt", "expected_output"):
                value = entry.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{where}: missing or empty {field}")
            files = entry.get("files", [])
            if not isinstance(files, list):
                errors.append(f"{where}: 'files' must be a list")
                continue
            for file_entry in files:
                try:
                    resolve_eval_file(root, evals_path.parent, file_entry)
                except EvalFileError as exc:
                    errors.append(f"{where}: {exc}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the catalog and evaluations without emitting TSV",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent

    if args.check:
        errors = validate_catalog(root) + validate_evals(root)
        if errors:
            for error in errors:
                print(f"FAIL {error}")
            return 1
        print(f"OK {len(skill_paths(root))} skills, catalog, README, and evals are valid")
        return 0

    try:
        rows = catalog_rows(root)
    except CatalogError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    for name, rel, description in rows:
        print(f"{name}\t{rel}\t{description}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
