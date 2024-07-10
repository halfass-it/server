#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
VENV=$CACHE/.venv
PYTHON=$VENV/bin/python

case "$1" in
    gateway)
        $PYTHON ./fuzz/fuzz_gateway.py
        ;;
    auth)
        $PYTHON ./fuzz/fuzz_auth.py
        ;;
    game)
        $PYTHON ./fuzz/fuzz_game.py
        ;;
    router)
        $PYTHON ./fuzz/fuzz_router.py 
        ;;
    *)
        echo "Usage: $0 {router|gateway|auth|game}"
        exit 1
        ;;
esac
