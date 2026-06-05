# ADR 0002: Polyglot Microservices

## Status

Accepted.

## Context

A single-language stack limits our ability to use the right tool for each
domain (math in Python, performance in Rust, real-time in Go, glue in Node).

## Decision

We adopt a polyglot microservices architecture:

| Service | Language | Rationale |
| ------- | -------- | --------- |
| tax-engine | Python | QuantLib, pandas, tax-rule DSL |
| ledger | Go | Double-entry, append-only, low-overhead |
| payout-aggregator | Python | pandas, NumPy |
| crypto-tax | Rust | rust_decimal, perf |
| webhook-router | Node | @modelcontextprotocol/sdk, DXT |
| realtime-pricing | Rust | Tokio, low-latency |
| kyc | Go | gRPC, throughput |
| consent | Go | simplicity, auditability |
| notification | Node | ws, SSE, DXT |
| reporting | Python + DuckDB | embedded analytics |
| api-gateway | Go | Fiber, JWT, rate limit |
| mcp-server | Python + Go + Node + Rust | per-tool best fit |

## Consequences

- Multiple build pipelines (CI matrix).
- Cross-language contracts enforced via Protobuf + OpenAPI + MCP schemas.
- Single repository with `services/<name>/<lang>/`.
