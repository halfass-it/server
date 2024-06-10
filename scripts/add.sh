#!/bin/sh

CACHE="$XDG_CACHE_HOME/llmpeg"
mkdir -p $CACHE
VENV=$CACHE/.venv
POETRY=$VENV/bin/poetry
$POETRY add $1
