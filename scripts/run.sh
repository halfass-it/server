#!/bin/bash

# Set important variables
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/halfass-it"
VENV="$CACHE/.venv"
POETRY="$VENV/bin/poetry"
LOGS_DIR="$CACHE/logs"
NGINX_CONFIG_DIR="/etc/nginx"
NGINX_SITE_DIR="$NGINX_CONFIG_DIR/sites-available"
NGINX_SITE_ENABLED_DIR="$NGINX_CONFIG_DIR/sites-enabled"

# Create necessary directories
mkdir -p "$LOGS_DIR"

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
    local log_dir="$5"

    $POETRY run main "$host" "$port" "$workers" "$timeout" "$log_dir" run
}

# Handle different modes
case "$1" in
    server)
        run_main "127.0.0.1" "1337" "1024" "60" "$LOGS_DIR"
        ;;
    router)
        run_main "127.0.0.1" "1337" "1024" "60" "$LOGS_DIR" &>/dev/null &
        run_main "127.0.0.1" "1338" "1024" "60" "$LOGS_DIR" &>/dev/null &
        run_main "127.0.0.1" "1339" "1024" "60" "$LOGS_DIR" &>/dev/null &
        run_main "127.0.0.1" "1340" "1024" "60" "$LOGS_DIR" &>/dev/null &

        # Copy Nginx configuration
        sudo cp ./build/nginx.conf "$NGINX_CONFIG_DIR/nginx.conf"
        sudo cp ./build/default.conf "$NGINX_SITE_DIR/default.conf"

        # Enable the default site
        sudo ln -sf "$NGINX_SITE_DIR/default.conf" "$NGINX_SITE_ENABLED_DIR/default.conf"

        # Restart Nginx
        sudo systemctl enable nginx
        sudo systemctl start nginx
        sudo systemctl restart nginx
        ;;
    *)
        echo "Usage: $0 {server|router}"
        exit 1
        ;;
esac