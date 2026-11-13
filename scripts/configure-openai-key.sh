#!/bin/zsh
set -euo pipefail

project_dir="${0:A:h:h}"
cd "$project_dir"

echo "Pega tu API key de OpenAI. No se mostrará en pantalla."
read -rs "openai_key?API key: "
echo

if [[ -z "$openai_key" ]]; then
  echo "La clave no puede estar vacía." >&2
  exit 1
fi

umask 077
printf '%s\n' \
  "OPENAI_API_KEY=$openai_key" \
  "OPENAI_MODEL=gpt-6-astra" \
  "COMPANION_DB_PATH=data/companion.db" > .env

unset openai_key
echo "Clave guardada localmente en .env. Git no incluirá este archivo."

