#!/bin/sh

echo '{"data": {"auth": "username", "command": "ping"}}' | nc localhost 1339
