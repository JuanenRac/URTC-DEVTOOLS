# =============================================================================
# URTC-DEVTOOLS - tests/test_gap_cases.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Refusals and commands of the set tool, the registry and the workflow comparison that the other tests do not reach. Folders are temporary; nothing is written to
the repository."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import devtools_set  # noqa: E402
import tooling_registry  # noqa: E402
import workflow_templates as wt  # noqa: E402

SHA = "a" * 40


def entry(**changes):
    base = {
        "path": "tools/x.py", "kind": "identical", "in_set": False, "same_in": ["URTC", "HYDRA"], "reason": "because",
        "sources": {"URTC": {"repo": "URTC-DEVTOOLS", "path": "tools/x.py"}, "HYDRA": {"repo": "HYDRA-UMC-SDK", "path": "tools/x.py"}},
        "urtc_sha256": "",
    }
    base.update(changes)
    return base


def run(function, *args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = function(*args)
    return code, out.getvalue(), err.getvalue()


class TheSetCommands(unittest.TestCase):
    def test_list_names_every_file_with_its_hash(self):
        code, out, _ = run(devtools_set.main, ["list"])
        self.assertEqual(code, 0)
        self.assertIn("URTC-DEVTOOLS set version", out)
        for relative in devtools_set.shared_files():
            self.assertIn(relative, out)

    def test_no_argument_lists_too(self):
        self.assertEqual(run(devtools_set.main, [])[0], 0)

    def test_check_passes_on_this_repository(self):
        code, out, _ = run(devtools_set.main, ["check"])
        self.assertEqual(code, 0)
        self.assertIn("DEVTOOLS_SET=PASS", out)

    def test_help_exits_with_zero_and_an_unknown_command_with_two(self):
        for word in ("-h", "--help", "help"):
            self.assertEqual(run(devtools_set.main, [word])[0], 0)
        for word in ("bogus", "Check", ""):
            self.assertEqual(run(devtools_set.main, [word])[0], 2)

    def test_a_copy_that_is_missing_or_changed_is_a_problem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "files" / "tools").mkdir(parents=True)
            (root / "files" / "tools" / "a.py").write_bytes(b"print(1)\n")
            self.assertEqual(devtools_set.check_own_copies(root), ["tools/a.py: missing"])
            (root / "tools").mkdir()
            (root / "tools" / "a.py").write_bytes(b"changed\n")
            self.assertEqual(devtools_set.check_own_copies(root), ["tools/a.py: differs from files/tools/a.py"])
            (root / "tools" / "a.py").write_bytes(b"print(1)\r\n")
            self.assertEqual(devtools_set.check_own_copies(root), [])

    def test_the_hash_depends_on_the_text(self):
        self.assertEqual(devtools_set.digest("a"), devtools_set.digest("a"))
        self.assertNotEqual(devtools_set.digest("a"), devtools_set.digest("b"))
        self.assertNotEqual(devtools_set.digest("a"), devtools_set.digest("a\n"))


class TheRegistryShape(unittest.TestCase):
    def shape(self, *entries):
        return tooling_registry.check_registry_shape({"files": list(entries)})

    def test_a_good_entry_has_no_problem(self):
        self.assertEqual(self.shape(entry()), [])

    def test_the_same_path_twice_is_named(self):
        self.assertTrue(any("listed twice" in p for p in self.shape(entry(), entry())))

    def test_a_kind_outside_the_list_is_named(self):
        self.assertTrue(any("kind must be one of" in p for p in self.shape(entry(kind="other"))))
        self.assertTrue(any("kind must be one of" in p for p in self.shape({"path": "p", "reason": "r", "sources": {"URTC": {}}})))

    def test_a_missing_or_blank_reason_is_named(self):
        for reason in ("", "   ", None, 3):
            self.assertTrue(any("(reason)" in p for p in self.shape(entry(reason=reason))), reason)

    def test_the_urtc_source_is_required(self):
        for sources in ({}, {"HYDRA": {}}, None, "x"):
            self.assertTrue(any("URTC source is required" in p for p in self.shape(entry(sources=sources))), sources)

    def test_same_in_must_name_families_with_a_source(self):
        problems = self.shape(entry(same_in=["URTC", "ARMOR"]))
        self.assertTrue(any("ARMOR" in p and "no source" in p for p in problems))

    def test_a_shared_file_names_at_least_two_families_unless_it_is_ecosystem(self):
        self.assertTrue(any("at least two" in p for p in self.shape(entry(same_in=["URTC"]))))
        self.assertTrue(any("at least two" in p for p in self.shape(entry(same_in=[]))))
        self.assertEqual(self.shape(entry(kind="ecosystem", same_in=[])), [])

    def test_an_unknown_family_is_named(self):
        problems = self.shape(entry(sources={"URTC": {"repo": "a", "path": "b"}, "MARS": {"repo": "c", "path": "d"}}))
        self.assertTrue(any("unknown family MARS" in p for p in problems))


