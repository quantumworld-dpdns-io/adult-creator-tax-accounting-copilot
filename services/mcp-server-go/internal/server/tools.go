package server

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"github.com/rs/zerolog"
)

// RegisterTools adds all MCP tools to the server.
func RegisterTools(s *server.MCPServer, logger *zerolog.Logger) {
	s.AddTool(
		mcp.NewTool("get_payouts",
			mcp.WithDescription("Fetch aggregated payouts for a creator."),
			mcp.WithString("creator_id", mcp.Required()),
			mcp.WithString("start", mcp.Required()),
			mcp.WithString("end", mcp.Required()),
		),
		makePayoutsHandler(logger),
	)

	s.AddTool(
		mcp.NewTool("compute_tax_estimate",
			mcp.WithDescription("Compute a tax estimate."),
			mcp.WithString("creator_id", mcp.Required()),
			mcp.WithString("jurisdiction", mcp.Required()),
			mcp.WithNumber("year", mcp.Required()),
		),
		makeTaxEstimateHandler(logger),
	)
}

func makePayoutsHandler(logger *zerolog.Logger) server.ToolHandlerFunc {
	return func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		creatorID := req.Params.Name
		args := req.Params.Arguments
		logger.Info().Str("tool", "get_payouts").Str("creator", creatorID).Msg("invoked")

		out := map[string]any{
			"creator_id":  args["creator_id"],
			"start":       args["start"],
			"end":         args["end"],
			"currency":    "USD",
			"gross":       12345.67,
			"fees":        234.56,
			"net":         12111.11,
			"generatedAt": time.Now().UTC().Format(time.RFC3339),
		}
		b, _ := json.Marshal(out)
		return mcp.NewToolResultText(string(b)), nil
	}
}

func makeTaxEstimateHandler(logger *zerolog.Logger) server.ToolHandlerFunc {
	return func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		args := req.Params.Arguments
		logger.Info().Str("tool", "compute_tax_estimate").Msg("invoked")

		jur, ok := args["jurisdiction"].(string)
		if !ok {
			return nil, fmt.Errorf("jurisdiction must be a string")
		}
		out := map[string]any{
			"creator_id":         args["creator_id"],
			"jurisdiction":       jur,
			"year":               args["year"],
			"estimated_tax_usd":  2456.78,
			"effective_rate":     0.21,
			"bracket":            "22%",
			"generatedAt":        time.Now().UTC().Format(time.RFC3339),
		}
		b, _ := json.Marshal(out)
		return mcp.NewToolResultText(string(b)), nil
	}
}
