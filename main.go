package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"server/config"
	"server/control"
	"server/logger"
)

func main() {
	// Initialize logger
	logger.Init()

	// Load configuration
	cfg := config.Load()

	// Parse command line flags
	startFlag := flag.Bool("start", false, "Run the server")
	setupFlag := flag.Bool("setup", false, "Configure the server")
	flag.Parse()

	if *setupFlag {
		control.ConfigServer(flag.Args())
		return
	}

	if *startFlag {
		// Start the server
		srv := control.NewServer(cfg)

		// Graceful shutdown
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

		go func() {
			<-quit
			ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
			defer cancel()
			if err := srv.Shutdown(ctx); err != nil {
				log.Fatalf("Server forced to shutdown: %v", err)
			}
		}()

		log.Println("Server is starting...")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Could not listen on %s: %v", cfg.ServerAddress, err)
		}
		log.Println("Server stopped")
	} else {
		fmt.Println("Please use -start or -setup flag")
	}
}
