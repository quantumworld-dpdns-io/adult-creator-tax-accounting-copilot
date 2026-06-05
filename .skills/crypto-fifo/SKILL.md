---
name: crypto-fifo
description: |
  Compute realized gains for crypto-denominated creator payouts using
  FIFO, LIFO, HIFO, or Specific Identification. Handles bridges, airdrops,
  staking, DeFi yield, and stablecoin depeg events.
version: 1.0.0
license: MIT
tags: [crypto, tax, fifo]
---

# Crypto FIFO / Cost-Basis

## Inputs

- `creator_id` *(string, required)*
- `tax_year` *(integer, required)*
- `method` *(enum, default "FIFO")* — `FIFO`, `LIFO`, `HIFO`, `SpecID`
- `chains` *(array, default ["ethereum","base","arbitrum","solana","bitcoin"])*

## Steps

1. Pull on-chain transactions from `svc/crypto-tax` (Arrow IPC).
2. For each acquisition, record cost basis in USD (use median from 5 sources).
3. For each disposition, match by `method`.
4. Account for airdrops (income at FMV on receipt date).
5. Account for staking (income at FMV on receipt date).
6. Account for DeFi yield (basis snapshot method).
7. Output Form 8949 CSV + IRS Form 1040 Sch D summary.

## Tools

- `mcp:get_payouts`
- `mcp:prove_income_range` (optional, for ZK privacy)

## Quantum

- Wallet addresses never appear in the output (only anonymized HMACs).
- All storage encrypted with **Kyber-1024**.
