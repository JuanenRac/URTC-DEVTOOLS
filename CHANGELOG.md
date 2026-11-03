# Changelog

All notable changes to this repository are listed here. The version of this repository is the version of the set of shared tools it holds.

## [Unreleased]

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
