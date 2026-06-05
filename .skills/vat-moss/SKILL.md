---
name: vat-moss
description: Aggregate EU VAT Mini One-Stop-Shop obligations for a creator.
version: 1.0.0
license: MIT
tags: [vat, eu, moss]
---

# VAT MOSS / OSS

## Inputs

- `creator_id` *(string)*
- `period` *(string)* — `YYYY-Q` or `YYYY-MM`

## Steps

1. Pull EU-destined transactions for the period.
2. Apply destination-country VAT rate.
3. Group by member state.
4. Generate the OSS VAT return XML (schema-validated).
5. Sign with **Dilithium-5**.
6. Submit via member-state API (or hand off to accountant).

## Tools

- `mcp:aggregate_vat`
- `svc/tax-engine`

## Notes

- Replaces legacy MOSS from 2021.
- Quarterly cadence (Q1=Apr, Q2=Jul, Q3=Oct, Q4=Jan).
- Annual recapitulative by Jan 31.
