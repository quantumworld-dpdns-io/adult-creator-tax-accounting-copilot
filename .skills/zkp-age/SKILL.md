---
name: zkp-age
description: Issue a ZK age proof for a creator (default ≥ 18).
version: 1.0.0
license: MIT
tags: [zk, noir, age]
---

# ZK Age Proof

## Inputs

- `creator_id` *(string)*
- `min_age` *(integer, default 18)*

## Tools

- `mcp:verify_age_zk`

## Backends

- `noir` (bn254) — primary
- `noir` (bls12_381) — alt
- `risc0` — for general zkVM

## Privacy

- The actual DOB **never** leaves the enclave (Teaclave / WASM-time-shielded).
- Only the proof is stored.
