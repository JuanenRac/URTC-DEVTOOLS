#!/usr/bin/env python3
# =============================================================================
# URTC-DEVTOOLS - tools/fleet_simulation.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A virtual family of repositories, built in a temporary folder, to try the set from end to end without the real repositories (evidence: simulator).

The set is only worth something when many repositories carry it at once, and the real family is far away: dozens of checkouts, a bot that writes the workflows, a nightly job
that compares them. This module builds the family in memory-sized folders instead:

* every virtual repository gets the real files of the set (``files/``, rendered with its own name) and a lock written the way ``docs/LOCK_FORMAT.md`` says;
* faults are injected on purpose (a hand edit, a deleted copy, a shared file the lock does not list, a copy that fell behind a new version of the set, a broken lock, a
  workflow that is not pinned, runs on ``pull_request_target`` or drifts from the others);
* the checks are the ones of the set: the lock check (the same rules as ``urtc_docs.devtools_lock`` of URTC-DOCS, and the tests compare both when URTC-DOCS is next to
  this repository) and ``tools/workflow_templates.py``.

    python tools/fleet_simulation.py          # builds a family of virtual repositories, breaks it in a few ways, and prints FLEET_SIMULATION=PASS or FAIL

Nothing leaves the temporary folder. There is no clock, no network and no randomness: the same call always gives the same result. Standard library only.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import devtools_set  # noqa: E402
import workflow_templates  # noqa: E402

LOCK_FILE = devtools_set.LOCK_NAME
SCHEMA = 1
MANIFEST = "urtc.project.json"
PINNED_CHECKOUT = "actions/checkout@" + "0" * 40
DEFAULT_NAMES = ("URTC", "URTC-COMMON", "URTC-GATEWAY", "URTC-TESTER")


def digest(text: str) -> str:
    """SHA-256 as the lock compares it: line endings as newlines, UTF-8."""
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


