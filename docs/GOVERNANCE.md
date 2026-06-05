# Governance

## Roles

| Role | Responsibility | Members |
| ---- | -------------- | ------- |
| Maintainers | Approve, merge, release | @quantumworld-dpdns-io/maintainers |
| Security     | Triage vulns, sign releases | @quantumworld-dpdns-io/security |
| Quantum      | Quantum features, PQC, QML | @quantumworld-dpdns-io/quantum |
| ZK           | Noir, RISC Zero circuits | @quantumworld-dpdns-io/zk |
| Backend      | Microservices, K8s, IaC | @quantumworld-dpdns-io/backend |
| Frontend     | Next.js, DX | @quantumworld-dpdns-io/frontend |
| QA           | Robot Framework, OWASP | @quantumworld-dpdns-io/qa |

## Decision-Making

- **Lazy consensus** for routine PRs (24h window).
- **Supermajority (3/4)** for breaking changes.
- **Unanimous** for security-sensitive merges.

## On-Call Rotation

Weekly rotation; PagerDuty-compatible. See `docs/runbook/on-call.md`.
