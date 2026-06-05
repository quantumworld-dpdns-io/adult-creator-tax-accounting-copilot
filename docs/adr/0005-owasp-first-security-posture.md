# ADR 0005: OWASP-First Security Posture

## Status

Accepted.

## Context

A financial/compliance system must be secure-by-design, not retrofitted.

## Decision

- **OWASP ASVS Level 2** is the minimum bar; Level 3 for tax-grade flows.
- **OWASP Top-10 2021** + **API Security Top-10** covered by Robot Framework.
- **ZAP** baseline + authenticated scans in CI.
- **SLSA Level 3** provenance + cosign keyless signing.
- **SBOM** per release (syft, VEX via grype).
- **Threat model** updated per PR (STRIDE).

## Consequences

- All PRs run the full Robot OWASP suite.
- Pipeline failures block merges.
- Quarterly external pen-test.
