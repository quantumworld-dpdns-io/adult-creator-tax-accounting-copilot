# Architecture

> C4-style architecture and data-flow documentation for the adult-creator tax & accounting copilot.

## 1. Context (C4 Level 1)

```
                    ┌────────────────────┐
   Creator (Person) │  Accountant (Org)  │  Tax Authority
                    └──────────┬─────────┘
                               │ HTTPS / MCP
                               ▼
        ┌──────────────────────────────────────────────────┐
        │  Adult Creator Tax & Accounting Copilot          │
        │  ─ Aggregates fiat & crypto payouts              │
        │  ─ Computes multi-jurisdiction tax estimates     │
        │  ─ Produces signed audit log + ZK proofs         │
        └────────┬───────────────────────────┬─────────────┘
                 │ OAuth2 / OIDC             │ JWT
                 ▼                           ▼
   ┌──────────────────────────┐  ┌──────────────────────────┐
   │  Platform partners       │  │  KYC provider (Persona)  │
   │  OnlyFans · Fansly · ... │  │                          │
   └──────────────────────────┘  └──────────────────────────┘
```

The copilot is the single source of truth for a creator's tax-relevant facts.

## 2. Containers (C4 Level 2)

| Container | Language | Port | Responsibility |
|---|---|---|---|
| `api-gateway` | Go | 8080 | Public entrypoint, rate-limit, JWT verify, route |
| `webhook-router` | TypeScript | 8081 | Ingest webhooks from platforms, normalise, sign, enqueue |
| `tax-engine` (Go) | Go | 8090 | High-throughput batch tax estimation (per 10k payouts < 1s) |
| `tax-engine` (Py) | Python | 8091 | ML-based estimation, quantlib curves, marginal brackets |
| `crypto-tax` | Go | 8092 | FIFO / LIFO / HIFO lot matching, CSV export |
| `kyc` | Go | 8093 | Persona integration, age verification, watch-list screen |
| `consent` | Go | 8094 | GDPR grant, DSAR export, erasure, retention sweep |
| `ledger` | Go | 8095 | Append-only BLAKE3 / Dilithium-signed ledger |
| `realtime-pricing` | Rust | 8096 | FX + token prices, WebSocket fan-out |
| `reporting` | Python | 8097 | 1099 / W-8BEN / VAT-MOSS / 2257 statement generation |
| `mcp-server-python` | Python | 8100 | MCP server, tools/{payouts,taxes,zk} |
| `mcp-server-go` | Go | 8101 | MCP server, mcp-go SDK |
| `mcp-server-node` | Node | 8102 | MCP server, @modelcontextprotocol/sdk |
| `mcp-server-rust` | Rust | 8103 | MCP server, axum + rmcp |
| `qrng` | Python (FastAPI) | 8200 | Quantum RNG bits (sim / ANU / IBM) |
| `zk-verifier` | Rust (axum) | 8210 | Verify Noir + RISC Zero proofs |
| `web` | Next.js | 3000 | Creator dashboard |
| `nginx-edge` | nginx | 443 | PQC TLS termination, OWASP headers, rate limit |
| `agents/crewai` | Python | - | Tax-analyst multi-agent (offline batch) |
| `agents/langgraph` | Python | - | Tax-filing state graph (offline batch) |

## 3. Components (C4 Level 3)

### 3.1 `tax-engine` (Go)

```
cmd/tax-engine
├── /v1/tax/estimate   POST   - estimate one creator
├── /v1/tax/file       POST   - generate 1099 / W-8BEN / VAT-MOSS
└── /v1/tax/aggregate  POST   - aggregate VAT MOSS across creators

internal/
├── rules/        # TOML-loaded progressive brackets
├── quantlib/     # term-structure curves
├── pagination/   # cursor-paged listings
└── observability/ # OTel middleware
```

### 3.2 `ledger`

```
cmd/ledger
├── POST /v1/ledger/append     (signed entry)
├── GET  /v1/ledger/head       (chain head)
├── GET  /v1/ledger/verify     (offline chain verify)
└── GET  /v1/ledger/stream     (server-sent events)

internal/
├── blake3/      # chain hashing
├── dilithium/   # signing
└── storage/     # Postgres + S3 (cold)
```

## 4. Data flow

### 4.1 Webhook → ledger flow

```
1. Platform → POST /webhook/{onlyfans|fansly|...}
2. webhook-router verifies HMAC, parses payload
3. webhook-router emits Kafka `webhook.received.v1`
4. tax-engine consumes, normalises into a Payout struct
5. tax-engine calls ledger.Append(payout + bracket decision)
6. ledger signs (Dilithium-5) and chains (BLAKE3)
7. qrng entropy injected into signature nonce
8. reporting service materialises 1099 / W-8BEN
9. (optional) agents/crewai validates the bracket choice
10. (optional) zk-verifier confirms a ZK age/income proof
```

### 4.2 Tax-estimate request flow

```
Creator → api-gateway → tax-engine
                            │
                            ├── rules/ (TOML brackets)
                            ├── quantlib/ (curves)
                            ├── realtime-pricing/ (FX)
                            ├── crypto-tax/ (lot match if needed)
                            └── ledger/Append (audit)
```

## 5. Data model

```sql
-- creators
id (uuid pk), display_name, jurisdiction, tin, created_at

-- payouts
id, creator_id, platform, currency, gross, fees, net, received_at

-- crypto_transactions
id, creator_id, asset, qty, cost_basis, proceeds, ts, type, source

-- consents
id, creator_id, scope, granted_at, expires_at, revoked_at

-- ledger_entries
seq, prev_hash, hash, signature, payload (jsonb), created_at
```

## 6. Cross-cutting

| Concern | Implementation |
|---|---|
| AuthN / AuthZ | OIDC via api-gateway, JWT to services, mTLS inside mesh |
| Observability | OpenTelemetry traces → Tempo, metrics → Prometheus, logs → Loki, LLM spans → Phoenix |
| Secrets | Vault + External Secrets Operator, sealed-secrets for Git |
| Policy | Kyverno (cluster), OPA (per-request), Conftest (CI) |
| Network | Cilium / Calico NetworkPolicies, Istio mTLS |
| Supply chain | Sigstore cosign, SLSA L3, SBOM, dependabot, renovate |
| Quantum-safe | Kyber-1024 KEM, Dilithium-5 sigs, BLAKE3 chains, PQC TLS at edge |

## 7. Deployment topology

4 clouds (Zeabur, Northflank, Scaleway, Exoscale), each running:
- 1× control-plane namespace (`copilot-system`)
- 1× workload namespace (`copilot-prod`)
- Cilium CNI
- Istio ingress gateway
- 25+ pods from the umbrella chart

Storage: managed Postgres + object storage (S3-compatible) per cloud.
Secrets: managed KMS in cloud + Vault sidecar.

## 8. Failure modes & mitigation

| Failure | Mitigation |
|---|---|
| Cloud region outage | Cross-cloud disaster recovery runbook in `docs/runbook/dr.md` |
| Postgres failover | Patroni per cloud, read-replica in 2nd region |
| Kafka lag | Auto-scale consumers, dead-letter topic |
| PQC library not on host | Hybrid TLS (PQC + X25519), Gradual deprecation of RSA/ECDSA |
| Quantum hardware unavailable | Classical fallback in every quantum kernel |
| MCP server down | Local-only mode; creator UI still works |
| Wasm plugin crash | Capability sandbox; pod restart on panic |

## 9. ADRs

See [`docs/adr/`](adr/) for the 9 architecture decision records.
