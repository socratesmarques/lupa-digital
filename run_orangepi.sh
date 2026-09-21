#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

PYTHON="./.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    PYTHON="$(command -v python3)"
fi

# Tenta executar primeiro como usuário normal.
# Em muitas imagens isso é suficiente para acessar GPIO.
if "$PYTHON" main.py; then
    exit 0
fi

echo
echo "A execução normal falhou."
echo "Se o problema for permissão de GPIO, tente:"
echo
echo "sudo -E env DISPLAY=\"$DISPLAY\" XAUTHORITY=\"${XAUTHORITY:-$HOME/.Xauthority}\" \"$PYTHON\" main.py"
