"""Regression checks for the client-discovery verifier.

The ``skills`` CLI exits 0 even when it skips a skill whose frontmatter a YAML
parser rejects.  These tests pin the verifier that turns that silent success
into a named failure.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "check_discovery", REPO / "scripts/check_discovery.py"
)
discovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discovery)


def listing(*names, skipped=None):
    lines = []
    if skipped:
        lines.append(f"│ ✖ Skipped /repo/skills/test/{skipped}/SKILL.md — YAML parse error")
    lines.append("│ Found %d skills" % len(names))
    lines.append("│ Available Skills")
    for name in names:
        lines.append("│")
        lines.append(f"│    {name}")
        lines.append("│")
        lines.append(f"│      {name} does something useful.")
        lines.append("│")
    return "\n".join(lines) + "\n"


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in ("mag-one", "mag-two"):
            skill = self.root / "skills" / "test" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: A test skill.\n---\n# Body\n",
                encoding="utf-8",
            )

    def test_complete_listing_is_clean(self):
        self.assertEqual([], discovery.validate(listing("mag-one", "mag-two"), self.root))

    def test_missing_skill_is_reported(self):
        errors = discovery.validate(listing("mag-one"), self.root)
        self.assertTrue(any("not discovered" in e and "mag-two" in e for e in errors), errors)

    def test_skip_notice_is_reported_even_when_names_match(self):
        errors = discovery.validate(
            listing("mag-one", "mag-two", skipped="mag-two"), self.root
        )
        self.assertTrue(any("skipped" in e for e in errors), errors)

    def test_unexpected_name_is_reported(self):
        errors = discovery.validate(listing("mag-one", "mag-two", "mag-ghost"), self.root)
        self.assertTrue(any("no SKILL.md on disk" in e for e in errors), errors)

    def test_descriptions_and_headers_are_not_parsed_as_names(self):
        text = "\n".join(
            [
                "│",
                "│ ✗ Source: /repo/ai-mag-skills",
                "│",
                "Numados Skills",
                "│",
                "│    mag-one",
                "│",
                "│      Read the guide: quote values containing a colon.",
                "│",
                "│    mag-two",
                "│",
                "│      Another description with trailing text.",
            ]
        )
        self.assertEqual([], discovery.validate(text, self.root))

    def test_description_line_ending_in_entry_shape_is_not_a_name(self):
        text = "\n".join(
            [
                "│    mag-one",
                "│",
                "│      Long description that ends with a box │    mag-ghost",
                "│",
                "│    mag-two",
                "│",
                "│      Another description.",
            ]
        )
        self.assertEqual([], discovery.validate(text, self.root))

    def test_description_mentioning_skipped_is_not_a_skip_notice(self):
        text = "\n".join(
            [
                "│    mag-one",
                "│",
                "│      Skipped migrations are reported to the operator.",
                "│",
                "│    mag-two",
                "│",
                "│      Another description.",
            ]
        )
        self.assertEqual([], discovery.validate(text, self.root))

    def test_ansi_sequences_are_ignored(self):
        text = "\x1b[?25l" + listing("mag-one", "mag-two") + "\x1b[?25h"
        self.assertEqual([], discovery.validate(text, self.root))

    def test_repository_skills_are_counted_from_disk(self):
        self.assertEqual(37, len(discovery.disk_skills(REPO)))


if __name__ == "__main__":
    unittest.main()
