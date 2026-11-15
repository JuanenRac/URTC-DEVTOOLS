# =============================================================================
# URTC-DEVTOOLS - tests/test_fleet_simulation.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A virtual family takes the set, is broken in every way the lock and the workflow check know, and heals (evidence: simulator). Folders are temporary."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import devtools_set  # noqa: E402
import fleet_simulation as fs  # noqa: E402

DOCS_SOURCE = ROOT.parent / "URTC-DOCS" / "src"
SHARED = "tools/build_test.py"


class FleetCase(unittest.TestCase):
    """The family is built once; every test starts by undoing the faults of the one before."""

    _folder: tempfile.TemporaryDirectory
    _fleet: fs.VirtualFleet

    @classmethod
    def setUpClass(cls):
        cls._folder = tempfile.TemporaryDirectory()
        cls._fleet = fs.VirtualFleet(Path(cls._folder.name))

    @classmethod
    def tearDownClass(cls):
        cls._folder.cleanup()

    def setUp(self):
        self.fleet = self._fleet
        self.fleet.reset()


class TakingTheSet(FleetCase):
    def test_a_family_that_just_took_the_set_is_clean(self):
        self.assertEqual(self.fleet.check_all(), {})
        self.assertEqual(self.fleet.nightly(), [])

    def test_every_repository_carries_every_file_of_the_set_with_its_own_name(self):
        for name in self.fleet.names:
            for relative in devtools_set.shared_files():
                self.assertEqual((self.fleet.repo(name) / relative).read_text(encoding="utf-8"), devtools_set.render_for(name, relative), (name, relative))

    def test_the_lock_names_the_version_of_the_set_and_the_hash_of_each_copy(self):
        lock = json.loads((self.fleet.repo("URTC-TESTER") / fs.LOCK_FILE).read_text(encoding="utf-8"))
        self.assertEqual((lock["schema"], lock["source"], lock["version"]), (1, "URTC-DEVTOOLS", devtools_set.version()))
        self.assertEqual(sorted(lock["files"]), devtools_set.shared_files())
        self.assertEqual(lock["files"][SHARED], fs.digest(devtools_set.render_for("URTC-TESTER", SHARED)))

    def test_the_hash_differs_between_repositories_where_the_name_of_the_repository_is_written(self):
        hashes = {name: json.loads((self.fleet.repo(name) / fs.LOCK_FILE).read_text(encoding="utf-8"))["files"] for name in self.fleet.names}
        named = [r for r in devtools_set.shared_files() if devtools_set.PLACEHOLDER in devtools_set.canonical_text(r)]
        self.assertTrue(named, "some shared file must carry the name of its repository")
        for relative in named:
            self.assertNotEqual(hashes["URTC"][relative], hashes["URTC-TESTER"][relative], relative)

    def test_taking_the_set_twice_changes_nothing(self):
        before = (self.fleet.repo("URTC") / fs.LOCK_FILE).read_bytes()
        self.fleet.take_set("URTC")
        self.assertEqual((self.fleet.repo("URTC") / fs.LOCK_FILE).read_bytes(), before)

    def test_the_demonstration_passes(self):
        self.assertEqual(fs.demonstration(), [])


