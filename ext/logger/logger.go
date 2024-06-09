package logger

import (
	"log"
	"os"
)

func Init() {
	logFilePath := os.Getenv("LOGFILE_PATH")
	if logFilePath == "" {
		logFilePath = "./server.log"
	}

	file, err := os.OpenFile(logFilePath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Error opening log file: %v", err)
	}

	log.SetOutput(file)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
}
