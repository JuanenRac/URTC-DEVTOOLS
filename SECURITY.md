# Security Policy 🔒 (URTC-DEVTOOLS)

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x  | ✅ Yes             |

## Reporting a Vulnerability

This repository holds tools that run in the CI and on the computer of whoever builds a repository of the family: the check that no private detail is published, the picture generators, the live panel of the build scripts, the manifest version bumper and the notice that is sent to the central dashboard after a green CI. What a report here can be about:

1. **A check that lets something private through**, for example a secret, an address or a private document name that the documentation policy should have refused.
2. **A script that does more than it says**, for example one that writes outside the repository, runs a command it was not asked to run or leaks an environment variable.
3. **The dashboard notice**: a path by which the token could be printed or sent to another address.
4. **A lock that can be made to match an edited file.**

How to report:

1. **Email**: send a detailed report to `electrohobby3d@gmail.com`. Do not open a public issue for something that exposes a secret.
2. **Response**: initial acknowledgment within 48 hours.

The lock file records SHA-256 hashes to find an edit or a copy that fell behind. It is a consistency check, not a signature: whoever can change a file in a repository can change the lock beside it, and the review of the change is what protects the repository.
