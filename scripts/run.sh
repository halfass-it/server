#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
POETRY=$VENV/bin/poetry
$POETRY run main "127.0.0.1" "1337" "1024" "60" run
