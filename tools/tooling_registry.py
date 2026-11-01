#!/usr/bin/env python3
# =============================================================================
# URTC-DEVTOOLS - tools/tooling_registry.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The registry of the tooling that the families keep as the same file, and the check that none of them drifted.

The families (URTC, HYDRA-UMC, A.R.M.O.R.) each keep their shared tools in one place: this repository (``files/``), HYDRA-UMC-SDK (``tools/canonical/``)
and ARMOR-COMMON (``tools/``). Several of those files are the same text in more than one family. ``tools/tooling_registry.json`` says which, where each
family keeps its source, how two sources are compared, and the SHA-256 of the URTC source (the same hash the lock of every repository carries).

    python tools/tooling_registry.py check              # exit 1 when the registry and this repository disagree, or when two sources that must be equal are not
    python tools/tooling_registry.py report             # the table: for each file, the sources of the families and how many repositories carry each text
    python tools/tooling_registry.py update             # write the hashes of the URTC sources into the registry (after a change to files/)
    python tools/tooling_registry.py ... --workspace DIR  # the folder that holds the repositories side by side (default: the parent of this one)

``check`` works with this repository alone (the hashes of the registry against ``files/`` and the list of the set); when the repositories of the other
families are next to this one it also compares the sources that the registry says must be equal. Nothing is ever written to another repository.
Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import devtools_set  # the set of this repository (tools/ is on the path when this file is run)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "tools" / "tooling_registry.json"
KINDS = ("identical", "same_after_banner", "ecosystem")
# the manifest that marks a repository as a member of a family, and the prefix of its name
FAMILIES = {
    "URTC": ("urtc.project.json", "URTC"),
    "HYDRA": ("hydra-umc.project.json", "HYDRA-UMC"),
    "ARMOR": ("armor.project.json", "ARMOR-"),
}
BANNER_LINES = 12
_URTC_NAME = re.compile(r"(?<![A-Za-z0-9_-])URTC(?:-[A-Z0-9]+)*(?![A-Za-z0-9_])")
_NAME = re.compile(r"(?:URTC|HYDRA-UMC|ARMOR|A\.R\.M\.O\.R)[A-Za-z0-9.-]*|<REPO>")


def load(registry: Path = REGISTRY) -> dict[str, Any]:
    data = json.loads(registry.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("files"), list):
        raise ValueError("the registry must be an object with a list under 'files'")
    return data


def normalise(text: str, repository: str | None, kind: str) -> str:
    """The text as it is compared: newlines only; with a repository, its name written ``<REPO>``; for ``same_after_banner`` any family or project
    name in the first lines (the banner of the file) is ignored too."""
    text = text.replace("\r\n", "\n").rstrip("\n")
    if repository:
        text = text.replace(repository, "<REPO>")
    if kind == "same_after_banner":
        lines = text.split("\n")
        lines[:BANNER_LINES] = [_NAME.sub("<NAME>", line) for line in lines[:BANNER_LINES]]
        text = "\n".join(lines)
    return text


def fingerprints(text: str, repository: str, kind: str) -> set[str]:
    """Two readings of a text, as it is and with the name of its repository as a placeholder: two texts are the same when they share one
    (a source may name another repository on purpose, and a copy names its own)."""
    return {hashlib.sha256(normalise(text, name, kind).encode("utf-8")).hexdigest() for name in (None, repository)}


def read(path: Path) -> str | None:
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def family_repositories(workspace: Path, family: str) -> list[Path]:
    manifest, prefix = FAMILIES[family]
    if not workspace.is_dir():
        return []
    return sorted(p for p in workspace.iterdir() if p.is_dir() and p.name.startswith(prefix) and (p / manifest).is_file())


def source_text(workspace: Path, entry: dict[str, Any], family: str) -> tuple[str, str | None]:
    """(name of the repository holding the source, its text or None when it is not there)."""
    source = entry["sources"].get(family)
    if source is None:
        return "", None
    return source["repo"], read(workspace / source["repo"] / source["path"])


