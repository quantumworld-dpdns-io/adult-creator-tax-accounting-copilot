---
name: zkp-income
description: ZK proof that a creator's income is in a USD range.
version: 1.0.0
license: MIT
tags: [zk, noir, income]
---

# ZK Income Range Proof

## Inputs

- `creator_id` *(string)*
- `lower_usd` *(integer)*
- `upper_usd` *(integer)*

## Use cases

- Proving eligibility for the 1099-K threshold *without* revealing gross.
- Proving residency-based tax obligations *without* revealing exact income.
- Disclosing to a third-party auditor *without* revealing platform mix.

## Tools

- `mcp:prove_income_range`
