<!--
=============================================================================
URTC-DEVTOOLS - The lock file
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE
=============================================================================
-->

# The lock file

A repository that takes the shared tools carries `tools/devtools.lock.json`. It says which version of the set the copies came from and what each copy looked like when it was taken.

```json
{
  "schema": 1,
  "source": "URTC-DEVTOOLS",
  "version": "0.0.1",
  "files": {
    ".github/workflows/dashboard-dispatch.yml": "<sha256>",
    "tools/_doc_policy.py": "<sha256>"
  }
}
```

* `version` is the version of this repository when the set was taken (the version of the manifest, `urtc.project.json`).
* `files` lists every shared file the repository carries, with the SHA-256 of the file **as it sits in that repository**. The name of the repository is written inside some of the files, so the hash differs from one repository to the next; line endings are read as newlines, so Windows and Linux agree.
* The file is plain JSON with sorted keys, so a new lock after a new version shows only what changed.

## What is checked

`python tools/check_repo_tools.py` in URTC-DOCS reads the lock of every repository that has one:

| Finding | Meaning |
|---|---|
| `edited after the set was taken` | A copy no longer has the hash of the lock: someone changed it by hand. |
| `in the lock but missing` | A file the lock lists is gone. |
| `a shared file that the lock does not list` | A shared file was added without taking the set. |
| `the lock says set X, URTC-DEVTOOLS is at Y` | The copy fell behind. Only checked when URTC-DEVTOOLS is next to the repositories. |
| `cannot be read` | The lock is not valid JSON or has another schema. |

A repository without a lock is not an error yet: the family moves to the lock one repository at a time. The check that compares each copy with the template (or with the other repositories) keeps running next to it.

## What is not needed

The lock is a file of the repository. Reading and checking it needs no network and no other checkout, so every repository stays buildable and checkable with its own checkout, as before.
