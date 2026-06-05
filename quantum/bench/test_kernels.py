"""Tests for the quantum kernels (CUDA-Q + classical fallbacks)."""
import os
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from quantum.cudaq.kernels import (  # noqa: E402
    qaoa_currency_basket,
    qrng_bits,
    seed_dilithium,
    seed_kyber,
    train_fraud_model,
    vqe_portfolio,
)
from quantum.qiskit.kernels import (  # noqa: E402
    qaoa_currency_basket as qaoa_qiskit,
    variational_fraud_classifier,
)


def test_qrng_length() -> None:
    assert len(qrng_bits(64)) == 16
    assert len(qrng_bits(128)) == 32


def test_qrng_uniqueness() -> None:
    seen = {qrng_bits(64) for _ in range(50)}
    assert len(seen) == 50


def test_seed_kyber_size() -> None:
    assert len(seed_kyber()) == 32


def test_seed_dilithium_size() -> None:
    assert len(seed_dilithium()) == 64


def test_qaoa_cudaq_basket() -> None:
    basket = qaoa_currency_basket(
        expected_returns=[0.05, 0.08, 0.03, 0.06],
        covariance=[[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    assert len(basket) == 4
    assert sum(basket) > 0


def test_qaoa_qiskit_basket() -> None:
    basket = qaoa_qiskit(
        expected_returns=[0.05, 0.08, 0.03, 0.06],
        covariance=[[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    assert len(basket) == 4


def test_train_fraud_model() -> None:
    model = train_fraud_model([
        ([0.1, 0.2, 0.3], 0),
        ([0.5, 0.6, 0.7], 1),
        ([0.2, 0.1, 0.4], 0),
        ([0.9, 0.8, 0.7], 1),
    ])
    assert len(model.weights) == 3


def test_vqe_portfolio_sums_to_one() -> None:
    weights = vqe_portfolio([0.25, 0.25, 0.25, 0.25], [0.05, 0.08, 0.03, 0.06], steps=20)
    assert abs(sum(weights) - 1.0) < 1e-2
    assert all(w >= 0 for w in weights)


def test_vqe_handles_zero_initial() -> None:
    weights = vqe_portfolio([0, 0, 0, 0], [0.05, 0.08, 0.03, 0.06], steps=10)
    assert sum(weights) > 0


def test_variational_fraud_classifier_range() -> None:
    score = variational_fraud_classifier([0.1, 0.2, 0.3], [0.4, 0.5, 0.6])
    assert 0.0 <= score <= 1.0
