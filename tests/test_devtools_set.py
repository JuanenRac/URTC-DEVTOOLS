# =============================================================================
# URTC-DEVTOOLS - tests/test_devtools_set.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared set: what files/ holds, how it renders for a repository, and that this repository carries it unedited."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import devtools_set  # noqa: E402

# the files every repository of the family carries as the same copy (the list of URTC-DOCS: src/urtc_docs/drift.py)
EXPECTED = {
    ".github/workflows/dashboard-dispatch.yml",
    ".github/actions/urtc-baseline/action.yml",
    "bump_manifest_version.py",
    "tools/_doc_policy.py",
    "tools/_readme_parity.py",
    "tools/_readme_svg.py",
    "tools/_tracked_names.py",
    "tools/make_architecture.py",
    "tools/make_structure.py",
    "tools/pretty_run.py",
    "tools/run_host_tests.py",
    "tools/status_lights.py",
    "tools/universal_readme_check.py",
    "test.sh",
    "test.bat",
}


class TheSet(unittest.TestCase):
    def test_the_canonical_files_are_the_ones_every_repository_carries(self):
        self.assertEqual(set(devtools_set.shared_files()), EXPECTED)

    def test_the_canonical_files_have_newlines_only_and_no_name_of_a_repository_but_the_placeholder(self):
        for relative in devtools_set.shared_files():
            raw = (ROOT / "files" / relative).read_bytes()
            self.assertNotIn(b"\r\n", raw, relative)
            self.assertNotIn(b"URTC-DEVTOOLS", raw, relative)

    def test_the_python_files_of_the_set_are_valid_python(self):
        for relative in devtools_set.shared_files():
            if relative.endswith(".py"):
                ast.parse(devtools_set.canonical_text(relative), relative)

    def test_a_file_renders_with_the_name_of_the_repository(self):
        text = devtools_set.render_for("URTC-EXAMPLE", "tools/_doc_policy.py")
        self.assertNotIn("<REPO>", text)
        self.assertIn("URTC-EXAMPLE", text)

    def test_compiled_files_left_by_a_run_are_not_part_of_the_set(self):
        with tempfile.TemporaryDirectory() as folder:
            files = Path(folder) / "files"
            (files / "tools" / "__pycache__").mkdir(parents=True)
            (files / "tools" / "x.py").write_text("x = 1\n", encoding="utf-8")
            (files / "tools" / "__pycache__" / "x.cpython-312.pyc").write_bytes(b"\xcb\r\n")
            self.assertEqual(devtools_set.shared_files(files), ["tools/x.py"])

    def test_this_repository_carries_every_file_of_the_set_unedited(self):
        self.assertEqual(devtools_set.check_own_copies(), [])

    def test_an_edited_copy_is_found(self):
        with tempfile.TemporaryDirectory() as folder:
            copy = Path(folder) / "URTC-COPY"
            for relative in devtools_set.shared_files():
                target = copy / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(devtools_set.render_for(copy.name, relative), encoding="utf-8", newline="")
                (copy / "files" / relative).parent.mkdir(parents=True, exist_ok=True)
                (copy / "files" / relative).write_text(devtools_set.canonical_text(relative), encoding="utf-8", newline="")
            self.assertEqual(devtools_set.check_own_copies(copy), [])
            (copy / "tools" / "pretty_run.py").write_text("edited\n", encoding="utf-8")
            (copy / "bump_manifest_version.py").unlink()
            self.assertEqual(devtools_set.check_own_copies(copy), ["bump_manifest_version.py: missing", "tools/pretty_run.py: differs from files/tools/pretty_run.py"])

    def test_the_digest_ignores_the_line_endings(self):
        self.assertEqual(devtools_set.digest("a\r\nb\r\n"), devtools_set.digest("a\nb\n"))
        self.assertEqual(devtools_set.digest("a\n"), hashlib.sha256(b"a\n").hexdigest())

    def test_the_version_of_the_set_is_the_version_of_the_manifest_and_of_pyproject(self):
        manifest = json.loads((ROOT / "urtc.project.json").read_text(encoding="utf-8"))
        self.assertEqual(devtools_set.version(), manifest["version"])
        self.assertIn(f'version = "{manifest["version"]}"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    def test_the_commands(self):
        self.assertEqual(devtools_set.main(["check"]), 0)
        self.assertEqual(devtools_set.main(["list"]), 0)
        self.assertEqual(devtools_set.main(["nothing"]), 2)


class TheLockOfThisRepository(unittest.TestCase):
    """This repository takes the set like any other: its lock lists the files it carries with the hash they have, and the version of the set."""

    def test_the_lock_matches_the_files_and_the_version(self):
        lock_path = ROOT / devtools_set.LOCK_NAME
        self.assertTrue(lock_path.is_file(), "tools/devtools.lock.json is missing; run URTC-DOCS tools/sync_repo_tools.py --apply")
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(lock["schema"], 1)
        self.assertEqual(lock["source"], "URTC-DEVTOOLS")
        self.assertEqual(lock["version"], devtools_set.version())
        self.assertEqual(sorted(lock["files"]), devtools_set.shared_files())
        for relative, expected in lock["files"].items():
            actual = devtools_set.digest((ROOT / relative).read_bytes().decode("utf-8"))
            self.assertEqual(actual, expected, relative)


if __name__ == "__main__":
    unittest.main()
