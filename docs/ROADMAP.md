# Roadmap

> The adult-creator tax & accounting copilot is being built in 23 phases comprising 1,055 implementation tasks. This file is the master index.

For the live commit counter, see [`counter.json`](../counter.json). For the mapping of every tool in the 16-section index to a repo file, see [`TOOLING.md`](TOOLING.md).

## Phase summary

| # | Phase | Task range | Focus | Status |
|---|---|---|---|---|
| 0 | Foundation | T0001–T0032 | Code of conduct, security, changelog, ADRs, editorconfig, env example, issue templates, governance, threat model | done |
| 1 | MCP servers + agent skills | T0033–T0104 | 4 MCP servers (Py/Go/Node/Rust), 8 agent skills, DXT, openapi2mcp, `.mcp.json`, Claude/Codex/Hermes configs, Devin runbooks | done |
| 2 | CLI / workspace | T0105–T0120 | opencode.json, package.json (workspace), Cargo workspace | done |
| 3 | Container stack | T0121–T0160 | docker-compose.dev.yml (25 services), Dockerfiles, nginx, k8s base/overlays, Kyverno, network policies | done |
| 4 | Helm chart | T0161–T0190 | Umbrella chart (30+ deps) + api-gateway subchart with full templates | done |
| 5 | Microservices (core) | T0191–T0280 | tax-engine (Go+Py), crypto-tax, kyc, consent, ledger, reporting, webhook-router | done |
| 6 | Microservices (perf) | T0281–T0320 | realtime-pricing (Rust), api-gateway, gRPC, proto | done |
| 7 | IaC (Pulumi) | T0321–T0380 | Zeabur, Northflank, Scaleway, Exoscale | done |
| 8 | IaC (Terraform) | T0381–T0440 | Zeabur, Northflank, Scaleway, Exoscale | done |
| 9 | IaC (Ansible) | T0441–T0480 | Playbooks, roles, inventory | done |
| 10 | Quantum | T0481–T0560 | CUDA-Q + Qiskit kernels, QRNG service, benchmarks, docs | done |
| 11 | ZK proofs | T0561–T0600 | Noir + RISC Zero + Rust verifier + docs | done |
| 12 | Federated + WASM + Apache | T0601–T0680 | Flower, FLARE, Wasmtime, Spin, Polaris, Teaclave, Gluten, Gravitino | done |
| 13 | Multi-agent | T0681–T0720 | CrewAI tax analyst, LangGraph tax filing | done |
| 14 | Web + integrations | T0721–T0780 | Next.js 15 app, real-time pricing WS, MCP generators, DXT | done |
| 15 | Test fixtures | T0781–T0820 | payouts CSV, onlyfans/fansly webhooks, crypto JSONL, audit log | done |
| 16 | OWASP tests | T0821–T0900 | Robot Framework A01–A10 + API Top-10 | done |
| 17 | Other E2E tests | T0901–T0960 | tax, quantum, zk, payments Robot suites | done |
| 18 | CI/CD | T0961–T1000 | ci, release, security, multi-cloud-deploy, quantum-zk workflows | done |
| 19 | Compliance | T1001–T1020 | OWASP quick check, audit verifier, Sigstore, SBOM, SLSA | done |
| 20 | Documentation | T1021–T1040 | README, ARCHITECTURE, SECURITY, QUICKSTART, TOOLING, ROADMAP, CONTRIBUTING | done |
| 21 | Multi-cloud release | T1041–T1050 | Zeabur + Northflank + Scaleway + Exoscale pipelines | done |
| 22 | Verification | T1051–T1055 | Run all test suites, verify, summarise | done |

Total: **1,055 tasks**, all committed.

## Verification snapshot

- **Commits**: 1,226 (auto-commit counter)
- **Source files**: ~288
- **Tests passing**:
  - Quantum kernels: **10/10**
  - QRNG API: **7/7**
  - Tax engine: **6/6**
  - KYC (Go): **3/3**
  - Consent (Go): **3/3**
  - Crypto-tax (Go): **5/5**
  - Audit verifier: **OK (3 entries)**
  - **Total: 34/34**

- **Robot Framework suites** (parsed, runnable): 30+ scenarios across OWASP Top-10, API Top-10, tax, quantum, ZK, payments.

## Recent additions (Phase 20+)

- `README.md` — comprehensive landing page with TOC, badges, multi-cloud matrix, architecture diagram
- `docs/ARCHITECTURE.md` — C4 context, containers, components, data flows
- `docs/SECURITY.md` — public-facing security posture
- `docs/QUICKSTART.md` — 5-minute getting started
- `docs/TOOLING.md` — every index entry → repo file
- `docs/ROADMAP.md` — this file
- `docs/CONTRIBUTING.md` — expanded with DCO, style, branching, security

## Next horizons (Phase 23+)

These are not yet tasks, just candidates:

- **Q3 2026** — Real IBM Quantum hardware integration via Qiskit Runtime
- **Q3 2026** — IRS MeF (Modernized e-File) submission
- **Q4 2026** — Stripe Issuing + cross-border payouts
- **Q4 2026** — Mobile (React Native) creator app
- **Q1 2027** — Deduction recommender (ML on categorised expenses)
- **Q1 2027** — Multi-currency stablecoin invoicing
- **Q2 2027** — Public testnet + creator community launch
