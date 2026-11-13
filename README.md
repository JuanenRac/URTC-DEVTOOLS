<p align="center">
  <img src="images/URTC_DEVTOOLS_BANNER.svg" alt="URTC-DEVTOOLS banner" width="100%">
</p>

# 🧰 URTC-DEVTOOLS

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### The shared repository tools of the URTC family as one versioned set, with a lock file in each repository

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Python%20%2B%20JSON-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.6-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Tests-131-2ea44f.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** this repository holds the 18 files that the repositories of the family carry as the same copy, a small tool that lists them and checks the copies this repository carries itself, tests and documentation. All of it runs and is tested in CI. The lock file is written and checked by URTC-DOCS; every repository of the family carries a lock, and nothing here has run on hardware.

---

## 📋 At a glance

| | |
|---|---|
| Version | `0.0.6` |
| Maturity | Scaffolding |
| Tests | 131 (`python -m unittest discover -s tests`) |
| Stack | Python / GitHub Actions / JSON |
| Target | The PC of the person using it |
| On real hardware | Not applicable: nothing here runs on hardware |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

🟢 done and verified · 🟡 works, with known limits · 🟠 half done or not verified · 🔴 not done or not working. Nothing is green if it never ran on real hardware.

| Part | Status | What the repository can show |
| --- | :---: | --- |
| Software | 🟡 | The set, its listing and its check; run only on a computer. |
| Tests | 🟡 | The test suite passes in the CI on every push. |
| Security | 🟠 | The lock records SHA-256 hashes to find an edit or a copy that fell behind; it is a consistency check, not a signature. |
| Documentation | 🟡 | README in eight languages and the lock format; the translations were not reviewed by native speakers. |

## 🎯 Overview

The tools that every repository of the family carries as the same copy, gathered in one place and given a version:

* [`files/`](files): the canonical copy of the 18 shared files (the documentation-policy and README-parity checks, the picture generators, the live panel of the build scripts, the manifest version bumper, the status-light check and the dashboard notice). The name of the repository is written `<REPO>` and replaced when a file is put into a repository.
* The **version of this repository is the version of the set**; the [changelog](CHANGELOG.md) says what changed in each version.
* A **lock file** in each repository, `tools/devtools.lock.json`, written by `tools/sync_repo_tools.py` of URTC-DOCS: the version of the set and the SHA-256 of every copy. `tools/check_repo_tools.py` finds a copy that was edited by hand and, when this repository is next to the others, a copy that fell behind. See [the lock format](docs/LOCK_FORMAT.md).
* Every repository stays buildable and checkable with its own checkout: the lock is a file of the repository and nothing needs the network.

## 🧩 Role in URTC

URTC-DEVTOOLS is where the shared tools get a name and a version. A change to one of them used to be a change in about ten repositories with nothing saying which version each one carried; now the set has a version, each repository says which one it took, and a copy that was edited or left behind is reported. It changes nothing in the repositories by itself: URTC-DOCS puts the files in and writes the locks, one repository at a time.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="URTC-DEVTOOLS architecture: who takes the set, what it holds and what it writes" width="100%">
</p>

How the parts of this repository fit together: who takes the set, what it holds and what it writes in each repository. The picture is drawn from `docs/architecture.json` and checked against the code.

## 🚀 Quick start

**Requirements:** Python 3.10 or newer; nothing else.

```bash
python tools/devtools_set.py list            # the version of the set and the SHA-256 of each file
python tools/devtools_set.py check           # the copies this repository carries are the canonical files
python tools/tooling_registry.py check       # the registry of the tooling the families share: hashes and equal sources
python -m unittest discover -s tests         # the tests
python tools/sync_repo_tools.py --apply      # from URTC-DOCS: put the set and the locks into the repositories next to it
```

## 🧪 Testing

The suite has 131 tests (`python -m unittest discover -s tests`). They check that `files/` holds exactly the shared files, that each one is valid and renders with the name of a repository, that an edited or missing copy is found, that the lock of this repository matches its files and version, and the manifest, the changelog and the documents. One test compares `files/` with the template of URTC-DOCS and skips when that repository is not next to this one. The lock logic itself is tested in URTC-DOCS.

