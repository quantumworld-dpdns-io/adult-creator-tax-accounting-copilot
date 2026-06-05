# ADR 0008: Federated Learning for Personalization

## Status

Accepted.

## Context

We want to fine-tune the LLM per-creator without centralizing private financial
data.

## Decision

- **Flower** as the framework (Python + Rust core).
- **NVIDIA FLARE** for jobs that need homomorphic encryption.
- **Differential privacy** (Gaussian, ε=1.0, δ=1e-5) on every round.
- **Secure aggregation** plugin.

## Consequences

- New service `svc/fl-coordinator`.
- Per-region supernode residency (EU/US/APAC).
- Daily automated audit log of every round.
