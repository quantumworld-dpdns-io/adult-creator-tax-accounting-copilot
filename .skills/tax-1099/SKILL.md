---
name: tax-1099
description: |
  Generate US 1099 tax forms (1099-NEC / 1099-MISC / 1099-K) for an
  adult content creator's aggregated payouts across platforms.
version: 1.0.0
author: quantumworld-dpdns-io
license: MIT
tags: [tax, us, 1099]
---

# Tax 1099

This skill walks an agent through producing a signed, quantum-safe 1099 PDF for
a given creator and year.

## Inputs

- `creator_id` *(string, required)* — The creator's unique identifier.
- `year` *(integer, required)* — Tax year.
- `form` *(enum, default "1099-NEC")* — Which 1099 form to produce.

## Steps

1. Call `mcp:get_payouts` for the year.
2. Filter by the 1099-NEC threshold ($600 in 2026) or 1099-K threshold
   (varies by state, default $5,000).
3. Call `mcp:compute_tax_estimate` for the year to get bracket context.
4. Generate the PDF via `svc/tax-engine`.
5. Sign with **Dilithium-5** (quantum-safe).
6. Upload to S3 with **Kyber-1024** envelope encryption.
7. Emit a `proof-of-filing` event to the quantum-safe audit log.

## Tools required

- `mcp:get_payouts`
- `mcp:compute_tax_estimate`
- `mcp:file_1099`

## Outputs

- `pdf_url` — S3 URI of the signed PDF.
- `signed` — Always `true` (PQC).
- `signature_algo` — `Dilithium-5`.

## Compliance

- IRS Pub 1220 (electronic filing) conformance.
- Quantum-safe audit-log entry per filing.
- Right-to-retain for 7 years.