## 🏗️ Build & Release

`build.sh` / `build.bat` raise the version of the set, check the copies and run the tests; `build-test.sh` / `build-test.bat` check without changing any version; `run.sh` / `run.bat` list the set. A new version of the set is made by changing a file in `files/` and its copy, raising the version once for the whole batch and taking the set into the repositories; see [the guide](docs/TAKING_THE_SET.md).

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of URTC-DEVTOOLS" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
URTC-DEVTOOLS/
├── files/                                     the 18 canonical files, at the path they have in every repository
├── tools/                                     the check of the set, the repository validation and the copies this repository carries
├── tests/                                     unit tests of the set, of the lock and of the repository
├── docs/                                      the lock format and how to take the set
├── .github/                                   CI, nightly comparison, issue and pull-request templates
├── images/                                    banner and the pictures of this README
├── build.sh build.bat                         build scripts
├── build-test.sh build-test.bat               build and test scripts that change nothing in the repository
├── test.sh test.bat                           run the tests
├── run.sh run.bat                             list the set, or check it
├── urtc.project.json                          manifest: version, role, maturity and build command
├── CHANGELOG.md                               what changed in each version
├── SECURITY.md SUPPORT.md LICENSE             security policy, support and license
├── CONTRIBUTING.md CODE_OF_CONDUCT.md         how to contribute and the code of conduct
├── .gitattributes .gitignore                  Git settings
├── bump_version.py bump_manifest_version.py   scripts that raise the version
└── pyproject.toml ruff.toml                   project metadata and lint settings
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* The lock is written and checked by URTC-DOCS (`tools/sync_repo_tools.py` and `tools/check_repo_tools.py`); every repository of the family carries one now (`tools/devtools.lock.json`).
* URTC-DOCS still holds its own template, which the synchroniser reads; the two are compared by a test when they are next to each other.
* The files that exist in the sister projects are not moved here alone: the same file in all the families, or none.
* Nothing here has run on hardware; the tools run on a computer.

**Next**

* Make this repository the source the synchroniser reads, and retire the template of URTC-DOCS.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

URTC is made of independent repositories, each with its own version, tests and README. This is the family, by group:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware of the tool-head board (25 tool profiles, CAN bootloader) and the CAN protocol reference.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - the CAN protocol written once as data (specification, generated tables, conformance vectors) and the code the programs share.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - desktop tool that updates the board firmware over CAN or over SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - gateway in front of the CAN bus: lets only listed identifiers through, limits their rate and asks for a session key.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - hardware-independent C logic and command protocol for a tool rack with pre-heating and lifecycle tracking.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - desktop live CAN-bus tester that shows the controls and telemetry of the tool profile a board reports.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - sensor-frame protocol in C and a Python thermal/RGB companion for an inspection tool head.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - browser app that flashes and tests the board over Web Serial and SLCAN, with nothing to install.
* **Ecosystem Operations:**
  * **URTC-DEVTOOLS** (this repository) - the shared repository tools of the family as one versioned set, with a lock file that tells a copy that was edited from one that fell behind.
  * [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) - architecture, interfaces, security baseline and generated catalogue of the ecosystem, plus the tools that compare all repositories.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - desktop tool that detects, installs and updates the repositories of the URTC family, one explicit action at a time.

**Sister projects (independent, with the same base and tools):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - sister project: the documentation hub of HYDRA-UMC, an independent ecosystem that shares this one's base and tools
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - sister project: the documentation hub of A.R.M.O.R., the security ecosystem, also independent and on the same base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - the profile and the status dashboard of all the ecosystems

## 📚 Documentation

Where to read more:

* [The lock format and what is checked](docs/LOCK_FORMAT.md)
* [Taking the set, and making a new version](docs/TAKING_THE_SET.md)
* [Changelog of this repository](CHANGELOG.md)
* [License (GPL-3.0-or-later)](LICENSE)
* Questions, ideas and reports: electrohobby3d@gmail.com

## 🤝 Contributing & Community

* Before a pull request run `URTC_CI=1 python tools/ci_validate.py`: it must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files.
* Do not describe as working on a board what has only been built.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

GPL-3.0-or-later - see [LICENSE](LICENSE).
