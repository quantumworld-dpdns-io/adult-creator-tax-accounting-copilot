# ADR 0006: Post-Quantum Cryptography Migration

## Status

Accepted.

## Context

NIST PQC standards (FIPS 203/204/205) finalize in 2024. "Harvest now, decrypt
later" means we must migrate now.

## Decision

- Hybrid: **X25519+Kyber-1024** TLS, **Ed25519+Dilithium-5** signing.
- liboqs is the reference implementation; **step-ca** issues PQC certs.
- All certs expire ≤ 24h; auto-rotation via cert-manager.
- Internal mTLS via Linkerd PQC profile.

## Consequences

- OpenSSL provider must be built with oqs-provider.
- Each release tests PQ TLS via Robot Framework.
