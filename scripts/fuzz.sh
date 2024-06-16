#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
PYTHON=$VENV/bin/python

case "$1" in
    server)
        $PYTHON ./fuzz/fuzz_server.py
        ;;
    router)
        $PYTHON ./fuzz/fuzz_router.py
        ;;
    *)
        echo "Usage: $0 {server|router}"
        exit 1
        ;;
esac
