# =============================================================================
# URTC-DEVTOOLS - tests/test_tracked_names.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check that refuses versioned files named like an untranslated Windows path, on its own and over a real temporary git repository."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import _tracked_names as tracked  # noqa: E402

GIT = shutil.which("git")


class BadNamesTests(unittest.TestCase):
    def test_ordinary_names_pass(self):
        names = ["README.md", "src/main.c", "tools/a_b-c.py", "docs/Users guide.md", "images/screenshots/deck.png", "a/b/c/d.txt"]
        self.assertEqual(tracked.bad_names(names), [])

    def test_a_colon_anywhere_is_refused(self):
        self.assertEqual(tracked.bad_names(["a:b", "dir/file:1.txt"]), ["a:b", "dir/file:1.txt"])

    def test_the_character_a_drive_colon_turns_into_is_refused(self):
        name = "C\uf03a/Users/x/file.txt"
        self.assertEqual(tracked.bad_names([name]), [name])

    def test_a_folder_named_like_a_drive_is_refused_at_any_depth(self):
        for name in ("C/x.txt", "d\uf03a/x", "src/E\uf03a/y.txt", "z:/y"):
            with self.subTest(name=name):
                self.assertEqual(tracked.bad_names([name]), [name])

    def test_a_single_letter_folder_without_the_colon_is_fine_unless_it_is_c_at_the_root(self):
        self.assertEqual(tracked.bad_names(["src/C/x.txt", "d/x.txt"]), [])
        self.assertEqual(tracked.bad_names(["C/x.txt"]), ["C/x.txt"])

    def test_a_user_profile_folder_at_the_root_is_refused_in_any_case(self):
        for name in ("Users/juane/x.txt", "users/juane/x.txt", "Documents and Settings/x"):
            with self.subTest(name=name):
                self.assertEqual(tracked.bad_names([name]), [name])

    def test_a_user_folder_deeper_down_is_fine(self):
        self.assertEqual(tracked.bad_names(["docs/Users/x.md", "src/Documents and Settings/x"]), [])

    def test_the_order_is_kept_and_only_the_bad_ones_come_back(self):
        names = ["ok.txt", "C\uf03a/x", "also/ok.md", "Users/a", "z"]
        self.assertEqual(tracked.bad_names(names), ["C\uf03a/x", "Users/a"])

    def test_an_empty_list_has_nothing_bad(self):
        self.assertEqual(tracked.bad_names([]), [])


@unittest.skipIf(GIT is None, "git is not installed here")
class CheckTrackedNamesTests(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name)

    def git(self, *args):
        subprocess.run([GIT, *args], cwd=self.root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_a_folder_that_is_not_a_git_tree_cannot_be_listed(self):
        self.assertEqual(tracked.check_tracked_names(self.root), "could not list the versioned files")

    def test_a_clean_tree_has_no_message(self):
        self.git("init", "-q")
        (self.root / "a.txt").write_text("x", encoding="utf-8")
        self.git("add", "--", "a.txt")
        self.assertIsNone(tracked.check_tracked_names(self.root))

    def test_a_tree_with_nothing_versioned_has_no_message(self):
        self.git("init", "-q")
        self.assertIsNone(tracked.check_tracked_names(self.root))

    def test_a_versioned_file_inside_a_folder_called_users_is_reported_with_its_count_and_name(self):
        self.git("init", "-q")
        (self.root / "Users").mkdir()
        (self.root / "Users" / "x.txt").write_text("x", encoding="utf-8")
        (self.root / "fine.txt").write_text("x", encoding="utf-8")
        self.git("add", "--", "Users/x.txt", "fine.txt")
        message = tracked.check_tracked_names(self.root)
        self.assertIsNotNone(message)
        self.assertIn("(1:", message)
        self.assertIn("'Users/x.txt'", message)

    def test_only_versioned_files_count_not_files_lying_about(self):
        self.git("init", "-q")
        (self.root / "Users").mkdir()
        (self.root / "Users" / "x.txt").write_text("x", encoding="utf-8")
        self.assertIsNone(tracked.check_tracked_names(self.root))


if __name__ == "__main__":
    unittest.main()
