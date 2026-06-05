# ADR 0007: ZK Proofs for Tax Compliance

## Status

Accepted.

## Context

Creators want to prove things ("I earned > $600", "I am 18+", "I am tax-
compliant in X jurisdiction") without leaking the underlying data.

## Decision

- **Noir** for SNARK circuits targeting bn254 and bls12_381.
- **RISC Zero** for general zkVM receipts.
- **Verifier** is a small WASM component (Wasmtime/Fermyon Spin).
- Proofs are stored on S3 with PQC-signed envelope.

## Consequences

- A new service `svc/zkservice` handles proving/verification.
- Robot Framework ZK suite verifies correctness on every release.
