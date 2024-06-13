#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV="$CACHE/.venv"
POETRY="$VENV/bin/poetry"
$POETRY remove "$1"
