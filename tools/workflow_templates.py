#!/usr/bin/env python3
# =============================================================================
# URTC-DEVTOOLS - tools/workflow_templates.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Compare the workflows that the repositories of the family keep as copies of one template.

A central bot writes the workflow templates into every repository, so nothing else notices when one copy
drifts from the others. This tool reads the repositories that sit side by side and reports two things:

* ``security``: every ``uses:`` of a third-party action is pinned to a full commit hash, every workflow has a
  top-level ``permissions:`` block and none of them runs on ``pull_request_target``;
* ``drift``: the workflows with the same file name are compared after the parts that legitimately differ
  between repositories are removed (comments, schedules, the language list of the code scan, the names of the
  repository); the copies are grouped by their text and every group beyond the first is reported, and so is every
  action that is pinned to more than one commit hash across the family.

    python tools/workflow_templates.py check [--workspace DIR]    # exit 1 on a security finding
    python tools/workflow_templates.py report [--workspace DIR]   # the drift as a table, always exit 0
    python tools/workflow_templates.py check --strict             # exit 1 on a drift too

Nothing is written. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "urtc.project.json"
USES = re.compile(r"^\s*-?\s*uses:\s*(\S+)")
SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
CRON = re.compile(r"^\s*-\s*cron:")
LANGUAGE = re.compile(r'^\s*-\s*"?(javascript-typescript|python|c-cpp|actions|java-kotlin)"?\s*$')


def repositories(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.iterdir() if (p / MANIFEST).is_file() and (p / ".github" / "workflows").is_dir())


def workflows(repo: Path) -> dict[str, str]:
    folder = repo / ".github" / "workflows"
    return {p.name: p.read_text(encoding="utf-8").replace("\r\n", "\n") for p in sorted(folder.glob("*.yml"))}


def security_findings(name: str, text: str) -> list[str]:
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        match = USES.match(line)
        if not match:
            continue
        target = match.group(1)
        if target.startswith("./") or target.startswith("docker://"):
            continue
        if not SHA.match(target):
            found.append(f"{name}:{number}: {target} is not pinned to a commit hash")
    if not re.search(r"(?m)^permissions:", text):
        found.append(f"{name}: no top-level permissions block")
    if re.search(r"(?m)^\s*pull_request_target\s*:", text):
        found.append(f"{name}: runs on pull_request_target")
    return found


def normalized(text: str, repo_name: str) -> str:
    kept = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or CRON.match(line) or LANGUAGE.match(line):
            continue
        kept.append(line.replace(repo_name, "<repo>").rstrip())
    return "\n".join(kept)


def drift(all_workflows: dict[str, dict[str, str]]) -> list[str]:
    """The lines of the report: one per file name whose copies differ, one per action pinned to several hashes."""
    lines = []
    by_file: dict[str, dict[str, list[str]]] = {}
    for repo, files in all_workflows.items():
        for name, text in files.items():
            digest = hashlib.sha256(normalized(text, repo).encode()).hexdigest()[:10]
            by_file.setdefault(name, {}).setdefault(digest, []).append(repo)
    for name, groups in sorted(by_file.items()):
        if len(groups) > 1 and sum(len(r) for r in groups.values()) > 1:
            shown = "; ".join(f"{digest}: {', '.join(repos)}" for digest, repos in sorted(groups.items()))
            lines.append(f"{name}: {len(groups)} different texts ({shown})")
    pins: dict[str, dict[str, set[str]]] = {}
    for repo, files in all_workflows.items():
        for text in files.values():
            for line in text.splitlines():
                match = USES.match(line)
                if match and "@" in match.group(1) and not match.group(1).startswith("./"):
                    action, _, ref = match.group(1).partition("@")
                    pins.setdefault(action, {}).setdefault(ref, set()).add(repo)
    for action, refs in sorted(pins.items()):
        if len(refs) > 1:
            lines.append(f"{action}: pinned to {len(refs)} hashes ({', '.join(sorted(r[:10] for r in refs))})")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("check", "report"))
    parser.add_argument("--workspace", type=Path, default=ROOT.parent)
    parser.add_argument("--strict", action="store_true", help="a drift fails the check too")
    args = parser.parse_args(argv)
    repos = repositories(args.workspace)
    if not repos:
        print("WORKFLOW_TEMPLATES=SKIP no repository with workflows next to this one")
        return 0
    everything = {repo.name: workflows(repo) for repo in repos}
    findings = [f"{repo}/{item}" for repo, files in everything.items() for name, text in files.items()
                for item in security_findings(name, text)]
    differences = drift(everything)
    for line in findings:
        print("SECURITY", line)
    for line in differences:
        print("DRIFT", line)
    failed = bool(findings) or (args.strict and bool(differences))
    if args.command == "report":
        failed = False
    print(f"WORKFLOW_TEMPLATES={'FAIL' if failed else 'PASS'} repositories={len(repos)} security={len(findings)} drift={len(differences)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
