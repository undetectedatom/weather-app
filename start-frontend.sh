#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
NPM_BIN="${NPM_BIN:-npm}"

if ! command -v "$NPM_BIN" >/dev/null 2>&1; then
  echo "Missing required command: $NPM_BIN" >&2
  exit 1
fi

cd "$FRONTEND_DIR"

if [ ! -d node_modules ]; then
  "$NPM_BIN" install
fi

exec "$NPM_BIN" run dev -- --host 0.0.0.0
