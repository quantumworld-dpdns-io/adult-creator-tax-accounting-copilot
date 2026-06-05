# Federated Learning (Flower + NVIDIA FLARE)
#
# We use **Flower** as the primary framework. NVIDIA FLARE is integrated for
# jobs that require homomorphic encryption.

# How FL is used here

The Adult Creator Tax & Accounting Copilot uses federated learning to
personalize a small per-creator LLM (typically a LoRA adapter) **without
centralizing private financial data**.

# Threat model

- **Honest-but-curious server**: server sees only encrypted + differentially-
  private gradients. Cannot recover individual creator data.
- **Malicious clients**: outlier detection (multi-Krum) drops poisoned
  updates. Each client receives a health check.
- **Membership inference**: DP budget is tracked; ε is capped at 1.0/round.

# Architecture

```text
  creator device     supernode       superlink       ledger
  +-------------+   +----------+    +-----------+   +--------+
  | on-device   |---| Flower   |--- | Flower    |---| model  |
  | LoRA train  |   | supernode|    | superlink |   | registry
  +-------------+   +----------+    +-----------+   +--------+
        |                                |
        +---------> FLARE <--------------+
                   (HE-filter)
```

# Compliance

- GDPR Art. 22 (automated decision-making) — human review required for
  any FL-driven recommendation.
- Right-to-object — a creator can opt out at any time.
- Regional residency — supernode stays in creator's region.
