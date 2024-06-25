#!/bin/bash

CACHE="$XDG_CACHE_HOME/halfass-it/auth_server"
VENV="$CACHE/.venv"
POETRY="$VENV/bin/poetry"
if [ ! -d "$VENV" ]; then
    $POETRY env use "$VENV"
    $POETRY install
fi
$POETRY run main run
