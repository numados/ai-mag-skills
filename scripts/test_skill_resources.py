"""Regression checks for independently distributable skill folders."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("skill_resources", REPO / "scripts/sync-skill-resources.py")
resources = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resources)


class SkillResourcesTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        shutil.copytree(REPO / "skills", self.root / "skills")
        shutil.copyfile(REPO / "LICENSE", self.root / "LICENSE")

    def test_each_bundled_skill_resolves_its_own_references_and_license(self):
        self.assertEqual([], resources.sync_resources(self.root))
        self.assertEqual([], resources.validate_local_references(self.root))
        license_text = (self.root / "LICENSE").read_bytes()
        for skill in resources.skill_directories(self.root):
            with self.subTest(skill=skill.name):
                self.assertEqual(license_text, (skill / "LICENSE").read_bytes())

    def test_check_reports_stale_copy_without_repairing_it(self):
        resources.sync_resources(self.root)
        _, destination = next(resources.resource_copies(self.root))
        destination.write_text("stale distribution copy\n", encoding="utf-8")
        self.assertTrue(resources.sync_resources(self.root, check=True))
        self.assertEqual("stale distribution copy\n", destination.read_text())

    def test_owner_change_is_propagated_to_all_its_copies(self):
        resources.sync_resources(self.root)
        source, _ = next(resources.resource_copies(self.root))
        source.write_text(source.read_text() + "\nOwner update.\n", encoding="utf-8")
        self.assertTrue(resources.sync_resources(self.root, check=True))
        self.assertEqual([], resources.sync_resources(self.root))
        for owner, destination in resources.resource_copies(self.root):
            if owner == source:
                self.assertTrue(destination.read_text().endswith(source.read_text()))
        self.assertEqual([], resources.sync_resources(self.root, check=True))

    def test_check_reports_missing_license_without_creating_it(self):
        resources.sync_resources(self.root)
        # A new skill has no generated license until a maintainer synchronizes it.
        skill = self.root / "skills/test/new-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# New skill\n", encoding="utf-8")
        self.assertTrue(resources.sync_resources(self.root, check=True))
        self.assertFalse((skill / "LICENSE").exists())

    def test_sync_is_idempotent(self):
        resources.sync_resources(self.root)
        before = {dest: dest.stat().st_mtime_ns for _, dest in resources.resource_copies(self.root)}
        self.assertEqual([], resources.sync_resources(self.root))
        self.assertEqual(before, {dest: dest.stat().st_mtime_ns for dest in before})

    def test_sibling_reference_is_rejected_even_when_target_exists(self):
        skill = resources.skill_directories(self.root)[0]
        sibling = next(path for path in resources.skill_directories(self.root) if path.parent == skill.parent and path != skill)
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n[Sibling](../{sibling.name}/SKILL.md)\n")
        self.assertTrue(any("reference leaves skill" in error for error in resources.validate_local_references(self.root)))

    def test_missing_inline_reference_is_rejected(self):
        skill = resources.skill_directories(self.root)[0]
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("\nRead `references/not-bundled.md`.\n")
        self.assertTrue(any("not-bundled.md" in error for error in resources.validate_local_references(self.root)))

    def test_external_links_and_page_anchors_are_not_local_dependencies(self):
        resources.sync_resources(self.root)
        skill = resources.skill_directories(self.root)[0]
        with (skill / "SKILL.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[Official docs](https://example.com/guide) [Section](#section)\n")
        self.assertEqual([], resources.validate_local_references(self.root))


if __name__ == "__main__":
    unittest.main()
