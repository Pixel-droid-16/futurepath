---
name: Imported Python runtimes
description: Replit package detection can fail after a Git release replaces the import-generated runtime metadata.
---

Merge the import-generated runtime module settings into a fetched release's
Replit configuration before installing its dependencies.

**Why:** The release supplied a run command but omitted runtime modules.
Dependency auto-detection then selected a different Python base module and pip
failed against immutable Nix storage. Restoring the imported Python 3.12 module
allowed the normal managed package installation to succeed.

**How to apply:** On imported-branch changes, preserve runtime metadata alongside
release configuration. Validate Replit configuration through the supported
replacement callback; do not work around this by using virtualenvs or modifying
Nix store permissions. Package installation may append duplicate requirements;
preserve the upstream dependency constraints instead of retaining duplicates.
