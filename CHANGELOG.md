# Changelog

All notable changes to this repository are listed here. The version of this repository is the version of the set of shared tools it holds.

## [0.0.4] - The manifest says which version of the shared contracts it needs: mincommon in urtc.project.json is the oldest version of URTC-COMMON among the copies this repository carries, the value the updater compares with what is... (and 4 more changes)

- **The manifest says which version of the shared contracts it needs:** `min_common` in `urtc.project.json` is the oldest version of URTC-COMMON among the copies this repository carries, the value the updater compares with what is installed (a warning only). `tools/min_common.py` of URTC-COMMON checks it and a new copy brings it up to date.

- **More tests for the set tool, the registry and the workflow comparison:** the commands of the set, a copy that is missing, changed or in a different line ending, every shape problem of a registry entry, a source that is gone or whose hash is stale (and the update that repairs it), and the security findings, the drift and the exit codes of the workflow comparison on temporary repositories. The suite has 95 tests.

- **The repository check compares the manifest with what can be computed:** `tools/ci_validate.py` now also runs the shared `tools/sync_manifests.py` offline, which compares the shipped version, the newest released heading of this changelog, the presence of tests and the claimed level of evidence with the manifest. It is part of the shared set of tools, so the copy is pinned by the lock.

- **The shared set carries `tools/sync_manifests.py`:** the check of a manifest against what can be computed about its repository is the same file in the three families and is registered in the tooling registry.
- **The tests of this repository are held to a coverage floor:** the CI measures the code the repository owns (`tools/devtools_set.py`, `tools/tooling_registry.py`, `tools/workflow_templates.py`; 92 percent measured) and fails under 85 percent; the files of the set are left out of the measure because they run, and are tested, in the repositories that carry them (`[tool.coverage.run]` in `pyproject.toml` lists them).

## [0.0.4]

- Build version synchronized with `urtc.project.json` and the repository-native version source.

## [0.0.3] - The full build check compiles only on CI or when allowed: for the stacks that compile (rust, go, android, flutter, firmware-c), tools/buildtest.py asks tools/localbuild.py first (or the same rule inline when a repository has... (and 3 more changes)

- **The full build check compiles only on CI or when allowed:** for the stacks that compile (`rust`, `go`, `android`, `flutter`, `firmware-c`), `tools/build_test.py` asks `tools/local_build.py` first (or the same rule inline when a repository has not taken the helper) and prints `BUILD_TEST=SKIPPED` with exit status 2 on a plain PC, never a pass; `ALLOW_LOCAL_BUILD=1` allows it and a CI runner always may. The light check (`--check`) and the Python, Qt Quick and node stacks are not locked.

- **The host C suites compile only on CI or when allowed:** `tools/run_host_tests.py` asks `tools/local_build.py` first and says SKIPPED (exit status 2) on a plain PC; `ALLOW_LOCAL_BUILD=1` allows it and a CI runner always may.

- **The build check of the repository is one text for the whole family, with a light mode that CI runs:** `tools/build_test.py` is the same file in every repository of the family (taken from the shared set); what used to differ between its seven variants is data in an optional `tools/build_test.json`. `python tools/build_test.py --check` looks at the manifest, the stack and the files the full check needs and compiles the Python sources, builds and runs nothing, and the baseline step of the workflow now runs it.
- **`tools/workflow_templates.py` compares the workflows of the repositories that sit side by side:** it checks that every third-party action is pinned to a commit hash, that every workflow has a top-level `permissions:` block and none runs on `pull_request_target`, and it reports the copies of one workflow that differ (after comments, schedules and repository names are removed) and every action pinned to more than one hash. `--strict` makes a drift fail too.

## [0.0.2] - The set shared by the family has the host-test executor, three more files, a composite action for the baseline steps and a registry of the shared tooling, and its CI runs a type check

- **The executor of the host tests of the firmware is in the set** (`tools/run_host_tests.py`, with the data file `tools/host_tests.json` that each repository keeps itself): ctest where cmake is installed, direct compiler calls elsewhere, sanitizers, static analysis, coverage floor and the run through WSL. It is carried by the three firmware repositories of the family and registered as an ecosystem file in the registry (the other families test their firmware another way).

- **Three more files in the set, and one text for the version bumper** (`test.sh`, `test.bat`, `tools/universal_readme_check.py`; `bump_manifest_version.py` finds the manifest of its family by name and carries the native-file rules of the HYDRA-UMC family, so URTC and HYDRA-UMC share one text). The registry lists them and `status_lights.py` and `_doc_policy.py` now say why they stay different between the families.

- **A composite action for the baseline steps of every workflow** (`files/.github/actions/urtc-baseline/action.yml`, one more file of the set, with its lock and the check of drift): set up Python, validate the project (`tools/ci_validate.py`) and compile the Python sources, written once instead of in the ten workflows. A repository checks itself out and calls it with `uses: ./.github/actions/urtc-baseline`; what is its own stays in its workflow. It was tried in one repository first.

- **A registry of the tooling the families share** (`tools/tooling_registry.json` and `tools/tooling_registry.py`): for each shared file, where URTC, HYDRA-UMC and A.R.M.O.R. keep their source, whether the text is the same in them (as it is, or apart from the banner) or belongs to the family, why, and the SHA-256 of the URTC source. `check` fails when the registry and `files/` disagree, and, with the repositories of the other families next to this one, when two sources that must be equal differ; `report` counts how many repositories of each family carry the same text as the source; `update` writes the hashes. Nothing is written to another repository.

### Changed
- The CI now runs a type check (`mypy`, pinned) over the tools and the tests of this repository; the copies of the shared picture tools, which are not edited here, are left out of it (a `[tool.mypy]` section in `pyproject.toml` says so).
- The status-light check states in every `zip()` whether its lengths must match, so the copy each repository carries is clean for the stricter linter of the other families; the behaviour is the same.

## [0.0.2]

- Build version synchronized with `urtc.project.json` and the repository-native version source.

## [0.0.1]

### Added
- The shared repository tools as a versioned set: the canonical copy of the documentation-policy check, the README-parity check, the check for versioned files named like a Windows path, the picture generators of the README (architecture and repository structure), the live panel of the build and test scripts, the manifest version bumper, the status-light check and the notice to the central dashboard (`files/`).
- `tools/devtools_set.py`: lists the set with the SHA-256 of each file and checks that the copies this repository carries itself are the canonical files.
- `tools/devtools.lock.json`: the lock this repository carries like any other, written by `tools/sync_repo_tools.py` of URTC-DOCS (the version of the set and the SHA-256 of each file).
- Documentation of the lock format, of how a repository takes the set and of how a new version of the set is made (`docs/`).
- README in eight languages, repository check, tests and the CI workflow.