class VirtualFleet:
    """A family of virtual repositories next to a virtual URTC-DEVTOOLS (only its manifest: the files come from ``files/`` of the real set)."""

    def __init__(self, root: Path, names: tuple[str, ...] = DEFAULT_NAMES, set_version: str | None = None, build: bool = True) -> None:
        """``build=False`` adopts a folder that an earlier fleet built (a copy of it): nothing is written."""
        self.root = root
        self.names = names
        self.set_version = set_version or devtools_set.version()
        self.files = tuple(devtools_set.shared_files())
        if not build:
            return
        self._write_json(root / "URTC-DEVTOOLS" / MANIFEST, {"name": "URTC-DEVTOOLS", "version": self.set_version})
        for name in names:
            self._write_json(self.repo(name) / MANIFEST, {"name": name, "version": "0.1.0", "ecosystem": "URTC"})
            self.take_set(name)
            self._write_ci(name)

    def _write_ci(self, name: str) -> None:
        """The workflow that a central bot writes into every repository: the same text with the name of the repository, its actions pinned to a commit."""
        path = self.repo(name) / ".github" / "workflows" / "ci.yml"
        text = "\n".join(
            [
                f"name: {name} CI",
                "on:",
                "  push:",
                "permissions:",
                "  contents: read",
                "jobs:",
                "  check:",
                "    runs-on: ubuntu-latest",
                "    steps:",
                f"      - uses: {PINNED_CHECKOUT}",
                "      - run: python tools/ci_validate.py",
                "",
            ]
        )
        self._put(path, text)

    # ---- building -----------------------------------------------------------------
    @staticmethod
    def _put(path: Path, text: str) -> None:
        """Writes the text unless the file already is exactly that (the disk is the slow part of a fleet, and a reset touches only what a fault changed)."""
        data = text.encode("utf-8")
        if path.is_file() and path.read_bytes() == data:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    @classmethod
    def _write_json(cls, path: Path, data: dict) -> None:
        cls._put(path, json.dumps(data, indent=2, sort_keys=True) + "\n")

    def reset(self) -> None:
        """Back to a family that took the current set of the real repository: every fault undone, only the files a fault touched rewritten."""
        self.publish_set(devtools_set.version())
        for name in self.names:
            self._write_json(self.repo(name) / MANIFEST, {"name": name, "version": "0.1.0", "ecosystem": "URTC"})
            self.take_set(name)
            self._write_ci(name)
            extra = self.repo(name) / ".github" / "workflows" / "extra.yml"
            if extra.is_file():
                extra.unlink()

    def repo(self, name: str) -> Path:
        return self.root / name

    def take_set(self, name: str, version: str | None = None) -> None:
        """What ``sync_repo_tools.py --apply`` does for one repository: write every copy rendered with its name, then the lock."""
        repo = self.repo(name)
        hashes = {}
        for relative in self.files:
            text = devtools_set.render_for(name, relative)
            self._put(repo / relative, text)
            hashes[relative] = digest(text)
        self._write_lock(name, version or self.set_version, hashes)

    def take_all(self) -> None:
        for name in self.names:
            self.take_set(name)

    def _write_lock(self, name: str, version: str, hashes: dict[str, str]) -> None:
        self._write_json(self.repo(name) / LOCK_FILE, {"schema": SCHEMA, "source": "URTC-DEVTOOLS", "version": version, "files": dict(sorted(hashes.items()))})

    def _lock(self, name: str) -> dict:
        return json.loads((self.repo(name) / LOCK_FILE).read_text(encoding="utf-8"))

    # ---- the set moves on ---------------------------------------------------------
    def publish_set(self, version: str) -> None:
        """A new version of the set is released: the repositories that have not taken it yet fall behind."""
        self.set_version = version
        self._write_json(self.root / "URTC-DEVTOOLS" / MANIFEST, {"name": "URTC-DEVTOOLS", "version": version})

    # ---- faults -------------------------------------------------------------------
    def hand_edit(self, name: str, relative: str, line: str = "# edited by hand\n") -> None:
        path = self.repo(name) / relative
        path.write_text(path.read_text(encoding="utf-8") + line, encoding="utf-8", newline="\n")

    def delete(self, name: str, relative: str) -> None:
        (self.repo(name) / relative).unlink()

    def drop_from_lock(self, name: str, relative: str) -> None:
        lock = self._lock(name)
        del lock["files"][relative]
        self._write_json(self.repo(name) / LOCK_FILE, lock)

    def to_crlf(self, name: str, relative: str) -> None:
        """The copy is checked out on Windows: same text, other line endings. Not a fault."""
        path = self.repo(name) / relative
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))

    def break_lock(self, name: str, how: str = "json") -> None:
        path = self.repo(name) / LOCK_FILE
        if how == "json":
            path.write_text("{not json", encoding="utf-8")
        elif how == "schema":
            self._write_json(path, {"schema": 2, "files": {}})
        else:
            self._write_json(path, {"schema": SCHEMA, "files": []})

    def remove_lock(self, name: str) -> None:
        (self.repo(name) / LOCK_FILE).unlink()

    def unpin_action(self, name: str) -> None:
        path = self.repo(name) / ".github" / "workflows" / "ci.yml"
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if "uses:" in line and "@" in line and not line.strip().startswith("#"):
                lines[index] = line.split("@")[0] + "@v4"
                break
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    def run_on_pull_request_target(self, name: str) -> None:
        path = self.repo(name) / ".github" / "workflows" / "extra.yml"
        path.write_text("name: extra\non:\n  pull_request_target:\npermissions:\n  contents: read\njobs: {}\n", encoding="utf-8", newline="\n")

    # ---- the checks ---------------------------------------------------------------
    def relock(self, name: str) -> None:
        """A hand edit that hides itself: the lock is written again from the files as they are now."""
        hashes = {relative: digest((self.repo(name) / relative).read_bytes().decode("utf-8")) for relative in self.files if (self.repo(name) / relative).is_file()}
        self._write_lock(name, self._lock(name).get("version", self.set_version), hashes)

    def missing_locks(self) -> list[str]:
        """The repositories of the family that carry no lock (counted, whatever the check lets pass)."""
        return [name for name in self.names if not (self.repo(name) / LOCK_FILE).is_file()]

    def check(self, name: str, allow_missing_lock: bool = True) -> list[str]:
        """The problems of the lock of one repository, with the rules of docs/LOCK_FORMAT.md; empty when it has none (unless ``allow_missing_lock`` is False) or all is as it should be.

        A file whose hash agrees with the lock but is not the canonical file is also a problem: the lock was recalculated after an edit."""
        path = self.repo(name) / LOCK_FILE
        if not path.is_file():
            return [] if allow_missing_lock else [f"{LOCK_FILE} is missing (the repository is expected to carry it)"]
        try:
            lock = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            lock = None
        if not isinstance(lock, dict) or lock.get("schema") != SCHEMA or not isinstance(lock.get("files"), dict):
            return [f"{LOCK_FILE} cannot be read (schema {SCHEMA} expected)"]
        problems = []
        for relative, expected in sorted(lock["files"].items()):
            target = self.repo(name) / relative
            if not target.is_file():
                problems.append(f"{relative}: in the lock but missing")
            elif digest(target.read_bytes().decode("utf-8", errors="replace")) != expected:
                problems.append(f"{relative}: edited after the set was taken (it differs from the lock)")
        for relative in self.files:
            if (self.repo(name) / relative).is_file() and relative not in lock["files"]:
                problems.append(f"{relative}: a shared file that the lock does not list")
        if lock.get("version") != self.set_version:
            problems.append(f"the lock says set {lock.get('version')!r}, URTC-DEVTOOLS is at {self.set_version!r}: run sync_repo_tools.py --apply")
        elif not problems:
            problems += [f"{problem.split(':')[0]}: edited and the lock recalculated (it differs from the canonical file)" for problem in devtools_set.verify_repo(self.repo(name))]
        return problems

    def check_all(self, allow_missing_lock: bool = True) -> dict[str, list[str]]:
        return {name: problems for name in self.names if (problems := self.check(name, allow_missing_lock))}

    def workflows(self) -> tuple[int, list[str]]:
        """``workflow_templates.py check`` over the virtual family: its exit status and the lines it prints."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = workflow_templates.main(["check", "--workspace", str(self.root), "--strict"])
        return code, out.getvalue().splitlines()

    def nightly(self) -> list[str]:
        """What a night of the comparison would report: the problem of every lock and every line of the workflow check that is not a pass."""
        lines = [f"{name}: {problem}" for name, problems in self.check_all().items() for problem in problems]
        lines += [f"NOTICE {name}: {LOCK_FILE} is missing (allowed for now)" for name in self.missing_locks()]
        _code, printed = self.workflows()
        return lines + [line for line in printed if line.startswith(("SECURITY", "DRIFT"))]


def demonstration() -> list[str]:
    """Take the set into a family, break it three ways, heal it; the problems found with what happened, empty when all is as expected."""
    problems = []
    with tempfile.TemporaryDirectory() as folder:
        fleet = VirtualFleet(Path(folder))
        if fleet.nightly():
            problems.append("a family that just took the set is not clean")
        fleet.hand_edit("URTC-GATEWAY", "tools/build_test.py")
        fleet.delete("URTC-TESTER", "tools/pretty_run.py")
        fleet.publish_set("9.9.9")
        if len(fleet.check_all()) != len(fleet.names):
            problems.append("a new version of the set did not leave every repository behind")
        fleet.take_all()
        if fleet.nightly():
            problems.append("taking the set again did not heal the family")
    return problems


def structured_report() -> dict:
    """The same night as ``demonstration``, as data: each fault injected has an identifier and the report must name it.

    ``{"set_version", "repositories": {name: {"lock": [...], "workflows": [...]}}, "faults_injected": [{"id", "repository", "found"}]}``;
    ``found`` is True when the problems of that repository mention the fault, so a fault that nothing noticed is visible in the data.
    """
    with tempfile.TemporaryDirectory() as folder:
        fleet = VirtualFleet(Path(folder))
        fleet.hand_edit("URTC-GATEWAY", "tools/build_test.py")
        fleet.delete("URTC-TESTER", "tools/pretty_run.py")
        fleet.publish_set("9.9.9")
        _code, printed = fleet.workflows()
        found = fleet.check_all()
        report: dict = {
            "set_version": fleet.set_version,
            "repositories": {name: {"lock": found.get(name, []), "workflows": [line for line in printed if line.startswith(("SECURITY", "DRIFT")) and name in line]} for name in fleet.names},
            "faults_injected": [],
        }
        for fault, name, marker in (
            ("hand_edit", "URTC-GATEWAY", "tools/build_test.py"),
            ("delete", "URTC-TESTER", "tools/pretty_run.py"),
        ):
            report["faults_injected"].append({"id": fault, "repository": name, "found": any(marker in line for line in found.get(name, []))})
        return report


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    problems = demonstration()
    if "--json" in arguments:
        report = structured_report()
        problems += [f"the fault {fault['id']} in {fault['repository']} is not named by the report" for fault in report["faults_injected"] if not fault["found"]]
        print(json.dumps(report, indent=2, sort_keys=True))
    for line in problems:
        print(line, file=sys.stderr if "--json" in arguments else sys.stdout)
    print(f"FLEET_SIMULATION={'FAIL' if problems else 'PASS'}", file=sys.stderr if "--json" in arguments else sys.stdout)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
