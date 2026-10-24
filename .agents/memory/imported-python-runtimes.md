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

For non-interactive setup hooks, explicitly direct pip into the project's
managed `.pythonlibs` prefix rather than relying on an interactive package
wrapper to select the destination.

**Why:** Even with the correct runtime modules present, a plain
`python -m pip install` in the post-merge runner targets immutable Nix storage.
An explicit project-local prefix preserves already-installed dependencies and
allows newly merged requirements to install without bypassing system protections.

**How to apply:** Use pip's project-local `--prefix` option in the setup hook,
not `--break-system-packages`; keep the existing managed Python search paths.
