# =============================================================================
# URTC-DEVTOOLS - tests/test_build_test.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The shared build check (files/tools/build_test.py): the light mode builds and runs nothing, and the data of tools/build_test.json drives the rest."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "files" / "tools" / "build_test.py"


def make_repo(tmp: Path, stack: str, files: dict[str, str] | None = None, config: dict | None = None) -> Path:
    (tmp / "tools").mkdir()
    shutil.copy(SCRIPT, tmp / "tools" / "build_test.py")
    (tmp / "urtc.project.json").write_text(json.dumps({"name": "URTC-EXAMPLE", "stack": stack}), encoding="utf-8")
    for name, text in (files or {}).items():
        path = tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if config is not None:
        (tmp / "tools" / "build_test.json").write_text(json.dumps(config), encoding="utf-8")
    return tmp


def run(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(repo / "tools" / "build_test.py"), *args], capture_output=True, text=True, cwd=repo)


class LightCheck(unittest.TestCase):
    def check(self, stack, files=None, config=None):
        with tempfile.TemporaryDirectory() as tmp:
            return run(make_repo(Path(tmp), stack, files, config), "--check")

    def test_a_python_repository_passes_when_its_sources_compile(self):
        result = self.check("python", {"a.py": "x = 1\n"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BUILD_TEST_CHECK=PASS", result.stdout)

    def test_a_source_that_does_not_compile_fails(self):
        self.assertNotEqual(self.check("python", {"a.py": "def (:\n"}).returncode, 0)

    def test_a_stack_the_script_does_not_know_fails(self):
        result = self.check("cobol")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported stack", result.stderr)

    def test_a_firmware_repository_needs_its_build_script_and_a_node_one_its_package(self):
        self.assertNotEqual(self.check("firmware-c").returncode, 0)
        self.assertEqual(self.check("firmware-c", {"build_firmware.sh": "#!/bin/sh\n"}).returncode, 0)
        self.assertNotEqual(self.check("node").returncode, 0)
        self.assertEqual(self.check("node", {"package.json": json.dumps({"scripts": {"test": "x"}})}).returncode, 0)

    def test_a_qt_quick_repository_needs_its_qml_with_the_import(self):
        self.assertNotEqual(self.check("python-qtquick").returncode, 0)
        self.assertNotEqual(self.check("python-qtquick", {"assets/qml/A.qml": "Item {}\n"}).returncode, 0)
        self.assertEqual(self.check("python-qtquick", {"assets/qml/A.qml": "import QtQuick 2.15\nItem {}\n"}).returncode, 0)

    def test_the_missing_translation_of_a_qml_key_is_named(self):
        qml = 'import QtQuick 2.15\nText { text: uiText("HELLO_KEY") }\n'
        result = self.check("python-qtquick", {"assets/qml/A.qml": qml, "language/en.lng": "OTHER=1\n"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HELLO_KEY", result.stderr)

    def test_a_tests_folder_that_is_not_there_fails_and_an_unknown_key_of_the_data_fails(self):
        self.assertNotEqual(self.check("python", config={"pytest": {"dir": "nope"}}).returncode, 0)
        result = self.check("python", config={"surprise": 1})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("surprise", result.stderr)


class FullCheck(unittest.TestCase):
    def test_the_tests_of_the_repository_run_when_it_lists_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), "python", {"tests/test_ok.py": "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.assertTrue(True)\n"},
                             {"unittest": "tests"})
            result = run(repo)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("UNIT_TESTS=PASS", result.stdout)
            self.assertIn("BUILD_TEST=PASS", result.stdout)

    def test_a_failing_test_fails_the_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), "python", {"tests/test_bad.py": "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.fail('no')\n"},
                             {"unittest": "tests"})
            self.assertNotEqual(run(repo).returncode, 0)

    def test_without_data_a_python_repository_only_compiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(make_repo(Path(tmp), "python", {"a.py": "x = 1\n", "tests/test_bad.py": "raise SystemExit(3)\n"}))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("UNIT_TESTS", result.stdout)


class LocalBuildLock(unittest.TestCase):
    """The full check of a stack that compiles is locked on a developer PC: skipped with exit 2, never a pass, and nothing is invoked."""

    def full(self, stack, **env):
        base = {k: v for k, v in os.environ.items() if k not in ("CI", "GITHUB_ACTIONS", "ALLOW_LOCAL_BUILD")}
        base.update(env)
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), stack, {"Cargo.toml": "", "build_firmware.sh": "exit 9\n", "gradlew": "", "gradlew.bat": "", "pubspec.yaml": "", "go.mod": ""})
            return subprocess.run([sys.executable, str(repo / "tools" / "build_test.py")], capture_output=True, text=True, cwd=repo, env={**base, "PATH": ""})

    def test_every_stack_that_compiles_is_skipped_without_permission(self):
        for stack in ("rust", "go", "android", "flutter", "firmware-c"):
            result = self.full(stack)
            self.assertEqual(result.returncode, 2, stack + result.stderr)
            self.assertIn("BUILD_TEST=SKIPPED", result.stdout)
            self.assertNotIn("BUILD_TEST=PASS", result.stdout)

    def test_the_permission_lets_the_build_start(self):
        for env in ({"CI": "true"}, {"GITHUB_ACTIONS": "true"}, {"ALLOW_LOCAL_BUILD": "1"}):
            result = self.full("rust", **env)
            self.assertNotEqual(result.returncode, 2)   # it tried to run cargo (not found on the empty PATH), which is a failure, not a skip
            self.assertNotIn("BUILD_TEST=SKIPPED", result.stdout)

    def test_the_light_check_and_the_python_stack_are_not_locked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), "rust", {"Cargo.toml": ""})
            self.assertEqual(run(repo, "--check").returncode, 0)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(make_repo(Path(tmp), "python", {"a.py": "x = 1\n"})).returncode, 0)


if __name__ == "__main__":
    unittest.main()
