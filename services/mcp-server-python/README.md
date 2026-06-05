# MCP Server (Python)

FastMCP-based Model Context Protocol server exposing tax/accounting tools to
Claude, Gemini, Codex Desktop, Claude Desktop, and any other MCP client.

## Tools exposed

- `get_payouts(creator_id, range)` — fetch aggregated payouts
- `compute_tax_estimate(creator_id, jurisdiction, year)` — tax estimate
- `file_1099(creator_id, year)` — generate 1099 PDF
- `file_w8ben(creator_id, treaty_country)` — generate W-8BEN
- `aggregate_vat(creator_id, period)` — EU VAT MOSS aggregation
- `verify_age_zk(creator_id)` — zero-knowledge age proof
- `prove_income_range(creator_id, lower, upper)` — ZK income range proof

## Transports

- stdio (default)
- SSE
- streamable HTTP (WASI 0.3 component)

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python -m mcp_server_python
```
