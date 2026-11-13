"""Regression checks for the shared skill-metadata reader and catalog validator.

The old check-skills.sh parser read ``description:`` with a regex that only
matched the value on the header line itself.  For the folded block scalars used
by ``mag-ai-writing`` (``>-``) and ``mag-minto-pyramid`` (``>``) that produced
the block *marker* (``>-`` / ``>``) instead of the block *content*.  These tests
pin the fixed behavior: block content is folded into text, the marker is never
returned, and empty blocks are rejected.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("skill_catalog", REPO / "scripts/skill_catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)

class FrontmatterParsingTests(unittest.TestCase):
    def parse(self, text):
        return catalog.parse_frontmatter(text, "<fixture>")

    def test_plain_description(self):
        fm = self.parse("---\nname: mag-foo\ndescription: Do the thing.\n---\n")
        self.assertEqual("mag-foo", fm["name"])
        self.assertEqual("Do the thing.", fm["description"])

    def test_plain_description_trims_whitespace(self):
        fm = self.parse("---\nname: mag-foo\ndescription:    padded text   \n---\n")
        self.assertEqual("padded text", fm["description"])

    def test_single_quoted_description(self):
        fm = self.parse("---\nname: mag-foo\ndescription: 'it''s quoted'\n---\n")
        self.assertEqual("it's quoted", fm["description"])

    def test_double_quoted_description(self):
        fm = self.parse('---\nname: mag-foo\ndescription: "say \\"hi\\" and\\nbye"\n---\n')
        self.assertEqual('say "hi" and\nbye', fm["description"])

    def test_folded_strip_chomping(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: >-\n  first line\n  second line\n---\n"
        )
        self.assertEqual("first line second line", fm["description"])

    def test_folded_clip_chomping(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: >\n  first line\n  second line\n---\n"
        )
        self.assertEqual("first line second line\n", fm["description"])

    def test_folded_blank_line_becomes_single_break(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: >\n  first\n\n  second\n---\n"
        )
        self.assertEqual("first\nsecond\n", fm["description"])

    def test_literal_strip_chomping(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: |-\n  line one\n  line two\n---\n"
        )
        self.assertEqual("line one\nline two", fm["description"])

    def test_literal_clip_chomping(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: |\n  line one\n  line two\n---\n"
        )
        self.assertEqual("line one\nline two\n", fm["description"])

    def test_block_yields_content_not_marker(self):
        # The original regex parser returned ">-" / ">" here; the value must be text.
        fm = self.parse("---\nname: mag-foo\ndescription: >-\n  hello world\n---\n")
        self.assertEqual("hello world", fm["description"])
        self.assertNotIn(">-", fm["description"])
        self.assertNotEqual(">", fm["description"])

    def test_empty_block_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("name: mag-foo\ndescription: >\n"), self.root
            )

    def test_block_only_whitespace_is_empty(self):
        fm = self.parse("---\nname: mag-foo\ndescription: >\n   \n---\n")
        self.assertEqual("", catalog.normalize_whitespace(fm["description"]))

    def test_missing_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("name: mag-foo\n"), self.root
            )

    def test_empty_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("name: mag-foo\ndescription:\n"), self.root
            )

    def test_missing_name_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("description: text\n"), self.root
            )

    def test_invalid_name_character_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("name: Mag-Foo\ndescription: text\n"), self.root
            )

    def test_name_without_prefix_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill("name: foo\ndescription: text\n"), self.root
            )

    def test_optional_scalar_fields(self):
        fm = self.parse(
            "---\n"
            "name: mag-foo\n"
            "description: Do the thing.\n"
            "license: Complete terms in LICENSE.txt\n"
            "compatibility: Requires a host with filesystem access.\n"
            "---\n"
        )
        self.assertEqual("Complete terms in LICENSE.txt", fm["license"])
        self.assertEqual("Requires a host with filesystem access.", fm["compatibility"])

    def test_flat_metadata_mapping(self):
        fm = self.parse(
            "---\n"
            "name: mag-foo\n"
            "description: Do the thing.\n"
            "metadata:\n"
            "  stability: stable\n"
            "  supported-harnesses: pi, codex\n"
            "---\n"
        )
        self.assertEqual(
            {"stability": "stable", "supported-harnesses": "pi, codex"},
            fm["metadata"],
        )

    def test_empty_metadata_mapping(self):
        self.assertEqual(
            {},
            self.parse(
                "---\nname: mag-foo\ndescription: Do the thing.\nmetadata: {}\n---\n"
            )["metadata"],
        )

    def test_nested_metadata_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "  limits:\n"
                "    tokens: 100\n"
                "---\n"
            )

    def test_metadata_collection_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "  tags: [one, two]\n"
                "---\n"
            )

    def test_duplicate_metadata_key_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "  stability: stable\n"
                "  stability: experimental\n"
                "---\n"
            )

    def test_plain_scalar_with_mapping_colon_fails(self):
        # YAML reads "Optional: needs a host" as a nested mapping; the client
        # then skips the skill instead of failing the build.
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "compatibility: Optional: needs a host\n"
                "---\n"
            )

    def test_quoted_scalar_with_mapping_colon_is_allowed(self):
        fm = self.parse(
            "---\n"
            "name: mag-foo\n"
            "description: Do the thing.\n"
            'compatibility: "Optional: needs a host"\n'
            "---\n"
        )
        self.assertEqual("Optional: needs a host", fm["compatibility"])

    def test_metadata_after_flow_empty_map_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata: {}\n"
                "  stability: stable\n"
                "---\n"
            )

    def test_tab_indented_metadata_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "\tstability: stable\n"
                "---\n"
            )

    def test_tab_indented_block_scalar_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: >\n"
                "\tline one\n"
                "---\n"
            )

    def test_empty_metadata_value_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "  stability:\n"
                "---\n"
            )

    def test_bare_metadata_key_fails(self):
        # YAML reads a bare ``metadata:`` as null, not as an empty mapping.
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: Do the thing.\nmetadata:\n---\n")

    def test_quoted_empty_metadata_value_is_allowed(self):
        fm = self.parse(
            "---\n"
            "name: mag-foo\n"
            "description: Do the thing.\n"
            "metadata:\n"
            "  note: ''\n"
            "---\n"
        )
        self.assertEqual({"note": ""}, fm["metadata"])

    def test_unquoted_numeric_metadata_value_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\n"
                "name: mag-foo\n"
                "description: Do the thing.\n"
                "metadata:\n"
                "  priority: 1\n"
                "---\n"
            )

    def test_quoted_numeric_metadata_value_is_allowed(self):
        fm = self.parse(
            "---\n"
            "name: mag-foo\n"
            "description: Do the thing.\n"
            "metadata:\n"
            "  priority: '1'\n"
            "---\n"
        )
        self.assertEqual({"priority": "1"}, fm["metadata"])

    def test_empty_compatibility_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill(
                    "name: mag-foo\ndescription: A test skill.\ncompatibility: ''\n"
                ),
                self.root,
            )

    def test_empty_license_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill(
                    "name: mag-foo\ndescription: A test skill.\nlicense:\n"
                ),
                self.root,
            )

    def test_yaml_non_string_scalars_fail(self):
        for value in ("0x10", "1e3", "0b1010", "1_000", "2026-11-08", "+1.5"):
            with self.subTest(value=value):
                with self.assertRaises(catalog.CatalogError):
                    self.parse(
                        "---\nname: mag-foo\ndescription: " + value + "\n---\n"
                    )

    def test_plain_scalar_with_comment_indicator_fails(self):
        # YAML would truncate the value at the comment.
        with self.assertRaises(catalog.CatalogError):
            self.parse(
                "---\nname: mag-foo\ndescription: Fixes the bug #123 tracked upstream.\n---\n"
            )

    def test_quoted_comment_indicator_is_allowed(self):
        fm = self.parse(
            "---\nname: mag-foo\ndescription: 'Fixes the bug #123 tracked upstream.'\n---\n"
        )
        self.assertEqual("Fixes the bug #123 tracked upstream.", fm["description"])

    def test_description_length_limit_applies_to_parsed_value(self):
        # Quoted whitespace counts: a client stores it.
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill(
                    "name: mag-foo\ndescription: 'x" + ("y" * 1024) + "'\n"
                ),
                self.root,
            )

    def test_clip_chomped_description_counts_its_newline(self):
        exact = "d" * 1024
        ok = self.write_skill("name: mag-foo\ndescription: >-\n  " + exact + "\n")
        catalog.read_skill_metadata(ok, self.root)
        overflow = self.write_skill(
            "name: mag-foo\ndescription: >\n  " + exact + "\n", name="mag-bar"
        )
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(overflow, self.root)

    def test_duplicate_name_key_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\nname: mag-bar\ndescription: x\n---\n")

    def test_duplicate_description_key_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: x\ndescription: y\n---\n")

    def test_unclosed_frontmatter_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: x\n")

    def test_missing_open_marker_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("name: mag-foo\ndescription: x\n---\n")

    def test_unsupported_key_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: x\nversion: 1\n---\n")

    def test_description_length_limit_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill(
                    "name: mag-foo\ndescription: " + ("x" * 1025) + "\n"
                ),
                self.root,
            )

    def test_compatibility_length_limit_fails(self):
        with self.assertRaises(catalog.CatalogError):
            catalog.read_skill_metadata(
                self.write_skill(
                    "name: mag-foo\n"
                    "description: A test skill.\n"
                    "compatibility: " + ("x" * 501) + "\n"
                ),
                self.root,
            )

    def test_flow_list_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: [a, b]\n---\n")

    def test_block_sequence_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: - item\n---\n")

    def test_indentation_indicator_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: >2\n  text\n---\n")

    def test_unterminated_quote_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse('---\nname: mag-foo\ndescription: "unclosed\n---\n')

    def test_trailing_double_quoted_content_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse('---\nname: mag-foo\ndescription: "ok" trailing\n---\n')

    def test_trailing_single_quoted_content_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: 'ok' trailing\n---\n")

    def test_multiline_plain_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: first\n  second\n---\n")

    def test_null_scalar_description_fails(self):
        with self.assertRaises(catalog.CatalogError):
            self.parse("---\nname: mag-foo\ndescription: null\n---\n")

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def write_skill(self, frontmatter, name="mag-foo", category="test"):
        directory = self.root / "skills" / category / name
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "SKILL.md"
        path.write_text("---\n" + frontmatter + "---\n# Body\n", encoding="utf-8")
        return path


class CatalogTests(unittest.TestCase):
    def test_all_current_skills_have_nonempty_normalized_descriptions(self):
        rows = catalog.catalog_rows(REPO)
        self.assertEqual(41, len(rows))
        for name, rel, description in rows:
            with self.subTest(name=name):
                self.assertTrue(name.startswith("mag-"), name)
                self.assertTrue(description.strip(), name)
                self.assertEqual(name, rel.split("/")[-2])

    def test_block_descriptions_contain_text_not_markers(self):
        rows = {name: description for name, _rel, description in catalog.catalog_rows(REPO)}
        for name in ("mag-ai-writing", "mag-minto-pyramid"):
            with self.subTest(name=name):
                self.assertGreater(len(rows[name]), 40)
                self.assertNotIn(rows[name], (">", ">-", "|", "|-", ">+", "|+"))

    def test_fresh_catalog_matches_metadata_reader(self):
        expected = []
        for path in catalog.skill_paths(REPO):
            name, description = catalog.read_skill_metadata(path, REPO)
            expected.append(
                (name, path.relative_to(REPO).as_posix(), catalog.normalize_whitespace(description))
            )
        expected.sort(key=lambda row: row[0])
        self.assertEqual(expected, catalog.catalog_rows(REPO))

    def test_repository_catalog_is_valid(self):
        self.assertEqual([], catalog.validate_catalog(REPO))

    def test_manifest_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_skill(root, "mag-foo", "A test skill.")
            self.write_manifest(root, ["./skills/test/mag-other"])
            self.write_readme(root, "skills/test/mag-foo/SKILL.md\n")
            errors = catalog.validate_catalog(root)
            self.assertTrue(any("plugin.json" in e for e in errors), errors)

    def test_manifest_entry_missing_skill_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_skill(root, "mag-foo", "A test skill.")
            self.write_manifest(root, ["./skills/test/mag-foo", "./skills/test/mag-missing"])
            self.write_readme(root, "skills/test/mag-foo/SKILL.md\n")
            errors = catalog.validate_catalog(root)
            self.assertTrue(any("missing SKILL.md" in e for e in errors), errors)

    def test_readme_missing_link_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_skill(root, "mag-foo", "A test skill.")
            self.write_manifest(root, ["./skills/test/mag-foo"])
            self.write_readme(root, "no skill links here\n")
            errors = catalog.validate_catalog(root)
            self.assertTrue(any("missing link" in e for e in errors), errors)

    def write_skill(self, root, name, description):
        directory = root / "skills" / "test" / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: {description}\n---\n# Body\n",
            encoding="utf-8",
        )

    def write_manifest(self, root, skills):
        directory = root / ".claude-plugin"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "plugin.json").write_text(
            json.dumps({"skills": skills}), encoding="utf-8"
        )

    def write_readme(self, root, text):
        (root / "README.md").write_text(text, encoding="utf-8")


class EvalValidationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def write_skill(self, name="mag-foo"):
        directory = self.root / "skills" / "test" / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: A test skill.\n---\n# Body\n",
            encoding="utf-8",
        )

    def write_eval(self, data, category="test", name="mag-foo"):
        directory = self.root / "evals" / category / name
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "evals.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def make_eval(self, **overrides):
        data = {
            "skill_name": "mag-foo",
            "evals": [
                {"id": 1, "prompt": "Do it.", "expected_output": "Done.", "should_trigger": True, "files": []},
            ],
        }
        data.update(overrides)
        return data

    def test_valid_eval_is_clean(self):
        self.write_skill()
        self.write_eval(self.make_eval())
        self.assertEqual([], catalog.validate_evals(self.root))

    def test_eval_file_relative_and_repo_relative_resolve(self):
        self.write_skill()
        directory = self.root / "evals" / "test" / "mag-foo"
        (directory / "fixtures").mkdir(parents=True)
        (directory / "fixtures" / "local.md").write_text("local", encoding="utf-8")
        (directory / "fixtures" / "repo.md").write_text("repo", encoding="utf-8")

        # eval-file-relative convention
        resolved = catalog.resolve_eval_file(self.root, directory, "fixtures/local.md")
        self.assertEqual((directory / "fixtures" / "local.md").resolve(), resolved)
        # repository-relative convention
        resolved = catalog.resolve_eval_file(
            self.root, directory, "evals/test/mag-foo/fixtures/repo.md"
        )
        self.assertEqual((directory / "fixtures" / "repo.md").resolve(), resolved)

    def test_eval_missing_file_is_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": ["fixtures/nope.md"]},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("missing files entry" in e for e in errors), errors)

    def test_eval_outside_file_is_reported(self):
        self.write_skill()
        directory = self.root / "evals" / "test"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "outside.md").write_text("outside", encoding="utf-8")
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": ["../outside.md"]},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("escapes its eval directory" in e for e in errors), errors)

    def test_eval_absolute_file_is_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": [str(self.root / "secret.md")]},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("absolute files entry" in e for e in errors), errors)

    def test_eval_ambiguous_file_is_reported(self):
        self.write_skill()
        eval_dir = self.root / "evals" / "test" / "mag-foo"
        (eval_dir / "fixtures").mkdir(parents=True)
        (eval_dir / "fixtures" / "a.md").write_text("eval-relative", encoding="utf-8")
        (self.root / "fixtures").mkdir(parents=True)
        (self.root / "fixtures" / "a.md").write_text("repo-relative", encoding="utf-8")
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": ["fixtures/a.md"]},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("ambiguous" in e for e in errors), errors)

    def test_eval_duplicate_ids_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": []},
            {"id": 1, "prompt": "q", "expected_output": "f", "files": []},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("duplicate id" in e for e in errors), errors)

    def test_eval_missing_should_trigger_is_allowed_but_consistent(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "files": []},
            {"id": 2, "prompt": "q", "expected_output": "f", "files": []},
        ]))
        self.assertEqual([], catalog.validate_evals(self.root))
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "should_trigger": True, "files": []},
            {"id": 2, "prompt": "q", "expected_output": "f", "files": []},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("every eval or none" in e for e in errors), errors)

    def test_eval_non_boolean_should_trigger_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "expected_output": "e", "should_trigger": "yes", "files": []},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("should_trigger" in e for e in errors), errors)

    def test_eval_missing_prompt_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "expected_output": "e", "files": []},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("missing or empty prompt" in e for e in errors), errors)

    def test_eval_missing_expected_output_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(evals=[
            {"id": 1, "prompt": "p", "files": []},
        ]))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("missing or empty expected_output" in e for e in errors), errors)

    def test_eval_unknown_skill_name_reported(self):
        self.write_skill()
        self.write_eval(self.make_eval(skill_name="mag-nonexistent"))
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("does not correspond to a skill" in e for e in errors), errors)

    def test_eval_bad_json_reported(self):
        self.write_skill()
        path = self.write_eval(self.make_eval())
        path.write_text("{not json", encoding="utf-8")
        errors = catalog.validate_evals(self.root)
        self.assertTrue(any("cannot parse JSON" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
