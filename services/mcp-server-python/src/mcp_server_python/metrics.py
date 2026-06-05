"""Server-side Prometheus metrics."""

from __future__ import annotations

from prometheus_client import Counter, Histogram

__all__ = [
    "TOOL_CALLS",
    "TOOL_LATENCY",
    "TOOL_ERRORS",
]

TOOL_CALLS = Counter(
    "mcp_tool_calls_total",
    "Number of MCP tool invocations",
    labelnames=("tool", "status"),
)

TOOL_LATENCY = Histogram(
    "mcp_tool_latency_seconds",
    "MCP tool call latency in seconds",
    labelnames=("tool",),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

TOOL_ERRORS = Counter(
    "mcp_tool_errors_total",
    "Number of MCP tool errors",
    labelnames=("tool", "kind"),
)
