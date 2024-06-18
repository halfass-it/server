#!/bin/bash

# Set important variables
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/halfass-it"
VENV="$CACHE/.venv"
POETRY="$VENV/bin/poetry"
NGINX_CONFIG_DIR="/etc/nginx"
NGINX_SITE_DIR="$NGINX_CONFIG_DIR/sites-available"
NGINX_SITE_ENABLED_DIR="$NGINX_CONFIG_DIR/sites-enabled"

# Create necessary directories
mkdir -p "$CACHE"

# Ensure virtual environment is set up
if [ ! -d "$VENV" ]; then
    $POETRY env use "$VENV"
    $POETRY install
fi

# Function to run the main script
run_main() {
    local host="$1"
    local port="$2"
    local workers="$3"
    local timeout="$4"
    local cache_dir="$5"

    $POETRY run main "$host" "$port" "$workers" "$timeout" "$cache_dir" run
}

# Handle different modes
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
        sudo systemctl start nginx || sudo systemctl restart nginx
        ;;
    *)
        echo "Usage: $0 {server|router}"
        exit 1
        ;;
esac
