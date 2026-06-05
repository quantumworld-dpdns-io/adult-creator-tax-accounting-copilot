# Threat Model (STRIDE summary)

| Category | Threat | Mitigation |
| -------- | ------ | ---------- |
| **S**poofing | Stolen JWT / API key | OAuth2 + mTLS (PQC) + workload identity (SPIFFE) |
| **T**ampering | Modified tax form | PQC-signed audit log (Dilithium) + hash chain |
| **R**epudiation | "I never filed that" | Quantum-safe audit log with millisecond timestamps |
| **I**nformation Disclosure | PII leak | PII tokenization + Teaclave enclaves + eBPF DLP |
| **D**enial of Service | DDoS | WAF + ModSecurity + bot defense + autoscaling |
| **E**levation of Privilege | Tenant boundary breach | RLS, OPA, Robot A01/BOLA suites |

## Quantum-Specific

- **Harvest-now-decrypt-later**: PQC everywhere (Kyber-1024 + Dilithium-3).
- **Shor's algorithm**: rotate any RSA/DH keys > 2048-bit pre-2027.
- **Q-day planning**: incident response runbook `docs/runbook/quantum-incident.md`.

## Out of Scope

- Physical security of data centers (PaaS provider responsibility).
- End-user device compromise (mitigated via Tetragon at server).
- Side-channel on user-side browsers (mitigated via Tetragon uprobe).
