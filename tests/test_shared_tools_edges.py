# =============================================================================
# URTC-DEVTOOLS - tests/test_shared_tools_edges.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The pure functions of two shared tools at their edges: how the test counter reads the output of each runner, and how the status lights read, limit and rewrite the status
table of a readme."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import pretty_run  # noqa: E402
import status_lights as sl  # noqa: E402

TABLE = (
    "# Title\n\nintro\n\n## \U0001F6A6 Project status\n\n"
    "| Part | Status | Meaning |\n|---|---|---|\n"
    "| Software | \U0001F7E2 | ok |\n| Tests | \U0001F7E1 | some |\n| Hardware | \U0001F534 | none \\| yet |\n\n## Next\n\ntext\n"
)


class CountTestsTests(unittest.TestCase):
    def test_pytest_with_and_without_failures(self):
        self.assertEqual(pretty_run.count_tests("===== 12 passed in 1.2s ====="), (12, 0))
        self.assertEqual(pretty_run.count_tests("===== 2 failed, 10 passed, 1 skipped in 3s ====="), (10, 2))

    def test_vitest_with_and_without_failures(self):
        self.assertEqual(pretty_run.count_tests("      Tests  1712 passed (1712)\n"), (1712, 0))
        self.assertEqual(pretty_run.count_tests("      Tests  3 failed | 40 passed (43)\n"), (40, 3))

    def test_unittest_ok_and_failed_and_with_errors(self):
        self.assertEqual(pretty_run.count_tests("Ran 109 tests in 2s\n\nOK\n"), (109, 0))
        self.assertEqual(pretty_run.count_tests("Ran 5 tests in 1s\n\nFAILED (failures=2)\n"), (3, 2))
        self.assertEqual(pretty_run.count_tests("Ran 5 tests in 1s\n\nFAILED (failures=1, errors=2)\n"), (2, 3))
        self.assertEqual(pretty_run.count_tests("Ran 1 test in 0.1s\n\nOK\n"), (1, 0))

    def test_ctest_all_passed_and_some_failed(self):
        self.assertEqual(pretty_run.count_tests("100% tests passed, 0 tests failed out of 4"), (4, 0))
        self.assertEqual(pretty_run.count_tests("50% tests passed, 1 tests failed out of 2"), (1, 1))

    def test_cargo_and_node(self):
        self.assertEqual(pretty_run.count_tests("test result: ok. 7 passed; 0 failed; 0 ignored"), (7, 0))
        self.assertEqual(pretty_run.count_tests("test result: FAILED. 4 passed; 2 failed; 0 ignored"), (4, 2))
        self.assertEqual(pretty_run.count_tests("ℹ pass 30\nℹ fail 1\n"), (30, 1))

    def test_several_runners_in_one_output_add_up(self):
        self.assertEqual(pretty_run.count_tests("===== 3 passed in 1s =====\nRan 4 tests in 1s\n\nOK\n"), (7, 0))

    def test_nothing_that_looks_like_a_result_gives_zero_and_zero(self):
        for text in ("", "hello", "12 passed", "OK"):
            with self.subTest(text=text):
                self.assertEqual(pretty_run.count_tests(text), (0, 0))

    def test_the_time_is_written_in_seconds_then_in_minutes(self):
        self.assertEqual(pretty_run._seconds(0), "0.0 s")
        self.assertEqual(pretty_run._seconds(59.94), "59.9 s")
        self.assertEqual(pretty_run._seconds(60), "1 min 00 s")
        self.assertEqual(pretty_run._seconds(125.9), "2 min 05 s")


class KindOfTests(unittest.TestCase):
    def test_each_label_gives_its_kind(self):
        cases = {"Software": "software", "software": "software", "Tests": "tests", "Test suite": "tests", "Documentation": "docs", "Docs": "docs",
                 "Hardware": "hardware", "Board bring-up": "hardware", "Firmware on the board": "hardware", "Integration": "integration",
                 "Hardware integration": "integration", "Licence": "other", "": "other", "  Software  ": "software"}
        for label, kind in cases.items():
            with self.subTest(label=label):
                self.assertEqual(sl.kind_of(label), kind)


