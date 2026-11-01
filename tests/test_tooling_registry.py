# =============================================================================
# URTC-DEVTOOLS - tests/test_tooling_registry.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The registry of the tooling the families keep as the same file: its shape, its hashes and the comparison across families."""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import devtools_set  # noqa: E402
import tooling_registry  # noqa: E402


def entry(**changes):
    base = {
        "path": "tools/x.py", "kind": "identical", "in_set": False, "same_in": ["URTC", "HYDRA"], "reason": "because",
        "sources": {"URTC": {"repo": "URTC-DEVTOOLS", "path": "tools/x.py"}, "HYDRA": {"repo": "HYDRA-UMC-SDK", "path": "tools/x.py"}},
        "urtc_sha256": "",
    }
    base.update(changes)
    return base


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


class TheRegistryOfThisRepository(unittest.TestCase):
    def test_it_passes_its_own_check(self):
        data = tooling_registry.load()
        self.assertEqual(tooling_registry.check_own_side(data), [])

    def test_it_lists_every_file_of_the_set(self):
        listed = {e["path"] for e in tooling_registry.load()["files"] if e["in_set"]}
        self.assertEqual(listed, set(devtools_set.shared_files()))

    def test_a_changed_hash_is_found(self):
        data = copy.deepcopy(tooling_registry.load())
        data["files"][0]["urtc_sha256"] = "0" * 64
        self.assertTrue(any("hash in the registry" in p for p in tooling_registry.check_own_side(data)))

    def test_a_file_of_the_set_missing_from_the_registry_is_found(self):
        data = copy.deepcopy(tooling_registry.load())
        data["files"] = [e for e in data["files"] if e["path"] != "tools/pretty_run.py"]
        self.assertTrue(any("tools/pretty_run.py" in p and "not in the registry" in p for p in tooling_registry.check_own_side(data)))

    def test_every_entry_says_why(self):
        for e in tooling_registry.load()["files"]:
            self.assertTrue(e["reason"].strip(), e["path"])


class TheShape(unittest.TestCase):
    def test_a_good_entry_has_no_problem(self):
        self.assertEqual(tooling_registry.check_registry_shape({"files": [entry()]}), [])

    def test_the_problems_are_named(self):
        problems = tooling_registry.check_registry_shape({"files": [
            entry(kind="other"), entry(reason=""), entry(same_in=["URTC"]), entry(same_in=["URTC", "ARMOR"]),
        ]})
        text = "\n".join(problems)
        for expected in ("kind must be", "say why", "at least two", "ARMOR, which has no source", "listed twice"):
            self.assertIn(expected, text)


class TheComparison(unittest.TestCase):
    def workspace(self, urtc: str, hydra: str) -> Path:
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(folder, ignore_errors=True))
        write(folder / "URTC-DEVTOOLS" / "tools" / "x.py", urtc)
        write(folder / "HYDRA-UMC-SDK" / "tools" / "x.py", hydra)
        return folder

    def test_equal_texts_pass_whatever_the_line_endings_and_the_name_of_the_repository(self):
        folder = self.workspace("# URTC-DEVTOOLS tool\r\nprint(1)\r\n", "# HYDRA-UMC-SDK tool\nprint(1)\n")
        failures, notes, compared = tooling_registry.check_across({"files": [entry()]}, folder)
        self.assertEqual((failures, notes, compared), ([], [], 1))

    def test_different_texts_fail(self):
        failures, _, _ = tooling_registry.check_across({"files": [entry()]}, self.workspace("print(1)\n", "print(2)\n"))
        self.assertEqual(len(failures), 1)

    def test_a_banner_only_difference_passes_for_same_after_banner_and_fails_for_identical(self):
        folder = self.workspace("# URTC-DEVTOOLS - x\nprint(1)\n", "# HYDRA-UMC-SDK - x\nprint(1)\n")
        # the name of the repository is already ignored; a family name that is not the repository's own is what the banner rule covers
        write(folder / "HYDRA-UMC-SDK" / "tools" / "x.py", "# A.R.M.O.R. - x\nprint(1)\n")
        loose, _, _ = tooling_registry.check_across({"files": [entry(kind="same_after_banner")]}, folder)
        strict, _, _ = tooling_registry.check_across({"files": [entry()]}, folder)
        self.assertEqual((loose, len(strict)), ([], 1))

    def test_a_source_that_is_not_there_is_a_note_not_a_failure(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(folder, ignore_errors=True))
        write(folder / "URTC-DEVTOOLS" / "tools" / "x.py", "print(1)\n")
        failures, notes, compared = tooling_registry.check_across({"files": [entry()]}, folder)
        self.assertEqual((failures, len(notes), compared), ([], 1, 0))

    def test_the_carriers_of_a_family_are_counted(self):
        folder = self.workspace("print(1)\n", "print(1)\n")
        for name, text in (("HYDRA-UMC-A", "print(1)\n"), ("HYDRA-UMC-B", "print(9)\n"), ("HYDRA-UMC-C", None)):
            write(folder / name / "hydra-umc.project.json", "{}")
            if text is not None:
                write(folder / name / "tools" / "x.py", text)
        self.assertEqual(tooling_registry.carriers(folder, entry(), "HYDRA"), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()
