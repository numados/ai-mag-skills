#!/usr/bin/env python3
"""Bundle owned references and the license so each skill installs independently."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

# Each reference has one editable owner. Destinations are committed distribution copies.
SHARED_REFERENCES = {
    "skills/development/mag-obsidian-markdown/references/note-format.md": (
        "skills/development/mag-knowledge-capture/references/obsidian-note-format.md",
        "skills/development/mag-task-storage/references/obsidian-note-format.md",
    ),
    "skills/development/mag-task-storage/references/storage-configuration.md": (
        "skills/development/mag-knowledge-capture/references/storage-configuration.md",
    ),
    "skills/rust/mag-rust-implementation/references/api-contracts.md": (
        "skills/rust/mag-rust-project/references/api-contracts.md",
        "skills/rust/mag-rust-review/references/api-contracts.md",
        "skills/rust/mag-rust-refactor/references/api-contracts.md",
    ),
    "skills/rust/mag-rust-async-reliability/references/lifecycle.md": (
        "skills/rust/mag-rust-implementation/references/lifecycle.md",
    ),
    "skills/rust/mag-rust-async-reliability/references/concurrency-model.md": (
        "skills/rust/mag-rust-unsafe-review/references/concurrency-model.md",
        "skills/rust/mag-rust-review/references/concurrency-model.md",
        "skills/rust/mag-rust-testing-quality/references/concurrency-model.md",
    ),
    "skills/development/mag-code-design/references/principles.md": (
        "skills/development/mag-code-construction/references/principles.md",
        "skills/dotnet/mag-csharp-review/references/principles.md",
    ),
    "skills/development/mag-code-design/references/patterns.md": (
        "skills/development/mag-code-construction/references/patterns.md",
    ),
    "skills/dotnet/mag-csharp-review/references/api-compatibility.md": (
        "skills/dotnet/mag-csharp-refactor/references/api-compatibility.md",
    ),
    "skills/dotnet/mag-csharp-implementation/references/version-and-docs.md": (
        "skills/dotnet/mag-csharp-explain/references/version-and-docs.md",
    ),
    "skills/development/mag-code-construction/references/technology-evidence.md": (
        "skills/development/mag-task-planning/references/technology-evidence.md",
        "skills/dotnet/mag-dotnet-testing-quality/references/technology-evidence.md",
    ),
}


def skill_directories(root):
    return [path.parent for path in sorted(root.glob("skills/*/*/SKILL.md"))]


def resource_copies(root):
    for source, destinations in SHARED_REFERENCES.items():
        for destination in destinations:
            yield root / source, root / destination
    for skill in skill_directories(root):
        yield root / "LICENSE", skill / "LICENSE"


def sync_resources(root, check=False):
    errors = []
    for source, destination in resource_copies(root):
        if not source.is_file():
            errors.append(f"missing resource owner: {source.relative_to(root)}")
            continue
        expected = source.read_text(encoding="utf-8")
        if destination.suffix == ".md":
            expected = (
                f"<!-- Generated from {source.relative_to(root).as_posix()}. "
                "Do not edit this copy; run python3 scripts/sync-skill-resources.py "
                "in the catalog repository. No source checkout is needed at runtime. -->\n\n"
                + expected
            )
        if destination.is_file() and destination.read_text(encoding="utf-8") == expected:
            continue
        if check:
            errors.append(f"missing or stale bundled resource: {destination.relative_to(root)}")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(expected, encoding="utf-8")
    return errors


def validate_local_references(root):
    errors = []
    for skill in skill_directories(root):
        for path in sorted(skill.rglob("*.md")):
            text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
            # Markdown links and the catalog's inline-code reference convention.
            links = re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text)
            links += re.findall(r"`(references/[^`\s]+)`", text)
            for link in links:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(skill.resolve()):
                    errors.append(f"{path.relative_to(root)}: reference leaves skill: {link}")
                elif not target.is_file():
                    errors.append(f"{path.relative_to(root)}: missing local reference: {link}")
    return errors


def validate_ownership(root):
    """Every reference has one owner; owners are never generated copies."""
    errors = []
    destinations = {}
    for source, targets in SHARED_REFERENCES.items():
        for destination in targets:
            if destination in destinations:
                errors.append(
                    f"duplicate generated destination: {destination} "
                    f"({destinations[destination]} and {source})"
                )
            destinations[destination] = source
    for source in SHARED_REFERENCES:
        if source in destinations:
            errors.append(f"owner is also a generated copy: {source}")
    return errors


def main(argv=None, root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing files")
    args = parser.parse_args(argv)
    if root is None:
        root = Path(__file__).resolve().parent.parent
    ownership_errors = validate_ownership(root)
    if ownership_errors:
        for error in ownership_errors:
            print(f"FAIL {error}")
        print("FAIL refusing to synchronize an invalid reference ownership map")
        return 1
    errors = sync_resources(root, check=args.check) + validate_local_references(root)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"OK bundled resources and local references for {len(skill_directories(root))} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
