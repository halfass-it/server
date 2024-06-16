#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
PYTHON=$VENV/bin/python

$PYTHON ./test/fuzz.py