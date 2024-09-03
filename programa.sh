#!/bin/bash

PYTHON="$1"
VENV_PATH="$2"
SOURCE_ROOT="$(dirname "$(readlink -f "$BASH_SOURCE")")"

echo "Inicializando programa"

cd $SOURCE_ROOT
$PYTHON -m venv $VENV_PATH
source "$VENV_PATH/bin/activate"
$PYTHON main.py
deactivate
