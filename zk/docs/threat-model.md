# ZK Threat Model

## Adversary capabilities

- **HNDL**: record all public inputs + proofs now, attack later.
- **Active**: send malicious proofs.
- **Coercer**: trick the user into revealing witness.

## Mitigations

1. **Sound circuit**: unit-tested, fuzz-tested, audit-reviewed.
2. **Small public inputs**: nothing of value leaks via the public inputs.
3. **Bounded proofs**: proofs expire (TTL in the public inputs).
4. **Revocation list**: a service maintains a revocation list of
   expired / invalidated proofs.
5. **Hybrid signature**: proofs are wrapped in a Dilithium-5 signature
   to prevent forgery of the *envelope*.
6. **WASM verifier**: the verifier runs in a TEE (Teaclave) or a
   WASM sandbox; even a compromised host cannot lie about the result.

## Out of scope

- Privacy of the public inputs themselves (the creator must understand
  what they reveal).
- Side-channel attacks on the prover (e.g. voltage analysis on hardware
  wallets).
