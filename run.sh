
CACHE="$HOME/.cache/server/logs"
mkdir -p "$CACHE"
export LOGFILE_PATH="$HOME/.cache/server/logs/$(date +%Y-%m-%d).log" 
export SERVER_ADDRESS="127.0.0.1:7331"
go run main.go -start