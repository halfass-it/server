#!/bin/sh

CACHE="$XDG_CACHE_HOME/halfass-it"
LOGS=$CACHE/logs

cat $LOGS/*.log | grep 'ERROR' | less