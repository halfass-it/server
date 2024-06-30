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
    local server="$6"

    $POETRY run $server "$host" "$port" "$workers" "$timeout" "$cache_dir" run
}

case "$1" in
    gateway)
        run_main "127.0.0.1" "5000" "1024" "60" "$CACHE" "gateway_server"
        ;;
    auth)
        run_main "127.0.0.1" "6000" "1024" "60" "$CACHE" "auth_server"
        ;;
    game)
        run_main "127.0.0.1" "7000" "1024" "60" "$CACHE" "game_server"
        ;;
    router)
        run_main "127.0.0.1" "5001" "1024" "60" "$CACHE" "gateway_server" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "5002" "1024" "60" "$CACHE" "gateway_server" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "5003" "1024" "60" "$CACHE" "gateway_server" &>/dev/null &
        sleep 1
        run_main "127.0.0.1" "5004" "1024" "60" "$CACHE" "gateway_server" &>/dev/null &
        sleep 1
        run main "127.0.0.1" "6001" "1024" "60" "$CACHE" "auth_server" &>/dev/null &
        sleep 1
        run main "127.0.0.1" "6002" "1024" "60" "$CACHE" "auth_server" &>/dev/null &
        sleep 1
        run main "127.0.0.1" "7001" "1024" "60" "$CACHE" "auth_server" &>/dev/null &
        sleep 1
        run main "127.0.0.1" "7002" "1024" "60" "$CACHE" "game_server" &>/dev/null &
        sleep 1

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
