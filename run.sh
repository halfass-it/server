
CACHE="$HOME/.cache/server/logs"
mkdir -p "$CACHE"
LOGFILE_PATH="$HOME/.cache/server/log/$(date +%Y-%m-%d).log"
SERVER_ADDRESS="127.0.0.1:8080"
go run main.go -start