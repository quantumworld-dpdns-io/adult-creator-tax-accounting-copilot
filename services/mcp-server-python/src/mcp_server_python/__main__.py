"""MCP server entry point (stdio)."""

from __future__ import annotations

import asyncio
import sys

from mcp_server_python.server import create_server, run


def main() -> int:
    """Entrypoint for the console script."""
    server = create_server()
    try:
        asyncio.run(run(server))
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
