# Tooling

> Mapping of every tool in the 16-section Software Tools Index to the corresponding file or directory in this repository.

This is the canonical answer to *"is tool X actually wired up?"*. If something in the index is missing here, the implementation is incomplete.

## 1. Languages & runtimes

| Tool | Location |
|---|---|
| Python 3.14 (uv workspace) | `pyproject.toml`, `services/tax-engine/`, `quantum/`, `services/mcp-server-python/`, `services/reporting/`, `agents/` |
| Go 1.26 (modules) | `services/kyc/`, `services/consent/`, `services/ledger/`, `services/crypto-tax/`, `services/mcp-server-go/`, `services/api-gateway/` |
| Node 22 / TypeScript | `services/webhook-router/`, `services/mcp-server-node/`, `apps/web/`, `package.json` |
| Rust 1.85 (workspace) | `services/realtime-pricing/`, `zk/verifier/`, `wasm/components/`, `federated/flare/`, `services/mcp-server-rust/`, `Cargo.toml` |

## 2. Package managers

| Tool | Manifest |
|---|---|
| uv | `pyproject.toml` |
| go mod | `services/*/go.mod` |
| pnpm | `package.json` (root workspace) |
| cargo | `Cargo.toml` (root workspace) |
| helm | `helm/Chart.yaml` |
| pulumi | `infra/pulumi/*/Pulumi.yaml` |
| terraform | `infra/terraform/*/main.tf` |
| ansible | `infra/ansible/playbooks/` |

## 3. Container & orchestration

| Tool | File |
|---|---|
| Docker (multi-stage) | `docker/Dockerfile.{python,go,node,rust}` |
| Docker Compose | `docker-compose.dev.yml` |
| Kubernetes manifests | `k8s/base/`, `k8s/overlays/{dev,prod}/` |
| Helm umbrella | `helm/Chart.yaml` |
| Kustomize | `k8s/*/kustomization.yaml` |
| Dev container | `.devcontainer/` |

## 4. Microservices

| Service | File |
|---|---|
| API gateway | `services/api-gateway/`, `helm/charts/api-gateway/` |
| Tax engine (Go) | `services/tax-engine/src/main.go` |
| Tax engine (Py) | `services/tax-engine/src/tax_engine/app.py` |
| Crypto tax | `services/crypto-tax/pkg/cryptotax.go` |
| KYC | `services/kyc/kyc.go` |
| Consent / DSAR | `services/consent/main.go` |
| Ledger | `services/ledger/cmd/ledger/main.go` |
| Real-time pricing | `services/realtime-pricing/src/main.rs` |
| Reporting | `services/reporting/statement.py` |
| Webhook router | `services/webhook-router/src/main.ts` |
| Web app | `apps/web/src/app/` |

## 5. MCP (Model Context Protocol)

| Tool | File |
|---|---|
| Python MCP server | `services/mcp-server-python/src/mcp_server_python/` |
| Go MCP server | `services/mcp-server-go/` |
| Node MCP server | `services/mcp-server-node/` |
| Rust MCP server | `services/mcp-server-rust/src/` |
| OpenAPI spec | `mcp/openapi.yaml` |
| OpenAPI → MCP generator | `mcp/generators/openapi2mcp.ts` |
| DXT bundles | `mcp/dxt/` |
| `.mcp.json` | `.mcp.json` |

## 6. Agent skills

| Skill | File |
|---|---|
| tax-1099 | `.skills/tax-1099/SKILL.md` + `skill.json` |
| crypto-fifo | `.skills/crypto-fifo/SKILL.md` + `skill.json` |
| vat-moss | `.skills/vat-moss/SKILL.md` + `skill.json` |
| w8ben | `.skills/w8ben/SKILL.md` + `skill.json` |
| kyc-aml | `.skills/kyc-aml/SKILL.md` + `skill.json` |
| zkp-age | `.skills/zkp-age/SKILL.md` + `skill.json` |
| zkp-income | `.skills/zkp-income/SKILL.md` + `skill.json` |
| quantum-audit | `.skills/quantum-audit/SKILL.md` + `skill.json` |

