package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

const DEBUG = 0

const LOGFILE_PATH = "./server.log"

func CreateFileIfNotExists(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		file, err := os.Create(path)
		if err != nil {
			fmt.Println("[main]::Error creating log file")
			os.Exit(3)
		}
		file.Close()
	}
}

func StartServer() {
	fmt.Println("[main]::Starting server")
	log.Println("[main]::Starting server")
}

func ConfigServer(args []string) {
	fmt.Println("[main]::Configuring server")
	log.Println("[main]::Configuring server")
}

func main() {
	CreateFileIfNotExists(LOGFILE_PATH)
	// TODO: move this to home cache
	log_file, err := os.OpenFile(LOGFILE_PATH, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("[main]::Error setting up logger")
		os.Exit(4)
	}
	defer log_file.Close()
	log.SetOutput(log_file)

	startFlag := flag.Bool("start", false, "Run the server")
	setupFlag := flag.Bool("setup", false, "Configure the server")

	flag.Parse()

	if *startFlag {
		StartServer()
	}

	if *setupFlag {
		args := flag.Args()
		ConfigServer(args)
	}
}
