#!/bin/bash

PYTHON="$1"
VENV_PATH="$2"
SOURCE_ROOT="$(dirname "$(readlink -f "$BASH_SOURCE")")"

echo "Instalando dependências"

cd $SOURCE_ROOT
$PYTHON -m venv $VENV_PATH
source "$VENV_PATH/bin/activate"
python -m pip install -r "$SOURCE_ROOT/requirements.txt"
deactivate
