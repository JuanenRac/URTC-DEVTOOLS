# =============================================================================
# URTC-DEVTOOLS - tests/test_tooling_registry_cli.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The parts of the registry tool that run from the command line: loading, the report, the update of the hashes and the exit codes of the check."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tooling_registry  # noqa: E402


def run(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tooling_registry.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class Loading(unittest.TestCase):
    def test_a_registry_without_a_list_of_files_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.json"
            path.write_text(json.dumps({"files": "no"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                tooling_registry.load(path)

    def test_the_registry_of_this_repository_loads(self):
        self.assertTrue(tooling_registry.load()["files"])


class FamilyRepositories(unittest.TestCase):
    def test_only_the_folders_with_the_manifest_of_the_family_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "URTC-A").mkdir()
            (root / "URTC-A" / "urtc.project.json").write_text("{}", encoding="utf-8")
            (root / "URTC-B").mkdir()
            self.assertEqual([p.name for p in tooling_registry.family_repositories(root, "URTC")], ["URTC-A"])
            self.assertEqual(tooling_registry.family_repositories(root / "missing", "URTC"), [])


class Update(unittest.TestCase):
    def test_a_wrong_hash_is_rewritten_and_a_right_one_is_left(self):
        data = copy.deepcopy(tooling_registry.load())
        data["files"][0]["urtc_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "registry.json"
            self.assertEqual(tooling_registry.update(data, registry=target), 1)
            self.assertEqual(tooling_registry.update(json.loads(target.read_text(encoding="utf-8")), registry=target), 0)


class MainCommand(unittest.TestCase):
    def test_check_passes_on_this_repository_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run("check", "--workspace", tmp)
        self.assertEqual(code, 0)
        self.assertIn("TOOLING_REGISTRY=PASS", out)

    def test_check_fails_when_the_registry_and_the_files_disagree(self):
        data = copy.deepcopy(tooling_registry.load())
        data["files"][0]["urtc_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(tooling_registry, "load", return_value=data):
            code, _, err = run("check", "--workspace", tmp)
        self.assertEqual(code, 1)
        self.assertIn("TOOLING_REGISTRY=FAIL", err)

    def test_report_lists_every_file_with_its_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run("report", "--workspace", tmp)
        self.assertEqual(code, 0)
        for entry in tooling_registry.load()["files"]:
            self.assertIn(entry["path"], out)

    def test_update_reports_how_many_hashes_it_changed(self):
        data = copy.deepcopy(tooling_registry.load())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "registry.json"
            with mock.patch.object(tooling_registry, "load", return_value=data), \
                    mock.patch.object(tooling_registry, "REGISTRY", target), \
                    mock.patch.object(tooling_registry, "update", return_value=0) as update:
                code, out, _ = run("update", "--workspace", tmp)
        self.assertEqual(code, 0)
        update.assert_called_once()
        self.assertIn("TOOLING_REGISTRY=WRITTEN 0", out)


if __name__ == "__main__":
    unittest.main()
