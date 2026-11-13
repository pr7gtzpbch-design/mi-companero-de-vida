#!/bin/zsh
set -euo pipefail

project_dir="${0:A:h}"
cd "$project_dir"

./scripts/configure-openai-key.sh
echo
echo "Configuración terminada. Puedes cerrar esta ventana."
read -r "?Presiona Enter para cerrar."
