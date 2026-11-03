# =============================================================================
# URTC-DEVTOOLS - tests/test_workflow_templates.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The comparison of the workflow templates: the security findings, the normalization and the drift report."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import workflow_templates as wt  # noqa: E402

SHA = "a" * 40
GOOD = f"name: x\non: push\npermissions: {{}}\njobs:\n  a:\n    steps:\n      - uses: actions/checkout@{SHA} # v5\n"


class SecurityTests(unittest.TestCase):
    def test_a_pinned_workflow_with_permissions_is_clean(self):
        self.assertEqual(wt.security_findings("x.yml", GOOD), [])

    def test_an_unpinned_action_is_reported(self):
        found = wt.security_findings("x.yml", GOOD.replace(f"@{SHA}", "@v5"))
        self.assertEqual(len(found), 1)
        self.assertIn("not pinned", found[0])

    def test_a_missing_permissions_block_and_pull_request_target_are_reported(self):
        text = GOOD.replace("permissions: {}\n", "").replace("on: push", "on:\n  pull_request_target:")
        self.assertEqual(len(wt.security_findings("x.yml", text)), 2)

    def test_local_actions_are_not_pinned_by_hash(self):
        self.assertEqual(wt.security_findings("x.yml", GOOD + "      - uses: ./.github/actions/a\n"), [])


class DriftTests(unittest.TestCase):
    def test_comments_schedules_and_the_repository_name_do_not_count(self):
        a = "# one\non:\n  schedule:\n    - cron: \"1 2 * * *\"\nname: R-A\n"
        b = "# two\non:\n  schedule:\n    - cron: \"3 4 * * *\"\nname: R-B\n"
        self.assertEqual(wt.normalized(a, "R-A").replace("<repo>", "x"), wt.normalized(b, "R-B").replace("<repo>", "x"))

    def test_a_different_text_and_a_second_pin_are_reported(self):
        other = GOOD.replace("a" * 40, "b" * 40) + "      - run: echo\n"
        lines = wt.drift({"R1": {"ci.yml": GOOD}, "R2": {"ci.yml": other}})
        self.assertTrue(any(line.startswith("ci.yml: 2 different texts") for line in lines))
        self.assertTrue(any(line.startswith("actions/checkout: pinned to 2 hashes") for line in lines))

    def test_equal_copies_report_nothing(self):
        self.assertEqual(wt.drift({"R1": {"ci.yml": GOOD}, "R2": {"ci.yml": GOOD}}), [])


class MainTests(unittest.TestCase):
    def make(self, root: Path, name: str, text: str):
        folder = root / name / ".github" / "workflows"
        folder.mkdir(parents=True)
        (folder / "ci.yml").write_text(text, encoding="utf-8")
        (root / name / wt.MANIFEST).write_text("{}", encoding="utf-8")

    def test_check_fails_on_a_security_finding_and_report_never_does(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make(root, "R1", GOOD.replace(f"@{SHA}", "@v5"))
            self.assertEqual(wt.main(["check", "--workspace", str(root)]), 1)
            self.assertEqual(wt.main(["report", "--workspace", str(root)]), 0)

    def test_strict_fails_on_a_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make(root, "R1", GOOD)
            self.make(root, "R2", GOOD + "      - run: echo\n")
            self.assertEqual(wt.main(["check", "--workspace", str(root)]), 0)
            self.assertEqual(wt.main(["check", "--workspace", str(root), "--strict"]), 1)


if __name__ == "__main__":
    unittest.main()
