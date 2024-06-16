#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
PYTHON=$VENV/bin/python

case "$1" in
    server)
        $PYTHON ./test/fuzz_server.py
        ;;
    router)
        $PYTHON ./test/fuzz_router.py
        ;;
    *)
        echo "Usage: $0 {server|router}"
        exit 1
        ;;
esac
