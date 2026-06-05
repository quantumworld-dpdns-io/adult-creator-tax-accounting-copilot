---
name: kyc-aml
description: Run KYC/AML/sanctions screening for a creator onboarding.
version: 1.0.0
license: MIT
tags: [kyc, aml, sanctions]
---

# KYC/AML

## Steps

1. Document OCR (ID + selfie).
2. Liveness check.
3. Sanctions screening (OFAC, EU, UN, UK).
4. PEP screening.
5. Adverse-media search.
6. Decision: approve / manual review / reject.
7. Audit-log every step (BLAKE3 + Dilithium).

## Tools

- `svc/kyc` (Persona, Onfido, Sumsub)
- `mcp:verify_age_zk` (preferred over storing DOB)
