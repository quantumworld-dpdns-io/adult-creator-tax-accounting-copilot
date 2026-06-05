---
name: w8ben
description: Generate IRS Form W-8BEN for non-US creators.
version: 1.0.0
license: MIT
tags: [tax, us, w-8ben]
---

# W-8BEN

## Inputs

- `creator_id` *(string)*
- `treaty_country` *(ISO 3166-1 alpha-2)*

## Steps

1. Pull creator identity (KYC-verified).
2. Determine treaty rate for the country.
3. Render PDF.
4. Sign (Dilithium-5).
5. Store in S3 + send to payment platform.

## Tools

- `mcp:file_w8ben`