def check_registry_shape(data: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for entry in data["files"]:
        path = entry.get("path", "?")
        if path in seen:
            problems.append(f"{path}: listed twice")
        seen.add(path)
        if entry.get("kind") not in KINDS:
            problems.append(f"{path}: kind must be one of {', '.join(KINDS)}")
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            problems.append(f"{path}: say why the file is, or is not, the same in the families (reason)")
        sources = entry.get("sources")
        if not isinstance(sources, dict) or "URTC" not in sources:
            problems.append(f"{path}: the URTC source is required")
            continue
        for family in entry.get("same_in", []):
            if family not in sources:
                problems.append(f"{path}: same_in names {family}, which has no source")
        if entry.get("kind") != "ecosystem" and len(entry.get("same_in", [])) < 2:
            problems.append(f"{path}: a file that is the same in the families must name at least two (same_in)")
        for family in sources:
            if family not in FAMILIES:
                problems.append(f"{path}: unknown family {family}")
    return problems


def check_own_side(data: dict[str, Any], root: Path = ROOT) -> list[str]:
    """The registry against this repository: the list of the set and the hash of every URTC source."""
    problems = check_registry_shape(data)
    in_set = {e["path"] for e in data["files"] if e.get("in_set")}
    for relative in devtools_set.shared_files(root / "files"):
        if relative not in in_set:
            problems.append(f"{relative}: it is in files/ and not in the registry")
    for entry in data["files"]:
        path = entry["path"]
        if entry.get("in_set"):
            if path not in devtools_set.shared_files(root / "files"):
                problems.append(f"{path}: the registry says it is in the set and files/ does not hold it")
                continue
            current = devtools_set.digest(devtools_set.canonical_text(path, root / "files"))
        else:
            text = read(root / entry["sources"]["URTC"]["path"])
            if text is None:
                problems.append(f"{path}: the URTC source {entry['sources']['URTC']['path']} is missing")
                continue
            current = devtools_set.digest(text)
        if entry.get("urtc_sha256") != current:
            problems.append(f"{path}: the hash in the registry is not the one of the file (run: python tools/tooling_registry.py update)")
    return problems


def check_across(data: dict[str, Any], workspace: Path) -> tuple[list[str], list[str], int]:
    """(failures, notes, comparisons made): the sources that must be equal, compared when the repositories are next to this one."""
    failures: list[str] = []
    notes: list[str] = []
    compared = 0
    for entry in data["files"]:
        same_in = entry.get("same_in", [])
        prints: dict[str, set[str]] = {}
        for family in same_in:
            repo, text = source_text(workspace, entry, family)
            if text is None:
                notes.append(f"{entry['path']}: the {family} source is not next to this repository, not compared")
                continue
            prints[family] = fingerprints(text, repo, entry["kind"])
        compared += len(prints) > 1
        first = next(iter(prints.values()), set())
        if any(not (first & other) for other in prints.values()):
            failures.append(f"{entry['path']}: the sources of {', '.join(sorted(prints))} are not the same text")
    return failures, notes, compared


def carriers(workspace: Path, entry: dict[str, Any], family: str) -> tuple[int, int, int]:
    """(repositories of the family that carry the same text as its source, carry another text, do not carry the file)."""
    repo, text = source_text(workspace, entry, family)
    if text is None:
        return 0, 0, 0
    wanted = fingerprints(text, repo, entry["kind"])
    same = other = absent = 0
    for repository in family_repositories(workspace, family):
        own = read(repository / entry["path"])
        if own is None:
            absent += 1
        elif family == "URTC" and entry.get("in_set"):
            # the set writes the name of the repository where the canonical file says <REPO>; as in the comparison of URTC-DOCS, any
            # name of a repository of the family counts as the placeholder
            rendered = devtools_set.render_for(repository.name, entry["path"], ROOT / "files")
            if _URTC_NAME.sub("<REPO>", normalise(own, None, "identical")) == _URTC_NAME.sub("<REPO>", normalise(rendered, None, "identical")):
                same += 1
            else:
                other += 1
        elif fingerprints(own, repository.name, entry["kind"]) & wanted:
            same += 1
        else:
            other += 1
    return same, other, absent


def report(data: dict[str, Any], workspace: Path) -> list[str]:
    lines = [f"{'file':36} {'kind':18} " + " ".join(f"{family:>22}" for family in FAMILIES)]
    for entry in data["files"]:
        cells = []
        for family in FAMILIES:
            if family not in entry["sources"]:
                cells.append(f"{'-':>22}")
                continue
            same, other, absent = carriers(workspace, entry, family)
            cells.append(f"{f'{same} same/{other} other/{absent} none':>22}")
        lines.append(f"{entry['path']:36} {entry['kind']:18} " + " ".join(cells))
        equal = ", ".join(entry.get("same_in", [])) or "no family"
        lines.append(f"    the same text in: {equal}. {entry['reason']}")
    return lines


def update(data: dict[str, Any], root: Path = ROOT, registry: Path = REGISTRY) -> int:
    changed = 0
    for entry in data["files"]:
        if entry.get("in_set"):
            current = devtools_set.digest(devtools_set.canonical_text(entry["path"], root / "files"))
        else:
            text = read(root / entry["sources"]["URTC"]["path"])
            if text is None:
                raise SystemExit(f"{entry['path']}: the URTC source is missing")
            current = devtools_set.digest(text)
        if entry.get("urtc_sha256") != current:
            entry["urtc_sha256"] = current
            changed += 1
    registry.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=("check", "report", "update"))
    parser.add_argument("--workspace", type=Path, default=ROOT.parent)
    args = parser.parse_args(argv)
    data = load()
    workspace = args.workspace.resolve()
    if args.command == "update":
        print(f"TOOLING_REGISTRY=WRITTEN {update(data)} hash(es) changed")
        return 0
    if args.command == "report":
        print("\n".join(report(data, workspace)))
        return 0
    problems = check_own_side(data)
    failures, notes, compared = check_across(data, workspace)
    for line in problems + failures:
        print(f"  {line}", file=sys.stderr)
    for line in notes:
        print(f"  note: {line}")
    if problems or failures:
        print(f"TOOLING_REGISTRY=FAIL {len(problems) + len(failures)} problem(s)", file=sys.stderr)
        return 1
    print(f"TOOLING_REGISTRY=PASS {len(data['files'])} files, {compared} cross-family comparisons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
