#!/bin/zsh
set -euo pipefail

project_dir="${0:A:h:h}"
cd "$project_dir"

if [[ ! -x .venv/bin/python ]]; then
  echo "Falta la instalación. Ejecuta ./scripts/setup.sh primero." >&2
  exit 1
fi

exec .venv/bin/python -m uvicorn backend.app.main:app \
  --host 127.0.0.1 \
  --port 8000
