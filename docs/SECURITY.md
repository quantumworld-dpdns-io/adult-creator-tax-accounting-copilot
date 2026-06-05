# Security

> Public-facing security overview for the adult-creator tax & accounting copilot.

This document complements [`SECURITY.md`](../SECURITY.md) (vulnerability-disclosure policy) and [`docs/THREAT_MODEL.md`](THREAT_MODEL.md) (STRIDE model). It describes the controls, standards, and audit trails that protect creator data.

## 1. Standards we follow

- **OWASP ASVS L2** — verified in CI (`tests/robot/owasp/`)
- **OWASP Top-10 2021** — A01-A10, each with a Robot test scenario
- **OWASP API Top-10** — API1-API10, each with a Robot test scenario
- **NIST SP 800-208** — Kyber-1024, Dilithium-5
- **NIST SP 800-56A** — hybrid PQC + X25519 key agreement
- **NIST SP 800-38D** — AES-256-GCM
- **GDPR** — lawfulness, minimisation, purpose limitation, retention, DSAR
- **2257 / 2257A** — model-release evidence chain
- **PCI-DSS** (data-flow adjacent only; we never store card data)
- **SOC 2 Type II** — control evidence exportable from the audit log

## 2. Cryptography

| Primitive | Choice | Why |
|---|---|---|
| Symmetric | AES-256-GCM | NIST-approved AEAD |
| Hash | BLAKE3 | Fast, quantum-safe birthday bound, used in chains |
| KEM | Kyber-1024 | NIST PQC round 3 winner, ML-KEM-1024 |
| Signature | Dilithium-5 | NIST PQC round 3 winner, ML-DSA-87 |
| TLS | TLS 1.3 + PQC | nginx terminates; prefers `KYBER_AES_256_GCM_SHA384`, falls back to `X25519_AES_256_GCM_SHA384` |
| EdDSA | Ed25519 (legacy interop) | Used in non-PQC paths only |
| Storage | age + Argon2id | At-rest encryption of creator uploads |

### Quantum-safe audit log

Every ledger entry is:

```
entry = {
  seq: u64,
  payload: <creator_action>,
  prev_hash: BLAKE3,
  hash: BLAKE3( prev_hash || payload ),
  signature: Dilithium5.sign( hash, ledger_key ),
  nonce: qrng.bits(256)   ← quantum entropy
}
```

Offline verification: `python scripts/verify_audit.py --log <file>` (see `scripts/verify_audit.py`).

## 3. Identity & access

- OIDC (Keycloak or cloud-managed) at the edge
- JWT propagation via Istio request-auth
- Per-service mTLS inside the mesh
- Service accounts with short-lived tokens (Vault dynamic secrets)
- Admin actions gated by `step-up` MFA

## 4. Network

- Cilium / Calico `NetworkPolicy` — default-deny per namespace
- Istio `AuthorizationPolicy` — explicit allow-rules per workload
- nginx edge with PQC TLS, OWASP security headers, mod_evasive, geo-block
- Rate-limit: 100 rps per IP, 10 rps per token, 1 rps per webhook secret
- WAF rules: SQLi, XSS, LFI, RCE, SSRF (`tests/robot/owasp/a03_injection.robot`)

## 5. Application security

- SAST: CodeQL, Semgrep, gosec, bandit, cargo-audit, npm audit, pip-audit
- DAST: OWASP ZAP baseline in `ci.yml`
- SCA: dependabot + renovate + `cargo audit` + `npm audit` + `pip-audit`
- Container: Trivy + Grype, base images cosign-signed
- IaC: Checkov, tfsec, conftest, kics
- Secret scanning: gitleaks + TruffleHog
- SBOM: CycloneDX, generated on every release
- SLSA: Level 3 provenance

## 6. Data protection

- Field-level encryption for TIN, banking, address
- KYC documents encrypted with per-creator DEK, KMS-wrapped KEK
- Tokenisation of bank-account numbers
- PII redaction in logs (Loki rules)
- Right-to-erasure: hard delete + crypto-shred the DEK
- Data-residency: per-cloud, configurable jurisdiction
- Retention: 7y (tax), 30d (logs), 90d (backups), then crypto-shred

## 7. Privacy

- Differential privacy ε=1.0 in federated fraud model
- Zero-knowledge proofs for age & income range
- WASM plugins run sandboxed by capability
- Audit log does not contain plaintext PII; only references
- DSAR self-service portal: `services/consent/`

## 8. Incident response

- Severity 1 → 15 min response, on-call rotation
- Forensics: read-only audit log + OTel traces
- Communication: status page + per-creator email
- Disclosure: 90-day coordinated disclosure (see `SECURITY.md`)
- Tabletop exercises quarterly

## 9. Compliance evidence

The audit log + reporting service produces:
- 1099-NEC / 1099-MISC / W-8BEN / W-8BEN-E
- EU VAT-MOSS return
- 2257 custodian statement
- SOC 2 control evidence export
- PCI-DSS scope attestation (out of scope for card data)

## 10. Bug bounty

- Scope: anything in this repo + the four cloud deployments
- Out of scope: third-party platforms (OnlyFans, Fansly, etc.)
- Bounties: Hall of fame + swag; monetary bounties TBD

Report privately via the process in [`SECURITY.md`](../SECURITY.md).
