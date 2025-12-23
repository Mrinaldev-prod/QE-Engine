#!/usr/bin/env bash
set -euo pipefail

HOOK_SRC="$(pwd)/scripts/git-hooks/pre-push"
HOOK_DEST="$(pwd)/.git/hooks/pre-push"

if [ ! -d "$(pwd)/.git" ]; then
  echo "This repository doesn't appear to be a git repo (no .git directory). Run this from the repo root."
  exit 1
fi

cp "$HOOK_SRC" "$HOOK_DEST"
chmod +x "$HOOK_DEST"
echo "Installed pre-push hook to .git/hooks/pre-push"
