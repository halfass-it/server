package control

import (
	"context"
	"log"
	"net/http"

	"server/config"
)

type Server struct {
	httpServer *http.Server
}

func NewServer(cfg *config.Config) *Server {
	mux := http.NewServeMux()
	mux.HandleFunc("/ping", pingHandler)
	mux.HandleFunc("/data", dataHandler)

	return &Server{
		httpServer: &http.Server{
			Addr:    cfg.ServerAddress,
			Handler: mux,
		},
	}
}

func (s *Server) ListenAndServe() error {
	return s.httpServer.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	return s.httpServer.Shutdown(ctx)
}

func ConfigServer(args []string) {
	log.Println("Configuring server with args:", args)
	// Configuration logic here
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	log.Println("Received ping request from: ", r.RemoteAddr)
	w.Write([]byte("pong"))
}

func dataHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Received data request from: ", r.RemoteAddr)
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	data := make([]byte, r.ContentLength)
	if _, err := r.Body.Read(data); err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	log.Println("Received data from: ", r.RemoteAddr)
	w.Write([]byte("Received data: " + string(data)))
}
