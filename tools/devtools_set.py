#!/usr/bin/env python3
# =============================================================================
# URTC-DEVTOOLS - tools/devtools_set.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The set of shared repository tools that this repository versions.

    python tools/devtools_set.py            # the version of the set and the SHA-256 of each file
    python tools/devtools_set.py list       # the same
    python tools/devtools_set.py check      # the copies this repository carries itself equal the canonical files

The canonical files sit in ``files/``, at the path they have in every repository, with the name of the repository written ``<REPO>``. The version
of the set is the version of this repository (``urtc.project.json``). A repository takes the set with ``tools/sync_repo_tools.py`` of URTC-DOCS, which
writes ``tools/devtools.lock.json`` with the version and the SHA-256 of each file it copied; ``tools/check_repo_tools.py`` compares the lock with the files.
Standard library only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ROOT / "files"
PLACEHOLDER = "<REPO>"
LOCK_NAME = "tools/devtools.lock.json"


def version() -> str:
    """The version of the set: the one of the manifest of this repository."""
    return str(json.loads((ROOT / "urtc.project.json").read_text(encoding="utf-8"))["version"])


def shared_files(files: Path = FILES) -> list[str]:
    """The relative paths of the canonical files, sorted."""
    return sorted(p.relative_to(files).as_posix() for p in files.rglob("*") if p.is_file())


def canonical_text(relative: str, files: Path = FILES) -> str:
    """The text of one canonical file, with newlines."""
    return (files / relative).read_bytes().decode("utf-8").replace("\r\n", "\n")


def digest(text: str) -> str:
    """SHA-256 of a text as it is compared: line endings as newlines, encoded as UTF-8."""
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def render_for(repository: str, relative: str, files: Path = FILES) -> str:
    """The text a repository carries: its own name where the canonical file says <REPO>."""
    return canonical_text(relative, files).replace(PLACEHOLDER, repository)


def check_own_copies(root: Path = ROOT) -> list[str]:
    """The files of the set that this repository carries as its own copy must be what the canonical file renders to."""
    problems = []
    for relative in shared_files(root / "files"):
        path = root / relative
        if not path.is_file():
            problems.append(f"{relative}: missing")
        elif path.read_bytes().decode("utf-8").replace("\r\n", "\n") != render_for(root.name, relative, root / "files"):
            problems.append(f"{relative}: differs from files/{relative}")
    return problems


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    command = arguments[0] if arguments else "list"
    if command == "list":
        print(f"URTC-DEVTOOLS set version {version()}")
        for relative in shared_files():
            print(f"{digest(canonical_text(relative))}  {relative}")
        return 0
    if command == "check":
        problems = check_own_copies()
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        if problems:
            print(f"DEVTOOLS_SET=FAIL {len(problems)} file(s)", file=sys.stderr)
            return 1
        print(f"DEVTOOLS_SET=PASS {len(shared_files())} files, version {version()}")
        return 0
    print(__doc__)
    return 0 if command in {"-h", "--help", "help"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
