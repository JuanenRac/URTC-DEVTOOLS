# Contributing to URTC-DEVTOOLS 🧰

This repository holds the shared repository tools of the URTC family as one versioned set. A contribution that makes a tool more correct, or makes a check clearer about what it found, is the most useful kind.

## Technology Stack
- **The set**: Python 3.10+ and one GitHub Actions workflow, standard library only (`files/`).
- **This repository's own checks**: `tools/devtools_set.py`, `tools/ci_validate.py` and `unittest` tests.

## Guidelines
1. **`files/` is the source.** Change the file in `files/` and the copy this repository carries (`python tools/devtools_set.py check` fails until they agree). Never edit one copy in another repository: take the set again with `tools/sync_repo_tools.py` of URTC-DOCS.
2. **One version for a batch.** The version of this repository is the version of the set. Raise it once for the whole batch of changes, in the manifest, `pyproject.toml` and the changelog.
3. **A file that exists in the sister projects is not moved here alone.** The same file in all the families, or none (see `docs/TAKING_THE_SET.md`).
4. **A tool does not need the network.** Every repository must stay buildable and checkable with its own checkout.
5. **Eight languages.** The README exists in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese, with the same sections and links; `tools/ci_validate.py` compares them.
6. **Nothing private in public files.** No dates, no names of private notes, no tracking codes, no secrets, no addresses of a real installation.
7. **Tests.** `python -m unittest discover -s tests` must pass, and `URTC_CI=1 python tools/ci_validate.py` must print `CI_VALIDATION=PASS`. Use `build-test.sh` / `build-test.bat` to check without changing the version; `build.sh` / `build.bat` raise it.
8. **Documentation language.** The files in `docs/` are written in English only, on purpose: they are technical reference for developers, kept in one language so that a change is made once and cannot drift between eight copies. The README of each repository is the part that is translated into the eight languages.
