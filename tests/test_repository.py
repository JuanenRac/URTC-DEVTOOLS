# =============================================================================
# URTC-DEVTOOLS - tests/test_repository.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The repository as a member of the family, and the comparison with URTC-DOCS when that is next to this one."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import devtools_set  # noqa: E402

DOCS = ROOT.parent / "URTC-DOCS"
README_FILES = ("README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md")


class Manifest(unittest.TestCase):
    def test_the_manifest_is_the_one_of_a_scaffolding_tool_with_host_tests(self):
        manifest = json.loads((ROOT / "urtc.project.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "URTC-DEVTOOLS")
        self.assertEqual(manifest["ecosystem"], "URTC")
        self.assertEqual((manifest["maturity"], manifest["evidence"]), ("scaffolding", "host-test"))
        self.assertIn(manifest["role"], {"api", "ui", "cli", "firmware", "library", "service", "tool", "docs", "node"})
        self.assertIn(manifest["deployment_target"], {"cm5", "user-pc", "mobile", "wearable", "dev-server", "mcu"})

    def test_the_changelog_names_the_version(self):
        manifest = json.loads((ROOT / "urtc.project.json").read_text(encoding="utf-8"))
        self.assertIn(f"## [{manifest['version']}]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_the_tests_badge_of_the_readme_is_the_number_of_tests_that_exist(self):
        badge = re.search(r"badge/Tests-(\d+)", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(badge)
        count = sum(len(re.findall(r"(?m)^    def test_", path.read_text(encoding="utf-8"))) for path in (ROOT / "tests").glob("test_*.py"))
        self.assertEqual(int(badge.group(1)), count, "update the Tests badge and the At a glance table of the eight READMEs")


class Documents(unittest.TestCase):
    def test_the_eight_readmes_state_the_same_version(self):
        manifest = json.loads((ROOT / "urtc.project.json").read_text(encoding="utf-8"))
        for name in README_FILES:
            self.assertIn(f"`{manifest['version']}`", (ROOT / name).read_text(encoding="utf-8"), name)


@unittest.skipUnless((DOCS / "template" / "eh3d-repo-template").is_dir(), "URTC-DOCS is not next to this repository")
class WithTheDocsRepository(unittest.TestCase):
    """While URTC-DOCS still holds its own template, the two must be the same set; this fails (locally, not in CI) when one fell behind."""

    def test_files_is_the_template_of_urtc_docs(self):
        template = DOCS / "template" / "eh3d-repo-template"
        mine = set(devtools_set.shared_files())
        theirs = {p.relative_to(template).as_posix() for p in template.rglob("*") if p.is_file() and p.name != "TEMPLATE.md"}
        self.assertEqual(mine, theirs)
        differing = [relative for relative in sorted(mine)
                     if devtools_set.canonical_text(relative) != (template / relative).read_bytes().decode("utf-8").replace("\r\n", "\n")]
        self.assertEqual(differing, [], "files/ and the template of URTC-DOCS differ: take the newer one into the other and raise the version")


if __name__ == "__main__":
    unittest.main()
