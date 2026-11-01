<!--
=============================================================================
URTC-DEVTOOLS - Taking the set and making a new version
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE
=============================================================================
-->

# Taking the set, and making a new version

## What the set is

The files under `files/` are the canonical copy of what every repository of the family carries as the same file. In them the name of the repository is written `<REPO>`; when a file is put into a repository the real name is written instead. The list of files is `SHARED_FILES` in `src/urtc_docs/drift.py` of URTC-DOCS, and `tests/test_devtools_set.py` holds the same list, so the two cannot differ without a test failing.

| Group | Files |
|---|---|
| Documentation checks | `tools/_doc_policy.py`, `tools/_readme_parity.py`, `tools/_tracked_names.py` |
| Pictures | `tools/_readme_svg.py`, `tools/make_architecture.py`, `tools/make_structure.py` |
| Scripts | `tools/pretty_run.py`, `bump_manifest_version.py`, `tools/status_lights.py` |
| Workflow | `.github/workflows/dashboard-dispatch.yml` |
| Composite action | `.github/actions/urtc-baseline/action.yml` (the steps every workflow runs first: Python, the validation of the project and the compilation of the sources) |

## Using the composite action

A workflow checks the repository out and then runs the baseline in one step; what is its own (linting, type checks, tests) stays in the workflow:

```yaml
      - name: Check out repository
        uses: actions/checkout@v5
      - name: Baseline (Python, project validation and compilation of the sources)
        uses: ./.github/actions/urtc-baseline
```

`python-version` (default `3.12`) is the one input. The action is one of the shared files: edited by hand in a repository, or left behind, it is found by the check like any other copy.

## Taking the set into a repository

From URTC-DOCS, with the repositories side by side:

```
python tools/sync_repo_tools.py            # list what would be written
python tools/sync_repo_tools.py --apply    # write the files and every tools/devtools.lock.json
python tools/check_repo_tools.py           # compare the copies and the locks
```

The synchroniser writes the files that differ and then the lock of each repository (the version of this repository and the hash of every file the repository carries). Commit each repository on its own, after its own CI validation passes.

## Making a new version of the set

1. Change the file in `files/` and, in the same change, the copy this repository carries (`python tools/devtools_set.py check` fails until they agree).
2. Raise the version once for the whole batch of changes (the manifest, `pyproject.toml` and the changelog) and run `tools/ci_validate.py`.
3. Give URTC-DOCS the same file in its template while it still holds one (`tests/test_repository.py` compares the two when URTC-DOCS is next to this repository).
4. Take the set into the repositories as above. A repository whose lock names an older version is reported until it does.

## Files shared with other families

Some of the files exist, byte for byte apart from the name, in the repositories of the sister projects. They are not moved by this repository: a change made here alone would give the family two versions of the same file. They move last, together, and only with the agreement of the owners of those repositories.

What is the same, and where each family keeps its source, is written in `tools/tooling_registry.json` (one entry per file: how two sources are compared, the families where the text is the same, the reason when it is not, and the SHA-256 of the URTC source). `tools/tooling_registry.py` reads it:

```
python tools/tooling_registry.py check     # the registry against files/, and the sources that must be equal when the other families are next to this repository
python tools/tooling_registry.py report    # for each file, how many repositories of each family carry the same text as its source
python tools/tooling_registry.py update    # write the hashes of the URTC sources into the registry after a change to files/ (or to a file the registry lists)
```

`check` needs nothing but this repository (the hashes and the list of the set); next to the repositories of the other families it also compares their sources. It never writes to another repository. A new file of the set needs an entry, and the check fails until it has one.

