#!/bin/zsh
set -euo pipefail

project_dir="${0:A:h:h}"
cd "$project_dir"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -r backend/requirements.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  chmod 600 .env
fi

echo "Instalación completada. Ejecuta ./scripts/configure-openai-key.sh"

