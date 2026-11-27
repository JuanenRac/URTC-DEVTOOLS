# =============================================================================
# URTC-DEVTOOLS - tests/test_process_encoding.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared tools read what a child process writes as UTF-8 and survive a byte that is not: text mode without an encoding reads with the code page of Windows."""
from __future__ import annotations

import ast
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import status_lights  # noqa: E402
import universal_readme_check  # noqa: E402

NOISY_TEST = """import sys
import unittest


class T(unittest.TestCase):
    def {name}(self):
        sys.stderr.flush()
        sys.stderr.buffer.write(bytes([0x81, 0x8F, 0x9D, 0xC3, 0xB1, 10]))
        sys.stderr.buffer.flush()
"""


def text_calls_without_encoding(source: str) -> list[int]:
    """The lines where a process is started in text mode without saying which encoding."""
    lines = []
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "Popen", "check_output"}):
            continue
        keywords = {k.arg: k.value for k in node.keywords}
        given = [keywords.get(name) for name in ("text", "universal_newlines")]
        text_mode = any(isinstance(value, ast.Constant) and value.value is True for value in given)
        if text_mode and not {"encoding", "errors"} <= set(keywords):
            lines.append(node.lineno)
    return lines


class ProcessEncodingTests(unittest.TestCase):
    def test_the_scan_finds_a_call_without_encoding(self):
        self.assertEqual(text_calls_without_encoding("import subprocess\nsubprocess.run(['x'], text=True)\n"), [2])

    def test_every_tool_of_the_set_names_the_encoding_of_what_it_reads(self):
        found = {path.name: text_calls_without_encoding(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "files" / "tools").glob("*.py"))}
        self.assertEqual({name: lines for name, lines in found.items() if lines}, {})

    def test_the_test_count_survives_output_that_is_not_text(self):
        with tempfile.TemporaryDirectory() as folder:
            tests = Path(folder) / "tests"
            tests.mkdir()
            (tests / "test_noise.py").write_text(NOISY_TEST.replace("{name}", "test_noise"), encoding="utf-8")
            self.assertEqual(universal_readme_check.run_tests(Path(folder)), 1)


class SharedRowsTests(unittest.TestCase):
    """The Security, Updates and Writing rows have their own ceiling only in an A.R.M.O.R. repository."""

    def kinds(self, manifest_name: str) -> list[str]:
        rows = "| Security | x | s |\n| Updates | x | u |\n| Writing | x | w |\n"
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            (repo / manifest_name).write_text('{"evidence": "none"}', encoding="utf-8")
            (repo / "README.md").write_text("## \U0001F6A6 Project status\n\n| Area | State | Note |\n|---|---|---|\n" + rows, encoding="utf-8")
            return [item["kind"] for item in status_lights.evaluate(repo, "off")["items"]]

    def test_the_rows_are_read_in_an_armor_repository_only(self):
        self.assertEqual(self.kinds("armor.project.json"), ["security", "updates", "writing"])
        self.assertEqual(self.kinds("urtc.project.json"), ["other", "other", "other"])


if __name__ == "__main__":
    unittest.main()