class TheRegistryAgainstARepository(unittest.TestCase):
    def test_source_text_of_a_family_without_a_source_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(tooling_registry.source_text(Path(tmp), entry(), "ARMOR"), ("", None))
            self.assertEqual(tooling_registry.source_text(Path(tmp), entry(), "HYDRA"), ("HYDRA-UMC-SDK", None))
            folder = Path(tmp) / "HYDRA-UMC-SDK" / "tools"
            folder.mkdir(parents=True)
            (folder / "x.py").write_bytes(b"print(1)\n")
            self.assertEqual(tooling_registry.source_text(Path(tmp), entry(), "HYDRA"), ("HYDRA-UMC-SDK", "print(1)\n"))

    def test_the_hash_of_a_source_that_changed_is_named_and_update_repairs_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "files").mkdir()
            (root / "tools").mkdir()
            (root / "tools" / "x.py").write_text("print(1)\n", encoding="utf-8")
            data = {"files": [entry(urtc_sha256="stale")]}
            self.assertTrue(any("hash in the registry is not the one of the file" in p for p in tooling_registry.check_own_side(data, root)))
            registry = root / "registry.json"
            self.assertEqual(tooling_registry.update(data, root, registry), 1)
            self.assertEqual(tooling_registry.check_own_side(data, root), [])
            self.assertEqual(tooling_registry.update(data, root, registry), 0)

    def test_a_source_that_is_gone_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "files").mkdir()
            data = {"files": [entry()]}
            self.assertTrue(any("source tools/x.py is missing" in p for p in tooling_registry.check_own_side(data, root)))
            with self.assertRaises(SystemExit):
                tooling_registry.update(data, root, root / "registry.json")

    def test_a_file_the_registry_says_is_in_the_set_but_files_does_not_hold_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "files").mkdir()
            data = {"files": [entry(in_set=True)]}
            self.assertTrue(any("files/ does not hold it" in p for p in tooling_registry.check_own_side(data, root)))

    def test_a_file_in_files_that_the_registry_does_not_list_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "files" / "tools").mkdir(parents=True)
            (root / "files" / "tools" / "extra.py").write_text("x\n", encoding="utf-8")
            problems = tooling_registry.check_own_side({"files": []}, root)
            self.assertTrue(any("is in files/ and not in the registry" in p for p in problems))

    def test_the_commands_report_and_check_run_on_an_empty_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run(tooling_registry.main, ["report", "--workspace", tmp])
            self.assertEqual(code, 0)
            self.assertIn("tools/", out)
            code, out, err = run(tooling_registry.main, ["check", "--workspace", tmp])
            self.assertIn(code, (0, 1))
            self.assertTrue("TOOLING_REGISTRY=" in out + err)

    def test_an_unknown_command_is_refused_by_the_parser(self):
        with self.assertRaises(SystemExit) as raised, contextlib.redirect_stderr(io.StringIO()):
            tooling_registry.main(["publish"])
        self.assertEqual(raised.exception.code, 2)


def make_repo(root: Path, name: str, **files: str) -> Path:
    repo = root / name
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / wt.MANIFEST).write_text("{}", encoding="utf-8")
    for file_name, text in files.items():
        (repo / ".github" / "workflows" / file_name).write_text(text, encoding="utf-8")
    return repo


GOOD = f"name: x\non: push\npermissions:\n  contents: read\njobs:\n  a:\n    steps:\n      - uses: actions/checkout@{SHA}\n"


