#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
exec python3 -m http.server "${CYBERCHIEF_EPISODE_PORT:-9130}" --bind 127.0.0.1
