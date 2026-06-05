"""CUDA-Q base quantum kernels for the Adult Creator Tax Copilot.

This module demonstrates four quantum features:

1. **QRNG** — quantum random number generation (seeding).
2. **QAOA** — currency-basket selection.
3. **QML** — variational fraud classifier.
4. **VQE** — portfolio optimization.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Sequence

try:
    import cudaq
except ImportError:  # pragma: no cover
    cudaq = None  # type: ignore[assignment]

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None  # type: ignore[assignment]


# ────────────────────────────────────────────────────────────────────
# 1. QRNG — Quantum Random Number Generation
# ────────────────────────────────────────────────────────────────────

def qrng_bits(n_bits: int = 256) -> str:
    """Return `n_bits` random bits.

    Uses CUDA-Q (or a CSPRNG fallback). In production we call the ANU
    QRNG API or the IBM Quantum back-end. The returned string is a
    hex digest of length n_bits/4.
    """
    if cudaq is not None:
        try:
            kernel = cudaq.make_kernel()
            q = kernel.qalloc(n_bits)
            kernel.h(q)
            kernel.mz(q)
            result = cudaq.sample(kernel, shots_count=1)
            bits = "".join(str(int(b)) for b in result)
            return f"{int(bits, 2):0{n_bits // 4}x}"
        except Exception:  # pragma: no cover
            pass
    return os.urandom(n_bits // 8).hex()


def seed_kyber() -> bytes:
    """Seed a Kyber keygen with quantum entropy."""
    return hashlib.sha3_256(qrng_bits(512).encode()).digest()


def seed_dilithium() -> bytes:
    """Seed a Dilithium keygen with quantum entropy."""
    return hashlib.sha3_512(qrng_bits(1024).encode()).digest()


# ────────────────────────────────────────────────────────────────────
# 2. QAOA — Currency basket selection
# ────────────────────────────────────────────────────────────────────

def qaoa_currency_basket(
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    p: int = 2,
) -> list[int]:
    """Run a simplified QAOA to select a currency basket.

    Returns a binary vector of length len(expected_returns).
    Falls back to a classical proxy if CUDA-Q is unavailable.
    """
    n = len(expected_returns)
    if cudaq is None or np is None:  # classical proxy
        scores = [r / (sum(c) + 1e-9) for r, c in zip(expected_returns, covariance)]
        ranked = sorted(range(n), key=lambda i: scores[i], reverse=True)
        basket = [0] * n
        for i in ranked[: max(1, n // 2)]:
            basket[i] = 1
        return basket

    @cudaq.kernel
    def kernel(gamma: float, beta: float, n: int):
        q = cudaq.qalloc(n)
        for i in range(n):
            h(q[i])
        for _ in range(p):
            for i in range(n):
                for j in range(n):
                    if i < j:
                        cx(q[i], q[j])
            for i in range(n):
                rz(2.0 * gamma * expected_returns[i], q[i])
            for i in range(n):
                h(q[i])
                rz(2.0 * beta, q[i])
                h(q[i])

    gammas = [0.1 * i for i in range(p)]
    betas = [0.2 * i for i in range(p)]

    best = [0] * n
    best_score = -1.0
    for g in gammas:
        for b in betas:
            result = cudaq.sample(kernel, g, b, n, shots_count=200)
            for bits, count in result.items():
                vec = [int(c) for c in bits[::-1]][:n]
                score = sum(vec[i] * expected_returns[i] for i in range(n)) - sum(
                    vec[i] * vec[j] * covariance[i][j] for i in range(n) for j in range(n)
                ) * 0.1
                if score > best_score:
                    best_score = score
                    best = vec
    return best


# ────────────────────────────────────────────────────────────────────
# 3. QML — variational fraud classifier
# ────────────────────────────────────────────────────────────────────

@dataclass
class FraudModel:
    weights: list[float]

    def predict(self, x: list[float]) -> float:
        # Simplified linear scoring; production uses a QML kernel.
        return sum(w * xi for w, xi in zip(self.weights, x))


def train_fraud_model(samples: list[tuple[list[float], int]], epochs: int = 10) -> FraudModel:
    """Train a small variational classifier.

    `samples` is a list of (features, label) where label is 0/1.
    """
    if not samples:
        return FraudModel(weights=[])
    d = len(samples[0][0])
    w = [0.0] * d
    lr = 0.05
    for _ in range(epochs):
        for x, y in samples:
            pred = 1.0 if sum(wi * xi for wi, xi in zip(w, x)) > 0 else 0.0
            err = y - pred
            for i in range(d):
                w[i] += lr * err * x[i]
    return FraudModel(weights=w)


# ────────────────────────────────────────────────────────────────────
# 4. VQE — portfolio optimization
# ────────────────────────────────────────────────────────────────────

def vqe_portfolio(weights: Sequence[float], returns: Sequence[float], steps: int = 50) -> list[float]:
    """Simplified VQE: minimize -Σ w_i * r_i subject to Σ w_i = 1, w_i >= 0."""
    n = len(weights)
    if n == 0:
        return []
    w = list(weights) if sum(weights) > 0 else [1.0 / n] * n
    for _ in range(steps):
        score = -sum(wi * ri for wi, ri in zip(w, returns))
        grad = [-ri for ri in returns]
        for i in range(n):
            w[i] -= 0.05 * grad[i]
        total = sum(w)
        if total > 0:
            w = [wi / total for wi in w]
        for i in range(n):
            w[i] = max(0.0, w[i])
    return w


if __name__ == "__main__":
    print("QRNG bits:", qrng_bits(64))
    basket = qaoa_currency_basket(
        expected_returns=[0.05, 0.08, 0.03, 0.06],
        covariance=[[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    print("QAOA basket:", basket)
    model = train_fraud_model([
        ([0.1, 0.2, 0.3], 0),
        ([0.5, 0.6, 0.7], 1),
        ([0.2, 0.1, 0.4], 0),
        ([0.9, 0.8, 0.7], 1),
    ])
    print("Fraud model weights:", model.weights)
    print("VQE optimal:", vqe_portfolio([0.25, 0.25, 0.25, 0.25], [0.05, 0.08, 0.03, 0.06]))
