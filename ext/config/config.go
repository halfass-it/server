package config

import (
	"os"
)

type Config struct {
	ServerAddress string
	LogFilePath   string
}

func Load() *Config {
	logFilePath := os.Getenv("LOGFILE_PATH")
	if logFilePath == "" {
		logFilePath = "./server.log"
	}

	serverAddress := os.Getenv("SERVER_ADDRESS")
	if serverAddress == "" {
		serverAddress = ":8080"
	}

	return &Config{
		ServerAddress: serverAddress,
		LogFilePath:   logFilePath,
	}
}