class FindingTheFaults(FleetCase):
    def test_a_hand_edit_is_found_in_that_repository_only(self):
        self.fleet.hand_edit("URTC-GATEWAY", SHARED)
        found = self.fleet.check_all()
        self.assertEqual(list(found), ["URTC-GATEWAY"])
        self.assertEqual(found["URTC-GATEWAY"], [f"{SHARED}: edited after the set was taken (it differs from the lock)"])

    def test_a_deleted_copy_is_found(self):
        self.fleet.delete("URTC", "tools/pretty_run.py")
        self.assertEqual(self.fleet.check("URTC"), ["tools/pretty_run.py: in the lock but missing"])

    def test_a_shared_file_the_lock_does_not_list_is_found(self):
        self.fleet.drop_from_lock("URTC-COMMON", "test.sh")
        self.assertEqual(self.fleet.check("URTC-COMMON"), ["test.sh: a shared file that the lock does not list"])

    def test_a_copy_checked_out_with_windows_line_endings_is_not_a_fault(self):
        self.fleet.to_crlf("URTC", SHARED)
        self.assertEqual(self.fleet.check("URTC"), [])

    def test_a_lock_that_cannot_be_read_is_reported_whatever_is_wrong_with_it(self):
        for how in ("json", "schema", "files"):
            with self.subTest(how=how):
                self.fleet.take_set("URTC-COMMON")
                self.fleet.break_lock("URTC-COMMON", how)
                self.assertEqual(self.fleet.check("URTC-COMMON"), [f"{fs.LOCK_FILE} cannot be read (schema 1 expected)"])

    def test_a_repository_without_a_lock_is_not_an_error_yet(self):
        self.fleet.remove_lock("URTC-COMMON")
        self.assertEqual(self.fleet.check("URTC-COMMON"), [])

    def test_a_new_version_of_the_set_leaves_every_repository_behind_until_it_takes_it(self):
        self.fleet.publish_set("9.9.9")
        self.assertEqual(set(self.fleet.check_all()), set(self.fleet.names))
        self.assertIn("9.9.9", self.fleet.check("URTC")[0])
        self.fleet.take_set("URTC")
        self.assertEqual(self.fleet.check("URTC"), [])
        self.assertEqual(len(self.fleet.check_all()), len(self.fleet.names) - 1)

    def test_several_faults_at_once_are_all_reported_and_taking_the_set_heals_them_all(self):
        self.fleet.hand_edit("URTC", SHARED)
        self.fleet.delete("URTC", "test.bat")
        self.fleet.drop_from_lock("URTC", "test.sh")
        self.assertEqual(len(self.fleet.check("URTC")), 3)
        self.fleet.take_set("URTC")
        self.assertEqual(self.fleet.check("URTC"), [])


class TheWorkflowCheck(FleetCase):
    def test_the_workflows_of_a_clean_family_pass_even_in_strict_mode(self):
        code, lines = self.fleet.workflows()
        self.assertEqual(code, 0)
        self.assertTrue(lines[-1].startswith("WORKFLOW_TEMPLATES=PASS"), lines)

    def test_an_action_that_is_not_pinned_to_a_hash_is_a_security_finding_and_a_drift(self):
        self.fleet.unpin_action("URTC-TESTER")
        code, lines = self.fleet.workflows()
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith("SECURITY URTC-TESTER/ci.yml") and "not pinned" in line for line in lines), lines)
        self.assertTrue(any(line.startswith("DRIFT ci.yml") for line in lines), lines)

    def test_a_workflow_on_pull_request_target_is_a_security_finding(self):
        self.fleet.run_on_pull_request_target("URTC-GATEWAY")
        code, lines = self.fleet.workflows()
        self.assertEqual(code, 1)
        self.assertTrue(any("runs on pull_request_target" in line for line in lines), lines)

    def test_the_nightly_report_joins_the_lock_problems_and_the_workflow_findings(self):
        self.fleet.hand_edit("URTC", SHARED)
        self.fleet.unpin_action("URTC-TESTER")
        report = self.fleet.nightly()
        self.assertTrue(any(line.startswith("URTC: ") for line in report), report)
        self.assertTrue(any(line.startswith("SECURITY ") for line in report), report)


@unittest.skipUnless((DOCS_SOURCE / "urtc_docs" / "devtools_lock.py").is_file(), "URTC-DOCS is not next to this repository")
class SameVerdictAsTheChecker(FleetCase):
    """The lock check of the simulation and the one that URTC-DOCS runs every night must agree on the same virtual family."""

    def setUp(self):
        super().setUp()
        sys.path.insert(0, str(DOCS_SOURCE))
        import urtc_docs.devtools_lock as real  # noqa: E402

        self.real = real

    def real_check(self, name):
        return self.real.check_repo(self.fleet.repo(name), self.fleet.files, self.fleet.set_version)

    def test_both_agree_on_every_scenario(self):
        scenarios = [
            lambda: None,
            lambda: self.fleet.hand_edit("URTC", SHARED),
            lambda: self.fleet.delete("URTC", "test.bat"),
            lambda: self.fleet.drop_from_lock("URTC", "test.sh"),
            lambda: self.fleet.to_crlf("URTC", SHARED),
            lambda: self.fleet.break_lock("URTC", "json"),
            lambda: self.fleet.publish_set("9.9.9"),
            lambda: self.fleet.remove_lock("URTC"),
        ]
        for index, scenario in enumerate(scenarios):
            with self.subTest(scenario=index):
                self.fleet.reset()
                scenario()
                self.assertEqual(sorted(self.fleet.check("URTC")), sorted(self.real_check("URTC")))


if __name__ == "__main__":
    unittest.main()
