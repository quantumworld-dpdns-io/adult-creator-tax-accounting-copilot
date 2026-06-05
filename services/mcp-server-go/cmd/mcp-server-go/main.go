// Package main starts the Go MCP server.
package main

import (
	"context"
	"log"

	"github.com/quantumworld-dpdns-io/mcp-server-go/internal/server"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	s := server.New()
	if err := s.Run(ctx); err != nil {
		log.Fatalf("mcp server: %v", err)
	}
}
