---
name: quantum-audit
description: Quantum-safe audit log entry (BLAKE3 chain + Dilithium signature).
version: 1.0.0
license: MIT
tags: [quantum, pqc, audit]
---

# Quantum-Safe Audit Log

## Properties

- **BLAKE3** hash chain (each entry references previous).
- **Dilithium-5** signature per entry.
- **Kyber-1024** envelope encryption for any sensitive payload.
- Mirrored to OCI Object Storage.
- Verifiable offline with `scripts/verify_audit.py`.

## Why

Harvest-now-decrypt-later attacks mean classical signatures (RSA/ECDSA) are
no longer sufficient for long-lived audit data.
