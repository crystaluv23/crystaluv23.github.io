#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec hugo server \
  --bind 127.0.0.1 \
  --baseURL http://localhost:1313/ \
  --port 1313 \
  --buildDrafts \
  --disableFastRender \
  --renderToMemory \
  --navigateToChanged
