#!/usr/bin/env bash
# Reconcile the existing Python project after an isolated task is merged.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Use Replit's managed Python environment, without a virtualenv or new stack.
python -m pip install --disable-pip-version-check --no-input \
  --prefix "$PWD/.pythonlibs" -r requirements.txt
python scripts/build_frontend.py
python -m compileall -q backend

# Do not import the app, touch its database, call providers, or run tests here.
# The workflow reconciler starts/restarts the existing app after setup succeeds.
