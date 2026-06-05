# Quick start

> Get the adult-creator tax & accounting copilot running in under 5 minutes.

## 0. Prerequisites

| Tool | Min version | Why |
|---|---|---|
| Docker | 24+ | dev stack |
| Python | 3.14 | tax-engine, quantum, MCP |
| Go | 1.26 | ledger, kyc, consent, crypto-tax |
| Node | 22 | webhook router, web app |
| Rust | 1.85 | realtime-pricing, zk-verifier |
| Helm | 3.14 | K8s deploy (optional) |

If you have none of these, just use **GitHub Codespaces** — the dev container has every tool pre-installed.

## 1. Clone & configure

```bash
git clone https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot.git
cd adult-creator-tax-accounting-copilot
cp .env.example .env
```

Edit `.env`:
- `DATABASE_URL` — defaults to dev compose stack
- `VAULT_TOKEN` — defaults to `dev-root-token`
- `OIDC_ISSUER` — leave as `http://localhost:8080/realms/copilot` for dev
- `QUANTUM_PROVIDER` — `sim` (default), `anu`, or `ibm`

## 2. Start the dev stack

```bash
docker compose -f docker-compose.dev.yml up -d
```

Services you'll see:
- `nginx-edge` → https://localhost (self-signed dev cert)
- `api-gateway` → http://localhost:8080
- `tax-engine` (Go) → http://localhost:8090
- `tax-engine` (Py) → http://localhost:8091
- `crypto-tax` → http://localhost:8092
- `kyc`, `consent`, `ledger`, `realtime-pricing`, `reporting` → 8093-8097
- `mcp-server-python` → http://localhost:8100
- `mcp-server-go` → http://localhost:8101
- `mcp-server-node` → http://localhost:8102
- `mcp-server-rust` → http://localhost:8103
- `qrng` → http://localhost:8200
- `zk-verifier` → http://localhost:8210
- `web` → http://localhost:3000
- `postgres`, `redis`, `dragonfly`, `kafka`, `minio`
- `ollama`, `vllm`, `sglang`
- `qdrant`, `milvus`, `weaviate`, `chroma`
- `phoenix`, `tempo`, `loki`, `mimir`, `grafana`, `prometheus`
- `vault`

## 3. Run the tests

```bash
# Python (quantum)
(cd quantum/bench && pytest test_kernels.py -v)            # 10 tests
(cd quantum/qrng/tests && PYTHONPATH=../.. pytest test_api.py -v)   # 7 tests

# Python (tax-engine)
(cd services/tax-engine && PYTHONPATH=src pytest -v)        # 6 tests

# Go
for s in kyc consent crypto-tax; do
  (cd services/$s && go test ./...)
done

# Robot Framework (E2E / OWASP / API / tax / quantum / zk / payments)
robot --variable ENV:dev tests/robot/owasp/
robot --variable ENV:dev tests/robot/api/
robot --variable ENV:dev tests/robot/quantum/
robot --variable ENV:dev tests/robot/zk/
robot --variable ENV:dev tests/robot/tax/
robot --variable ENV:dev tests/robot/payments/

# Audit log
python3 scripts/verify_audit.py --log tests/fixtures/audit_log_sample.jsonl
```

Expected: every suite passes (≈30 Python/Go tests + 30+ Robot scenarios).

## 4. Try the QRNG

```bash
curl -s 'http://localhost:8200/v1/qrng/bits?provider=sim&count=128' | jq
```

Returns 128 hex bytes of quantum-random data (simulator backend by default).

## 5. Try a tax estimate

```bash
curl -s -X POST http://localhost:8090/v1/tax/estimate \
  -H 'content-type: application/json' \
  -d '{
    "creator_id":"alice",
    "jurisdiction":"US",
    "year":2026,
    "payouts":[{"platform":"OnlyFans","currency":"USD","gross":20000,"fees":400,"net":19600}]
  }' | jq
```

Returns:
```json
{
  "creator_id": "alice",
  "jurisdiction": "US",
  "year": 2026,
  "gross": 20000.0,
  "bracket": "12%",
  "effective_rate": 0.12,
  "estimated_tax_usd": 2400.0
}
```

## 6. Verify a ZK proof

```bash
curl -s -X POST http://localhost:8210/v1/zk/verify \
  -H 'content-type: application/json' \
  -d @zk/fixtures/age_proof.json | jq
```

## 7. Open the UI

```bash
# Already running via compose at http://localhost:3000
# Or, for hot-reload dev:
(cd apps/web && pnpm dev)
```

## 8. Run the MCP server (Python)

```bash
cd services/mcp-server-python
python3 -m pip install -e .[dev]
python -m mcp_server_python
```

Then point your MCP client (Claude Desktop, opencode, etc.) at the running server.

## 9. Tear down

```bash
docker compose -f docker-compose.dev.yml down -v
```

## 10. Next steps

- Read [`ARCHITECTURE.md`](ARCHITECTURE.md) to understand the design.
- Read [`SECURITY.md`](SECURITY.md) before deploying to production.
- See [`TOOLING.md`](TOOLING.md) for a map of every tool in the index → repo file.
- See [`ROADMAP.md`](ROADMAP.md) for the 1,055-task plan and remaining work.
- Read [`CONTRIBUTING.md`](../CONTRIBUTING.md) before opening a PR.