## 7. Quantum computing

| Tool | File |
|---|---|
| CUDA-Q kernels | `quantum/cudaq/kernels.py` |
| Qiskit kernels | `quantum/qiskit/kernels.py` |
| QRNG service | `quantum/qrng/service.py`, `quantum/qrng/api.py` |
| Quantum benchmarks | `quantum/bench/test_kernels.py` |
| Quantum docs | `quantum/docs/{gallery.md, security-whitepaper.md}` |

## 8. Zero-knowledge proofs

| Tool | File |
|---|---|
| Noir age | `zk/noir/prove_age/src/main.nr` |
| Noir income range | `zk/noir/prove_income_range/src/main.nr` |
| RISC Zero guest | `zk/risc0/methods/guest/src/main.rs` |
| RISC Zero host | `zk/risc0/host/src/main.rs` |
| Verifier (Rust) | `zk/verifier/verify.rs` |
| ZK docs | `zk/docs/{README.md, threat-model.md}` |

## 9. WASM

| Tool | File |
|---|---|
| Wasmtime container | `wasm/wasmtime/Dockerfile` |
| Spin component | `wasm/spin/src/lib.rs` |
| Spin manifest | `wasm/spin/spin.toml` |
| Tax-form validator component | `wasm/components/tax_form_validator.rs` |
| Component manifest | `wasm/components/Cargo.toml` |

## 10. Federated learning

| Tool | File |
|---|---|
| Flower coordinator | `federated/flower/coordinator.py` |
| NVIDIA FLARE client | `federated/flare/client.rs` |
| FLARE Cargo | `federated/flare/Cargo.toml` |

## 11. Apache projects

| Project | File |
|---|---|
| Polaris catalog | `apache/polaris/config.toml` |
| Teaclave policy | `apache/teaclave/policy.yaml` |
| Gluten config | `apache/gluten/config.yaml` |
| Gravitino metalake | `apache/gravitino/metalake.yaml` |

## 12. Multi-agent frameworks

| Framework | File |
|---|---|
| CrewAI tax analyst | `agents/crewai/tax_analyst.py` |
| LangGraph tax filing | `agents/langgraph/tax_filing.py` |

## 13. IaC

| Tool | Location |
|---|---|
| Pulumi (Zeabur) | `infra/pulumi/zeabur/index.ts` |
| Pulumi (Northflank) | `infra/pulumi/northflank/index.ts` |
| Pulumi (Scaleway) | `infra/pulumi/scaleway/index.ts` |
| Pulumi (Exoscale) | `infra/pulumi/exoscale/index.ts` |
| Terraform (Zeabur) | `infra/terraform/zeabur/main.tf` |
| Terraform (Northflank) | `infra/terraform/northflank/main.tf` |
| Terraform (Scaleway) | `infra/terraform/scaleway/main.tf` |
| Terraform (Exoscale) | `infra/terraform/exoscale/main.tf` |
| Ansible playbooks | `infra/ansible/playbooks/{bootstrap,cilium,vault,postgres-tune}.yml` |
| Ansible roles | `infra/ansible/roles/{k8s-common,k8s-gpu-node,k8s-confidential}/tasks/main.yml` |
| Inventory | `infra/ansible/inventories/prod.ini` |

## 14. CI/CD

| Workflow | File |
|---|---|
| CI | `.github/workflows/ci.yml` |
| Release | `.github/workflows/release.yml` |
| Security | `.github/workflows/security.yml` |
| Multi-cloud deploy | `.github/workflows/multi-cloud-deploy.yml` |
| Quantum + ZK | `.github/workflows/quantum-zk.yml` |
| Dependabot | `.github/dependabot.yml` |
| Renovate | `renovate.json` |
| Issue templates | `.github/ISSUE_TEMPLATE/{bug,feature,security}.md` |
| PR template | `.github/PULL_REQUEST_TEMPLATE.md` |

## 15. Testing

