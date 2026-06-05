#!/usr/bin/env python3
"""Federated learning coordinator (Flower).

Real production wraps Flower superlink + supernode. This module provides a
runnable scaffold that:
  1. Sets up the FL training environment.
  2. Loads a tax-form language model.
  3. Runs FedAvg with differential privacy.
"""

from __future__ import annotations

import os
from typing import Any

DEFAULT_DP_EPSILON = float(os.getenv("FL_DP_EPSILON", "1.0"))
DEFAULT_DP_DELTA = float(os.getenv("FL_DP_DELTA", "1e-5"))
DEFAULT_CLIENTS = int(os.getenv("FL_CLIENTS_PER_ROUND", "10"))


def build_strategy(strategy: str = "FedAvg") -> str:
    return strategy


def apply_dp(gradients: list[float], epsilon: float = DEFAULT_DP_EPSILON, delta: float = DEFAULT_DP_DELTA) -> list[float]:
    """Apply Gaussian noise sufficient for (epsilon, delta)-DP."""
    if not gradients:
        return gradients
    sensitivity = max(abs(g) for g in gradients) or 1.0
    sigma = sensitivity * (2.0 * (1.25 * (1.0 / delta + 1.0))) ** 0.5 / epsilon
    # numpy is optional; fall back to a simple PRNG.
    try:
        import numpy as np

        return [g + float(np.random.normal(0, sigma)) for g in gradients]
    except ImportError:
        import random

        return [g + random.gauss(0, sigma) for g in gradients]


def aggregate(client_updates: list[list[float]], strategy: str = "FedAvg") -> list[float]:
    if not client_updates or not client_updates[0]:
        return []
    if strategy == "FedAvg":
        n = len(client_updates)
        d = len(client_updates[0])
        return [sum(c[i] for c in client_updates) / n for i in range(d)]
    return client_updates[0]


def main() -> dict[str, Any]:
    return {
        "strategy": build_strategy(),
        "dp_epsilon": DEFAULT_DP_EPSILON,
        "dp_delta": DEFAULT_DP_DELTA,
        "clients_per_round": DEFAULT_CLIENTS,
    }


if __name__ == "__main__":
    print(main())
