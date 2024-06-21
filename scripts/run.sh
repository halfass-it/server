#!/bin/bash

CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/halfass-it"
VENV="$CACHE/.venv"
POETRY="$VENV/bin/poetry"
NGINX_CONFIG_DIR="/etc/nginx"
NGINX_SITE_DIR="$NGINX_CONFIG_DIR/sites-available"
NGINX_SITE_ENABLED_DIR="$NGINX_CONFIG_DIR/sites-enabled"

mkdir -p "$CACHE"
if [ ! -d "$VENV" ]; then
    $POETRY env use "$VENV"
    $POETRY install
fi

run_main() {
    local host="$1"
    local port="$2"
    local workers="$3"
    local timeout="$4"
    local cache_dir="$5"

    $POETRY run main "$host" "$port" "$workers" "$timeout" "$cache_dir" run
}

memcached -l 127.0.0.1 -p 11211 -m 64 -d
case "$1" in
    server)
        run_main "127.0.0.1" "1337" "1024" "60" "$CACHE"
        ;;
    router)
        run_main "127.0.0.1" "1337" "1024" "60" "$CACHE" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "1338" "1024" "60" "$CACHE" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "1339" "1024" "60" "$CACHE" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "1340" "1024" "60" "$CACHE" &>/dev/null &

        sudo cp ./router/nginx.conf "$NGINX_CONFIG_DIR/nginx.conf"
        sudo cp ./router/default.conf "$NGINX_SITE_DIR/default.conf"
        sudo ln -sf "$NGINX_SITE_DIR/default.conf" "$NGINX_SITE_ENABLED_DIR/default.conf"
        sudo systemctl restart nginx || sudo systemctl start nginx
        ;;
    *)
        echo "Usage: $0 {server|router}"
        exit 1
        ;;
esac
