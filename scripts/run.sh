#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
POETRY=$VENV/bin/poetry
LOGS_DIR="$CACHE/logs"
$POETRY run main "127.0.0.1" "1339" "1024" "60" "$LOGS_DIR" run
