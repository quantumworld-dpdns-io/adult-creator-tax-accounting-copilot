# ZK Proofs

This directory contains zero-knowledge proof circuits and the verifier WASM
component.

## Layout

| Subdirectory | Description |
| ------------ | ----------- |
| `noir/`      | Noir circuits (Noir is an Aztec DSL targeting Aztec's barretenberg backend) |
| `risc0/`     | RISC Zero zkVM guest + host programs |
| `verifier/`  | Tiny WASM verifier (Wasmtime / Fermyon Spin) |
| `docs/`      | Threat model and integration docs |

## Use cases

1. **Age verification** — `prove_age`: prove creator is ≥ 18 without revealing DOB.
2. **Income range** — `prove_income_range`: prove income in a USD range.
3. **Residency** — `prove_residency`: prove residency without revealing address.
4. **Sanctions clean** — `prove_sanctions_clean`: prove no sanctions hit.
5. **Tax-paid proof** — `prove_VAT_paid`: prove EU VAT was paid in a period.

## Build

```bash
# Noir
cd zk/noir/prove_age
nargo prove

# RISC Zero
cd zk/risc0/host
cargo run --release

# Verifier
cd zk/verifier
cargo build --release --target wasm32-wasi
```

## Verification

A verifying service `svc/zk-service` exposes `/v1/zk/verify`. It accepts a
proof blob and public inputs, and returns `valid: bool`.

## Threat model

- **Soundness**: the verifier is binding — a valid proof implies the
  statement.
- **Zero-knowledge**: the proof reveals nothing about the witness.
- **Quantum-safety**: when a CRQC arrives, we replace the inner curve
  with a STARK / hash-based SNARK (e.g. Plonky3, halo2 with
  hash-based arity). The verifier stays compatible.