| Suite | File |
|---|---|
| Quantum kernels (pytest) | `quantum/bench/test_kernels.py` |
| QRNG API (pytest) | `quantum/qrng/tests/test_api.py` |
| Tax engine (pytest) | `services/tax-engine/tests/test_app.py` |
| MCP server (pytest) | `services/mcp-server-python/tests/test_server.py` |
| KYC (go test) | `services/kyc/kyc_test.go` |
| Consent (go test) | `services/consent/main_test.go` |
| Crypto-tax (go test) | `services/crypto-tax/main_test.go` |
| OWASP Top-10 | `tests/robot/owasp/a0{1..9}_*.robot`, `a10_*.robot` |
| OWASP API Top-10 | `tests/robot/api/api_top10.robot` |
| Tax E2E | `tests/robot/tax/tax_estimates.robot` |
| Quantum E2E | `tests/robot/quantum/qrng.robot` |
| ZK E2E | `tests/robot/zk/zk_verify.robot` |
| Payments E2E | `tests/robot/payments/webhooks.robot` |
| Common helpers | `tests/robot/common.robot` |
| Sample data | `tests/fixtures/` |
| Audit verifier | `scripts/verify_audit.py` |
| OWASP quick check | `scripts/owasp_quick_check.sh` |

## 16. Documentation & governance

| Item | File |
|---|---|
| README | `README.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| Security | `docs/SECURITY.md`, `SECURITY.md` |
| Quick start | `docs/QUICKSTART.md` |
| Tooling (this file) | `docs/TOOLING.md` |
| Roadmap | `docs/ROADMAP.md` |
| Threat model | `docs/THREAT_MODEL.md` |
| Branching | `docs/BRANCHING.md` |
| Code style | `docs/CODE_STYLE.md` |
| Governance | `docs/GOVERNANCE.md` |
| Contributing | `docs/CONTRIBUTING.md` |
| ADRs | `docs/adr/0001-0009-*.md` |
| Devin runbooks | `docs/runbook/devin/*.md` |
| CODEOWNERS | `CODEOWNERS` |
| Code of conduct | `CODE_OF_CONDUCT.md` |
| License | `LICENSE` |
| Changelog | `CHANGELOG.md` |
| Support | `SUPPORT.md` |
| Security policy | `SECURITY.md` |
| API specs | `docs/api/` |

## 17. Configuration

| Item | File |
|---|---|
| Python workspace | `pyproject.toml` |
| Node workspace | `package.json` |
| Rust workspace | `Cargo.toml` |
| Go modules | `services/*/go.mod` |
| opencode | `opencode.json` |
| Claude Code | `.claude/CLAUDE.md`, `.claude/commands/*.md` |
| Codex | `.codex/agents.json` |
| Hermes | `hermes.yml` |
| MCP root | `.mcp.json` |
| Editor config | `.editorconfig` |
| Git attributes | `.gitattributes` |
| Git ignore | `.gitignore` |
| Docker ignore | `.dockerignore` |
| npm config | `.npmrc` |
| Pre-commit | `.pre-commit-config.yaml` |
| Commitlint | `commitlint.config.js` |
| Env example | `.env.example` |
| Version pins | `.python-version`, `.nvmrc`, `.go-version`, `rust-toolchain.toml` |
| Feature flags | `config/flags.yaml` |
| Schemas | `config/schemas/` |

## 18. Observability & secrets

| Tool | File |
|---|---|
| Prometheus | `infra/observability/prometheus.yml` (compose) |
| Grafana | `infra/observability/grafana/` (compose) |
| Loki | compose |
| Tempo | compose |
| Mimir | compose |
| OTel | compose |
| Phoenix (LLM) | compose |
| Vault | compose, `infra/ansible/playbooks/vault.yml` |

## 19. Multi-cloud matrix

| Cloud | Pulumi | Terraform | Helm | Notes |
|---|---|---|---|---|
| Zeabur | ✓ | ✓ | ✓ | Free tier friendly |
| Northflank | ✓ | ✓ | ✓ | Managed k8s |
| Scaleway | ✓ | ✓ | ✓ | EU sovereignty |
| Exoscale | ✓ | ✓ | ✓ | CH sovereignty |
