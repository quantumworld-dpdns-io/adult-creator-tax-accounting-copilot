// Package server wires the MCP server and registers tools.
package server

import (
	"context"
	"fmt"
	"os"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/rs/zerolog"
)

// New builds a configured MCP server.
func New() *server.MCPServer {
	logger := zerolog.New(os.Stdout).With().Timestamp().Logger()

	s := server.NewMCPServer(
		"adult-creator-tax-copilot",
		"0.1.0",
		server.WithToolCapabilities(true),
		server.WithLogging(),
		server.WithRecovery(),
	)

	RegisterTools(s, &logger)
	return s
}

// Run starts the server using the MCP_TRANSPORT env var.
func (s *server.MCPServer) Run(ctx context.Context) error {
	transport := os.Getenv("MCP_TRANSPORT")
	if transport == "" {
		transport = "stdio"
	}
	switch transport {
	case "stdio":
		return server.ServeStdio(s)
	case "sse":
		addr := os.Getenv("MCP_ADDR")
		if addr == "" {
			addr = ":8080"
		}
		sse := server.NewSSEServer(s)
		return sse.Start(addr)
	default:
		return fmt.Errorf("unknown transport %q", transport)
	}
}
