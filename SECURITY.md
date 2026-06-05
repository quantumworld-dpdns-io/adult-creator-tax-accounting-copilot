# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities to **security@quantumworld-dpdns-io.example**.

- Use GPG key in `/SECURITY.md` (this file) for sensitive disclosures.
- We aim to acknowledge within 48h and patch within 14 days for high-severity.
- We follow responsible disclosure: do not open public issues for vulns.

## Security Posture

- **Quantum-safe**: Kyber-1024 + Dilithium-3 hybrid (X25519+Kyber TLS, Ed25519+Dilithium signing).
- **PQC audit log**: BLAKE3 hash chain + Dilithium signatures, replicated to OCI Object Storage.
- **Confidential compute**: Teaclave enclaves for tax-form decryption.
- **Zero-trust**: Linkerd mTLS (PQC) + Cilium Tetragon eBPF policies.
- **SBOM**: syft-generated per release; Grype + Trivy scans in CI.
- **SLSA Level 3** provenance; cosign keyless signing.

## OWASP Coverage

- ASVS L2: full
- Top-10 2021: full
- API Security Top-10: full
- Robot Framework suites in `tests/robot/owasp/`