class TheWorkflowFindings(unittest.TestCase):
    def test_a_good_workflow_has_no_finding(self):
        self.assertEqual(wt.security_findings("ci.yml", GOOD), [])

    def test_an_action_not_pinned_to_a_hash_is_named_with_its_line(self):
        found = wt.security_findings("ci.yml", GOOD.replace(SHA, "v4"))
        self.assertEqual(len(found), 1)
        self.assertIn("ci.yml:8: actions/checkout@v4 is not pinned", found[0])

    def test_a_short_hash_is_not_a_pin(self):
        self.assertEqual(len(wt.security_findings("ci.yml", GOOD.replace(SHA, "a" * 39))), 1)
        self.assertEqual(len(wt.security_findings("ci.yml", GOOD.replace(SHA, "a" * 41))), 0 if wt.SHA.match("a" * 41) else 1)

    def test_local_and_docker_actions_need_no_pin(self):
        text = GOOD + "      - uses: ./.github/actions/local\n      - uses: docker://alpine:3\n"
        self.assertEqual(wt.security_findings("ci.yml", text), [])

    def test_a_missing_permissions_block_and_pull_request_target_are_named(self):
        found = wt.security_findings("ci.yml", GOOD.replace("permissions:\n  contents: read\n", "").replace("on: push", "on:\n  pull_request_target:"))
        self.assertTrue(any("no top-level permissions" in f for f in found))
        self.assertTrue(any("pull_request_target" in f for f in found))

    def test_a_nested_permissions_block_is_not_a_top_level_one(self):
        text = "name: x\non: push\njobs:\n  a:\n    permissions:\n      contents: read\n"
        self.assertTrue(any("no top-level permissions" in f for f in wt.security_findings("ci.yml", text)))


class TheWorkflowDrift(unittest.TestCase):
    def test_comments_blank_lines_and_the_repository_name_do_not_count(self):
        a = "name: URTC-A\n# a comment\n\non: push\n"
        b = "name: URTC-B\non: push\n"
        self.assertEqual(wt.normalized(a, "URTC-A"), wt.normalized(b, "URTC-B"))

    def test_copies_that_differ_are_reported_once_per_file(self):
        found = wt.drift({"A": {"ci.yml": "on: push\n"}, "B": {"ci.yml": "on: pull_request\n"}, "C": {"ci.yml": "on: push\n"}})
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith("ci.yml: 2 different texts"))

    def test_a_single_copy_or_equal_copies_do_not_drift(self):
        self.assertEqual(wt.drift({"A": {"ci.yml": "on: push\n"}}), [])
        self.assertEqual(wt.drift({"A": {"ci.yml": "on: push\n"}, "B": {"ci.yml": "on: push\n"}}), [])
        self.assertEqual(wt.drift({}), [])

    def test_an_action_pinned_to_two_hashes_is_reported(self):
        a = f"jobs:\n  - uses: actions/checkout@{SHA}\n"
        b = f"jobs:\n  - uses: actions/checkout@{'b' * 40}\n"
        found = wt.drift({"A": {"x.yml": a}, "B": {"y.yml": b}})
        self.assertTrue(any(line.startswith("actions/checkout: pinned to 2 hashes") for line in found))

    def test_a_local_action_is_not_a_pin(self):
        text = "jobs:\n  - uses: ./a@b\n"
        self.assertEqual(wt.drift({"A": {"x.yml": text}, "B": {"x.yml": text}}), [])


class TheWorkflowCommand(unittest.TestCase):
    def test_a_workspace_without_repositories_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run(wt.main, ["check", "--workspace", tmp])
            self.assertEqual(code, 0)
            self.assertIn("WORKFLOW_TEMPLATES=SKIP", out)

    def test_a_folder_that_is_not_a_repository_is_not_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "plain").mkdir()
            (Path(tmp) / "file.txt").write_text("x", encoding="utf-8")
            make_repo(Path(tmp), "R", **{"ci.yml": GOOD})
            self.assertEqual([p.name for p in wt.repositories(Path(tmp))], ["R"])

    def test_check_fails_on_a_finding_and_report_never_does(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(Path(tmp), "R", **{"ci.yml": GOOD.replace(SHA, "v4")})
            code, out, _ = run(wt.main, ["check", "--workspace", tmp])
            self.assertEqual(code, 1)
            self.assertIn("WORKFLOW_TEMPLATES=FAIL", out)
            code, out, _ = run(wt.main, ["report", "--workspace", tmp])
            self.assertEqual(code, 0)
            self.assertIn("security=1", out)

    def test_a_drift_fails_only_when_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(Path(tmp), "A", **{"ci.yml": GOOD})
            make_repo(Path(tmp), "B", **{"ci.yml": GOOD.replace("on: push", "on: pull_request")})
            self.assertEqual(run(wt.main, ["check", "--workspace", tmp])[0], 0)
            code, out, _ = run(wt.main, ["check", "--strict", "--workspace", tmp])
            self.assertEqual(code, 1)
            self.assertIn("drift=1", out)

    def test_clean_repositories_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            make_repo(Path(tmp), "A", **{"ci.yml": GOOD})
            make_repo(Path(tmp), "B", **{"ci.yml": GOOD})
            code, out, _ = run(wt.main, ["check", "--strict", "--workspace", tmp])
            self.assertEqual(code, 0)
            self.assertIn("repositories=2 security=0 drift=0", out)


if __name__ == "__main__":
    unittest.main()
