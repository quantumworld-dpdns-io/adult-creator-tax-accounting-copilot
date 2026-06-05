# Adult Creator Tax & Accounting Copilot

[![CI](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/ci.yml)
[![Security](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/security.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/security.yml)
[![Multi-Cloud](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/multi-cloud-deploy.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/multi-cloud-deploy.yml)
[![Quantum + ZK](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/quantum-zk.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot/actions/workflows/quantum-zk.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OWASP](https://img.shields.io/badge/OWASP-ASVS%20L2-blue)](https://owasp.org/www-project-application-security-verification-standard/)
[![Quantum Safe](https://img.shields.io/badge/quantum--safe-Kyber%2FDilithium-purple)](https://csrc.nist.gov/projects/post-quantum-cryptography)
[![Robot Framework](https://img.shields.io/badge/tests-Robot%20Framework-red)](https://robotframework.org/)
[![Helm](https://img.shields.io/badge/helm-umbrella-0f1689)](https://helm.sh/)
[![Multi-Cloud](https://img.shields.io/badge/deploy-Zeabur%20%7C%20Northflank%20%7C%20Scaleway%20%7C%20Exoscale-blueviolet)](#multi-cloud-deployment)

> A polyglot, quantum-safe, multi-cloud copilot for adult-content creators — aggregating fiat & crypto payouts, computing tax obligations across jurisdictions, generating 1099 / W-8BEN / VAT-MOSS / 2257 evidence, and proving correctness with zero-knowledge proofs and a BLAKE3 + Dilithium-5 signed audit log.

---

## Table of Contents

- [Why this exists](#why-this-exists)
- [Highlights](#highlights)
- [Architecture at a glance](#architecture-at-a-glance)
- [Repository layout](#repository-layout)
- [Quick start](#quick-start)
- [Test suites](#test-suites)
- [Multi-cloud deployment](#multi-cloud-deployment)
- [Security & compliance](#security--compliance)
- [Quantum & zero-knowledge features](#quantum--zero-knowledge-features)
- [Tech-stack matrix](#tech-stack-matrix)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Why this exists

Adult-content creators operate in a uniquely hostile environment:

- **Fiat + crypto payouts** from platforms (OnlyFans, Fansly, Chaturbate, etc.) that don't coordinate
- **Agencies & managers** that take a cut but rarely provide clean accounting
- **Multi-jurisdiction tax exposure** (US 1099, UK self-assessment, EU VAT-MOSS, KYC/AML)
- **Privacy + censorship** risk that makes on-chain transparency unsafe
- **Quantum-readiness** — payments and signatures in 2026 will outlive the Y2Q transition

This copilot gives an independent creator (or their accountant) a single, auditable, quantum-safe, privacy-preserving ledger of *every* dollar, token, and tip — with explainable tax estimates, signed evidence, and verifiable proofs.

## Highlights

| Domain | What you get |
|---|---|
| **Polyglot microservices** | Go (tax-engine, ledger, kyc, consent, crypto-tax), Python (MCP server, tax-engine ML, quantum kernels), Node/TypeScript (webhook router, web app), Rust (real-time pricing, ZK verifier, WASM components) |
| **MCP integration** | First-class [Model Context Protocol](https://modelcontextprotocol.io/) server in 4 languages, OpenAPI → MCP generator, DXT bundles |
| **Agent skills** | `.skills/` for tax-1099, crypto-fifo, vat-moss, w8ben, kyc-aml, zkp-age, zkp-income, quantum-audit |
| **Quantum-safe cryptography** | Kyber-1024 KEM, Dilithium-5 signatures, BLAKE3 hash chains, hybrid TLS (PQC ciphers in nginx) |
| **Quantum kernels** | CUDA-Q + Qiskit: QRNG, Kyber/Dilithium entropy seeding, QAOA currency-basket optimisation, VQE portfolio rebalancing, variational fraud classifier |
| **Zero-knowledge proofs** | Noir circuits for age & income range; RISC Zero proofs; Rust verifier exposing JSON-RPC |
| **Federated learning** | Flower (Python) + FLARE (Rust) for cross-creator fraud-detection models without leaking private data |
| **WASM plugins** | Tax-form validator runs inside Wasmtime, Spin, and a Spin Docker image — sandboxed by capability |
| **Apache integrations** | Polaris (catalog), Teaclave (confidential compute), Gluten (Spark accelerator), Gravitino (metadata lakehouse) |
| **Multi-agent** | CrewAI tax analyst + LangGraph tax-filing graph |
| **OWASP coverage** | ASVS L2 + Top-10 2021 + API Top-10 — all 30+ test scenarios live in Robot Framework |
| **Test stack** | pytest, go test, Robot Framework (OWASP, API, tax, quantum, zk, payments), k6, Playwright, OWASP ZAP |
| **Audit log** | Append-only, BLAKE3 hash-chained, Dilithium-5 signed; offline verifier in `scripts/verify_audit.py` |
| **CI/CD** | GitHub Actions: ci / release / security / multi-cloud-deploy / quantum-zk |
| **Container** | Multi-stage Dockerfiles for Python, Go, Node, Rust; Docker Compose dev stack with 25+ services |
| **Kubernetes** | Helm umbrella chart (30+ sub-charts), Kustomize overlays (dev/prod), Kyverno cluster policies, Cilium/Calico network policies |
| **Service mesh** | Istio + Linkerd sidecars, mTLS by default |
| **IaC triad** | Pulumi + Terraform + Ansible — same workload deploys to 4 clouds |
| **Multi-cloud** | Zeabur · Northflank · Scaleway · Exoscale — identical Helm chart per provider |
| **Observability** | Prometheus + Grafana + Loki + Tempo + Mimir + OTel collector + Phoenix (LLM) |
| **Vector + SQL** | Qdrant, Milvus, Weaviate, Chroma (pgvector-compatible embeddings) |
| **LLM serving** | Ollama, vLLM, SGLang — model-agnostic |
| **Secrets** | Vault + External Secrets Operator + sealed-secrets |
| **Policy** | Kyverno + OPA + Conftest + Sigstore cosign signing |
| **Dev containers** | `.devcontainer/` + GitHub Codespaces + Gitpod |
| **Open source compliance** | DCO, CLA bot, Codeowners, CODE_OF_CONDUCT, SECURITY policy, support, governance, threat model, ADRs |

## Architecture at a glance

```
                ┌────────────────────────────────────────────────────────────┐
                │              Cloud Edge  (nginx + PQC TLS)                │
                │         Hybrid Kyber-1024 + X25519 + AES-256-GCM          │
                └────────────────────────────┬───────────────────────────────┘
                                             │
                ┌────────────────────────────┴───────────────────────────────┐
                │         Kubernetes  (multi-cloud: 4 providers)            │
                │   Istio / Linkerd mesh · Kyverno · OPA · Vault · mTLS     │
                │                                                             │
                │  ┌──────────────┐ ┌──────────────┐ ┌───────────────────┐  │
                │  │ api-gateway  │ │ webhook-     │ │ realtime-pricing  │  │
                │  │   (Go+Py)    │ │ router (TS)  │ │     (Rust)        │  │
                │  └──────┬───────┘ └──────┬───────┘ └─────────┬─────────┘  │
                │         │                │                   │            │
                │  ┌──────┴────────────────┴───────────────────┴──────────┐ │
                │  │ tax-engine (Go) · tax_engine (Py) · crypto-tax (Go)  │ │
                │  │ kyc (Go) · consent (Go) · ledger (Go) · reporting(Py)│ │
                │  └──────┬──────────────────────────────────────────────┘ │
                │         │                                                  │
                │  ┌──────┴────────┐  ┌────────────────┐  ┌──────────────┐  │
                │  │ MCP servers   │  │  Quantum svc   │  │  ZK verifier │  │
                │  │ Py · Go · Node│  │  (QRNG) Py     │  │  (Rust)      │  │
                │  │ · Rust        │  │  CUDA-Q · Qiskit│  │  Noir · RISC0│  │
                │  └───────────────┘  └────────────────┘  └──────────────┘  │
                │                                                             │
                │  ┌──────────────────────────────────────────────────────┐  │
                │  │  WASM plugins  ·  Apache (Polaris/Teaclave/          │  │
                │  │  Gluten/Gravitino)  ·  Federated (Flower/FLARE)     │  │
                │  └──────────────────────────────────────────────────────┘  │
                └─────────────────────────────────────────────────────────────┘
                  Postgres  ·  Redis / Dragonfly  ·  Kafka  ·  MinIO (S3)
                  Qdrant / Milvus / Weaviate / Chroma  ·  Vault  ·  OTel
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the C4 model, every microservice contract, and data-flow diagrams.

## Repository layout

```
.
├── apps/                      # Next.js web app (creator UI)
├── agents/                    # CrewAI + LangGraph multi-agent
├── apache/                    # Polaris / Teaclave / Gluten / Gravitino
├── agents/skills/             # Agent skill packages (8 skills)
├── config/                    # YAML, JSON schemas, feature flags
├── counter.json               # Auto-commit counter
├── docker/                    # Multi-stage Dockerfiles
├── docker-compose.dev.yml     # 25-service dev stack
├── docs/                      # ADRs, architecture, runbooks
│   └── adr/                   # Architecture decision records
├── federated/                 # Flower (Py) + FLARE (Rust)
├── helm/                      # Umbrella Helm chart + api-gateway subchart
├── infra/                     # Pulumi / Terraform / Ansible (4 clouds)
│   ├── ansible/{playbooks,roles}
│   ├── pulumi/{zeabur,northflank,scaleway,exoscale}
│   └── terraform/{zeabur,northflank,scaleway,exoscale}
├── k8s/                       # Kustomize overlays (base, dev, prod)
├── mcp/                       # Generated MCP server templates
├── proto/                     # gRPC / protobuf definitions
├── quantum/                   # CUDA-Q + Qiskit kernels, QRNG service
├── scripts/                   # verify_audit.py, owasp_quick_check.sh
├── services/                  # Polyglot microservices (see ARCHITECTURE.md)
│   ├── api-gateway/           # Kong-style gateway (Go)
│   ├── consent/               # GDPR / DSAR (Go)
│   ├── crypto-tax/            # FIFO/LIFO/HIFO (Go)
│   ├── kyc/                   # Persona integration (Go)
│   ├── ledger/                # Append-only ledger (Go)
│   ├── mcp-server-{python,go,node,rust}/
│   ├── realtime-pricing/      # Coingecko / Stripe FX (Rust)
│   ├── reporting/             # 1099 / W-8BEN / VAT-MOSS (Python)
│   ├── tax-engine/            # Go + Python dual impl
│   └── webhook-router/        # Platform webhooks (TypeScript)
├── tests/
│   ├── fixtures/              # Sample data (CSV / JSONL)
│   └── robot/                 # OWASP / API / tax / quantum / zk / payments
├── wasm/                      # Wasmtime + Spin components
├── webhooks/                  # Hand-written platform webhook handlers
├── zk/                        # Noir + RISC Zero + verifier (Rust)
├── .claude/                   # Claude Code commands & agents
├── .codex/                    # Codex agents
├── .devcontainer/             # Codespaces / Gitpod
├── .github/                   # Workflows, issue templates, dependabot
├── .opencode/                 # opencode CLI config
├── .skills/                   # Reusable agent skills
├── opencode.json              # opencode CLI configuration
├── package.json               # Node workspace
├── pyproject.toml             # Python workspace (uv)
└── Cargo.toml                 # Rust workspace
```

## Quick start

### Prerequisites
- Python 3.14+ · Go 1.26+ · Node 22+ · Rust 1.85+
- Docker + Docker Compose v2
- Helm 3.14+ · kubectl · kustomize
- Pulumi / Terraform / Ansible (only if you intend to deploy)

### 1. Clone & bootstrap

```bash
git clone https://github.com/quantumworld-dpdns-io/adult-creator-tax-accounting-copilot.git
cd adult-creator-tax-accounting-copilot
cp .env.example .env
make bootstrap   # installs pre-commit hooks, generates TLS material, etc.
```

### 2. Start the dev stack

```bash
docker compose -f docker-compose.dev.yml up -d
```

This brings up Postgres, Redis/Dragonfly, Kafka, MinIO, the LLM triplet (Ollama/vLLM/SGLang), the vector quartet (Qdrant/Milvus/Weaviate/Chroma), the observability quintet (Phoenix/Tempo/Loki/Mimir/Grafana), Prometheus, Vault, the nginx edge with PQC TLS, the API gateway, the tax-engine, and the MCP server.

### 3. Run the tests

```bash
# Python
cd quantum/bench && pytest test_kernels.py -v              # 10 tests
PYTHONPATH=../.. pytest test_api.py -v                       # 7 QRNG tests
cd ../../services/tax-engine && PYTHONPATH=src pytest -v     # 6 tests

# Go
for s in kyc consent crypto-tax; do
  (cd services/$s && go test ./...)
done

# Robot Framework (E2E / OWASP)
robot --variable ENV:dev tests/robot/owasp/
robot --variable ENV:dev tests/robot/api/
```

### 4. Open the UI

```bash
cd apps/web && pnpm dev
# → http://localhost:3000
```

For a 5-minute tour see [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Test suites

| Suite | Tooling | Coverage |
|---|---|---|
| Quantum kernels | pytest | 10/10 passing (QRNG, Kyber, Dilithium, QAOA, VQE, fraud) |
| QRNG API | pytest + fastapi.TestClient | 7/7 passing (sim, validation, limits, uniqueness) |
| Tax engine | pytest + fastapi.TestClient | 6/6 passing (US/UK/VAT, 1099, W-8BEN) |
| KYC | go test | Persona adult/minor/ID flows |
| Consent | go test | GDPR grant / DSAR / erasure |
| Crypto-tax | go test | FIFO / LIFO / HIFO / CSV export |
| OWASP Top-10 (2021) | Robot Framework | A01–A10 |
| OWASP API Top-10 | Robot Framework | API1–API10 |
| Quantum E2E | Robot Framework | QRNG HTTP |
| ZK E2E | Robot Framework | proof verify over HTTP |
| Payments | Robot Framework | webhook signature, idempotency |

## Multi-cloud deployment

The same workload targets four clouds via three IaC tools:

| Cloud | Pulumi | Terraform | Helm |
|---|---|---|---|
| [Zeabur](https://zeabur.com) | `infra/pulumi/zeabur` | `infra/terraform/zeabur` | `helm install copilot ./helm` |
| [Northflank](https://northflank.com) | `infra/pulumi/northflank` | `infra/terraform/northflank` | `helm install copilot ./helm` |
| [Scaleway](https://www.scaleway.com) | `infra/pulumi/scaleway` | `infra/terraform/scaleway` | `helm install copilot ./helm` |
| [Exoscale](https://www.exoscale.com) | `infra/pulumi/exoscale` | `infra/terraform/exoscale` | `helm install copilot ./helm` |

```bash
# Pick a target
export CLOUD=exoscale

# Deploy with Pulumi (preferred)
cd infra/pulumi/$CLOUD
pulumi up

# Or Terraform
cd infra/terraform/$CLOUD
terraform init && terraform apply

# Or Ansible
cd infra/ansible
ansible-playbook -i inventories/prod.ini playbooks/bootstrap.yml
```

## Security & compliance

- **OWASP ASVS L2** verified in CI by `security.yml` and the Robot suite under `tests/robot/owasp/`
- **OWASP Top-10 2021** + **API Top-10** scenarios under `tests/robot/owasp/` and `tests/robot/api/`
- **Quantum-safe signatures** — every audit-log entry is Dilithium-5 signed and chained with BLAKE3 (`scripts/verify_audit.py`)
- **PQC TLS** at the edge — `infra/nginx/nginx.conf` enables `KYBER_AES_256_GCM_SHA384` and X25519 fallback
- **GDPR / DSAR** — `services/consent/` grants, exports, and erases
- **2257 evidence** — `services/reporting/statement.py` aggregates model-release hashes
- **Sigstore cosign** signing for every release artefact
- **Kyverno cluster policies** — deny-privileged, read-only-root-fs, runAsNonRoot
- **Network policies** — default-deny, explicit allow-lists per namespace
- **SBOM + SLSA provenance** generated by `release.yml`

See [`docs/SECURITY.md`](docs/SECURITY.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) for the full posture.

## Quantum & zero-knowledge features

### Quantum kernels (`quantum/`)

| Kernel | Backend | Purpose |
|---|---|---|
| `qrng_bits` | CUDA-Q sim / Qiskit Aer | Quantum-random bit source |
| `seed_kyber` | CUDA-Q sim | Deterministic Kyber keypair seed |
| `seed_dilithium` | CUDA-Q sim | Deterministic Dilithium keypair seed |
| `qaoa_currency_basket` | CUDA-Q + Qiskit | Optimise basket of creator payouts |
| `train_fraud_model` | CUDA-Q + Qiskit | Variational fraud classifier |
| `vqe_portfolio` | CUDA-Q + Qiskit | Find-min-cost creator portfolio |

The `qrng` service (`quantum/qrng/service.py`) exposes `GET /v1/qrng/bits?provider=sim|anu|ibm&count=64..4096` and is consumed by the audit-log signer.

### Zero-knowledge proofs (`zk/`)

- **Noir** circuits: `zk/noir/prove_age/`, `zk/noir/prove_income_range/`
- **RISC Zero** host + guest: `zk/risc0/`
- **Verifier** (Rust): `zk/verifier/verify.rs` exposes a JSON-RPC interface at `/v1/zk/verify`

Use cases: a creator proves "I am 18+" without sending a selfie, or "my income is in bracket B" without revealing the exact number.

## Tech-stack matrix

| Layer | Choice |
|---|---|
| Languages | Go 1.26 · Python 3.14 · TypeScript / Node 22 · Rust 1.85 |
| API | REST (OpenAPI 3.1), gRPC, JSON-RPC, MCP |
| Storage | PostgreSQL 17 · Redis / Dragonfly · Kafka · MinIO (S3) |
| Vector | Qdrant · Milvus · Weaviate · Chroma |
| LLM serving | Ollama · vLLM · SGLang |
| Quantum | CUDA-Q 0.10 · Qiskit 1.4 |
| ZK | Noir 1.0 · RISC Zero 1.2 |
| WASM | Wasmtime · Spin |
| Federated | Flower 1.16 · NVIDIA FLARE 2.5 |
| Frontend | Next.js 15 · React 19 · Tailwind 4 |
| Container | Docker · Compose · BuildKit |
| Orchestration | Kubernetes 1.32 · Helm 3.14 · Kustomize 5 |
| Mesh | Istio · Linkerd |
| Policy | Kyverno · OPA · Conftest |
| Observability | Prometheus · Grafana · Loki · Tempo · Mimir · OpenTelemetry · Phoenix |
| Secrets | Vault · External Secrets Operator · sealed-secrets |
| IaC | Pulumi · Terraform · Ansible |
| CI/CD | GitHub Actions (5 workflows) |
| Testing | pytest · go test · Robot Framework · k6 · Playwright · OWASP ZAP |
| Signing | Sigstore cosign · Kyber · Dilithium |

## Roadmap

A 1,055-task implementation plan covering foundation, MCP, microservices, IaC, quantum, ZK, WASM, federated, Apache, agents, web, tests, CI/CD, and documentation is tracked in [`docs/ROADMAP.md`](docs/ROADMAP.md). Current counter: see [`counter.json`](counter.json).

## Contributing

We welcome PRs from creators, accountants, cryptographers, and tax professionals. Read [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md), open a feature request, and sign your commits (`git commit -s`).

Code style: [`docs/CODE_STYLE.md`](docs/CODE_STYLE.md)
Branching: [`docs/BRANCHING.md`](docs/BRANCHING.md)
Governance: [`docs/GOVERNANCE.md`](docs/GOVERNANCE.md)

## License

[MIT](LICENSE) — see also [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) and [SECURITY](SECURITY.md).

## Acknowledgements

- [OWASP](https://owasp.org) for ASVS / Top-10
- [NIST PQC](https://csrc.nist.gov/projects/post-quantum-cryptography) for Kyber & Dilithium
- [NVIDIA CUDA-Q](https://developer.nvidia.com/cuda-q), [IBM Qiskit](https://qiskit.org)
- [Noir](https://noir-lang.org), [RISC Zero](https://risczero.com)
- [Apache Polaris / Teaclave / Gluten / Gravitino](https://apache.org)
- [Flower](https://flower.dev), [NVIDIA FLARE](https://nvidia.github.io/NVFlare/)
- [Spin](https://spin.fermyon.dev), [Wasmtime](https://wasmtime.dev)
- [CrewAI](https://crewai.com), [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Helm](https://helm.sh), [Kustomize](https://kustomize.io), [Kyverno](https://kyverno.io)
- [Zeabur](https://zeabur.com), [Northflank](https://northflank.com), [Scaleway](https://scaleway.com), [Exoscale](https://exoscale.com)
- [Robot Framework](https://robotframework.org)

> Made with care by the [quantumworld-dpdns-io](https://github.com/quantumworld-dpdns-io) community.
