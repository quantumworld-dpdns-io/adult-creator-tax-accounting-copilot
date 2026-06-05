# ADR 0003: Quantum-Safe Audit Log

## Status

Accepted.

## Context

Audit logs must be tamper-evident and survive quantum adversaries. Harvest-now-
decrypt-later attacks mean we must sign with post-quantum schemes today.

## Decision

The audit log uses:

1. **BLAKE3** hash chain (each entry includes the previous hash).
2. **Dilithium-3** signature per entry.
3. **Kyber-1024** envelope encryption for any sensitive payload.
4. **Qiskit-generated random** for key-derivation salt.
5. **OCI Object Storage** as the canonical archive.
6. **Local Postgres** for indexed search.

## Consequences

- All audit log APIs require a Dilithium public key registration.
- Each release ships a `verify_audit.py` tool.
- Slower writes (~3ms per entry) — acceptable for tax-grade audit.
