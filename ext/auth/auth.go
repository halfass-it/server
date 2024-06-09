package main

import (
	"fmt"
	"os"
	"log"
	"github.com/joho/godotenv"
	"usr_mgmnt_auth/main/config"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Failed to load the env vars: %v", err)
	}

	corsConfig := config.SetupCorsConfig(os.Getenv("AUTH0"))
	service := config.SetupRouter(corsConfig)
	service.Run(fmt.Sprintf(":%s", os.Getenv("PORT")))
}
