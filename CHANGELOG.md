# Changelog

All notable changes to this repository are listed here. The version of this repository is the version of the set of shared tools it holds.

## [Unreleased]

### Changed
- The CI now runs a type check (`mypy`, pinned) over the tools and the tests of this repository; the copies of the shared picture tools, which are not edited here, are left out of it (a `[tool.mypy]` section in `pyproject.toml` says so).
- The status-light check states in every `zip()` whether its lengths must match, so the copy each repository carries is clean for the stricter linter of the other families; the behaviour is the same.

## [0.0.1]

### Added
- The shared repository tools as a versioned set: the canonical copy of the documentation-policy check, the README-parity check, the check for versioned files named like a Windows path, the picture generators of the README (architecture and repository structure), the live panel of the build and test scripts, the manifest version bumper, the status-light check and the notice to the central dashboard (`files/`).
- `tools/devtools_set.py`: lists the set with the SHA-256 of each file and checks that the copies this repository carries itself are the canonical files.
- `tools/devtools.lock.json`: the lock this repository carries like any other, written by `tools/sync_repo_tools.py` of URTC-DOCS (the version of the set and the SHA-256 of each file).
- Documentation of the lock format, of how a repository takes the set and of how a new version of the set is made (`docs/`).
- README in eight languages, repository check, tests and the CI workflow.