class TableTests(unittest.TestCase):
    def test_the_rows_and_the_line_of_the_first_row_are_found(self):
        first, rows = sl.read_table(TABLE)
        self.assertEqual(TABLE.split("\n")[first].split("|")[1].strip(), "Software")
        self.assertEqual([row[0] for row in rows], ["Software", "Tests", "Hardware"])
        self.assertEqual(sl.lights_of(rows), [sl.GREEN, sl.YELLOW, sl.RED])

    def test_an_escaped_pipe_stays_inside_its_cell(self):
        _first, rows = sl.read_table(TABLE)
        self.assertEqual(rows[2][2], "none \\| yet")

    def test_no_table_and_a_table_with_no_rows_give_none(self):
        self.assertIsNone(sl.read_table("# Title\n\nno status here\n"))
        self.assertIsNone(sl.read_table("## \U0001F6A6 Project status\n\n| Part | Status |\n|---|---|\n\n## Next\n"))

    def test_a_heading_inside_a_code_fence_is_not_a_table(self):
        fenced = "```\n## \U0001F6A6 Project status\n| a | b |\n|---|---|\n| Software | \U0001F7E2 |\n```\n"
        self.assertIsNone(sl.read_table(fenced))

    def test_only_the_first_status_section_counts(self):
        twice = TABLE + "\n## \U0001F6A6 Project status\n\n| Part | Status |\n|---|---|\n| Software | \U0001F534 |\n"
        _first, rows = sl.read_table(twice)
        self.assertEqual(len(rows), 3)

    def test_rewriting_the_lights_changes_only_the_light_cells(self):
        wanted = [sl.ORANGE, sl.ORANGE, sl.ORANGE]
        new = sl.replace_lights(TABLE, wanted)
        _first, rows = sl.read_table(new)
        self.assertEqual(sl.lights_of(rows), wanted)
        self.assertEqual([row[2] for row in rows], ["ok", "some", "none \\| yet"])
        self.assertEqual(new.replace(sl.ORANGE, "X").count("X"), 3)
        self.assertEqual(sl.replace_lights(new, [sl.GREEN, sl.YELLOW, sl.RED]), TABLE)

    def test_a_row_with_one_cell_has_an_empty_light(self):
        self.assertEqual(sl.lights_of([["Only"], ["A", sl.GREEN]]), ["", sl.GREEN])


class CeilingTests(unittest.TestCase):
    def test_a_young_project_never_goes_above_yellow(self):
        for maturity in ("scaffolding", "Experimental", "ALPHA", "prototype"):
            light, why = sl.ceiling("software", {"maturity": maturity}, True, True, "green")
            self.assertEqual(light, sl.YELLOW)
            self.assertIn("maturity", why)

    def test_a_software_row_needs_tests_and_a_workflow_and_a_green_run(self):
        self.assertEqual(sl.ceiling("software", {}, True, True, "green"), (sl.GREEN, "no limit"))
        self.assertEqual(sl.ceiling("software", {}, False, True, "green")[0], sl.YELLOW)
        self.assertEqual(sl.ceiling("docs", {}, True, False, "green")[0], sl.YELLOW)
        self.assertEqual(sl.ceiling("tests", {}, True, True, "red"), (sl.YELLOW, "the CI of the default branch is red"))
        self.assertEqual(sl.ceiling("software", {}, True, True, "unknown")[0], sl.GREEN)

    def test_a_hardware_row_is_held_by_the_evidence_and_never_by_the_tests(self):
        expected = {"none": sl.ORANGE, "host-test": sl.ORANGE, "simulator": sl.ORANGE, "bench": sl.YELLOW, "field": sl.GREEN}
        for evidence, light in expected.items():
            with self.subTest(evidence=evidence):
                self.assertEqual(sl.ceiling("hardware", {"evidence": evidence}, False, False, "red")[0], light)
        self.assertEqual(sl.ceiling("integration", {"evidence": "something else"}, True, True, "green")[0], sl.ORANGE)
        self.assertEqual(sl.ceiling("hardware", {}, True, True, "green")[0], sl.ORANGE)

    def test_a_project_not_bound_to_hardware_is_not_held_by_it(self):
        self.assertEqual(sl.ceiling("hardware", {"evidence": "none", "hardware_bound": False}, True, True, "green")[0], sl.GREEN)

    def test_other_rows_have_no_ceiling_of_their_own(self):
        self.assertEqual(sl.ceiling("other", {}, False, False, "red"), (sl.GREEN, "no limit"))

    def test_the_order_runs_from_the_worst_to_the_best(self):
        self.assertEqual(sl.ORDER, (sl.RED, sl.ORANGE, sl.YELLOW, sl.GREEN))
        self.assertEqual({sl.WORDS[sl.NAMES[name]] for name in sl.NAMES}, set(sl.NAMES))


if __name__ == "__main__":
    unittest.main()
