# Quantum Security Whitepaper

> Harvest-now-decrypt-later (HNDL) attacks mean classical signatures and
> key-exchange are no longer sufficient for long-lived data. The
> Adult Creator Tax & Accounting Copilot adopts a post-quantum security
> posture from day one.

## Threat model

1. **HNDL**: Adversary records TLS traffic now, decrypts later with a
   cryptographically-relevant quantum computer (CRQC).
2. **Impersonation**: Adversary signs a malicious tax form with a stolen
   RSA / ECDSA key.
3. **Audit-log forgery**: Adversary tampers with a 7-year tax-audit log.

## Mitigations

### 1. Hybrid TLS (X25519 + Kyber-1024)

We deploy OpenSSL with the `oqs-provider`, configured for
`X25519MLKEM1024` (X25519 + Kyber-1024). Even if a CRQC breaks X25519,
Kyber-1024 still secures the session.

### 2. Hybrid signatures (Ed25519 + Dilithium-5)

All releases are signed with `Ed25519+Dilithium-5`. Container images
are signed with `cosign` (keyless via Fulcio + Rekor). The audit log
is signed with Dilithium-5 alone (Ed25519 is unnecessary in this
context; we only need forgery resistance).

### 3. Quantum-entropy keygen

All long-term keys are seeded with bits from the ANU QRNG API
(or IBM Quantum), passed through BLAKE3.

### 4. Quantum-safe audit log

Each audit-log entry includes:

- The previous entry's BLAKE3 hash (chain).
- The current entry's BLAKE3 hash.
- A Dilithium-5 signature.
- A Kyber-1024 envelope for any sensitive payload.

This produces a tamper-evident log that can be verified offline with
`scripts/verify_audit.py`.

## Migration timeline

| Year | Milestone |
| ---- | --------- |
| 2024 | PQC hybrid TLS in dev / staging |
| 2025 | PQC hybrid TLS in prod (alongside classical) |
| 2026 | Internal mTLS: PQC-only via Linkerd |
| 2027 | All classical certs deprecated; Dilithium-only signed releases |
| 2028+ | Rotate any RSA-2048 / DH-2048 keys still in use |

## References

- NIST FIPS 203 (Kyber / ML-KEM)
- NIST FIPS 204 (Dilithium / ML-DSA)
- NIST FIPS 205 (SPHINCS+ / SLH-DSA)
- IETF draft-ietf-tls-hybrid-design
- Cloudflare Post-Quantum at scale
