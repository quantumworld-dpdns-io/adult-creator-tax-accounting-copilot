"""Quantum-simulator benchmark harness."""

from __future__ import annotations

import time
from typing import Any

import pytest

from quantum.cudaq.kernels import (
    qaoa_currency_basket,
    qrng_bits,
    seed_dilithium,
    seed_kyber,
    train_fraud_model,
    vqe_portfolio,
)
from quantum.qiskit.kernels import (
    circuit_depth,
    export_openqasm3,
    qaoa_circuit,
    qaoa_currency_basket as qaoa_qiskit,
    simulate,
    two_qubit_gate_count,
    variational_fraud_classifier,
)


def test_qrng_produces_bytes() -> None:
    bits = qrng_bits(128)
    assert len(bits) == 32  # 128 bits = 32 hex chars


def test_qrng_unique() -> None:
    a = qrng_bits(128)
    b = qrng_bits(128)
    assert a != b


def test_kyber_seed_size() -> None:
    assert len(seed_kyber()) == 32


def test_dilithium_seed_size() -> None:
    assert len(seed_dilithium()) == 64


def test_qaoa_currency_basket() -> None:
    basket = qaoa_currency_basket(
        expected_returns=[0.05, 0.08, 0.03, 0.06],
        covariance=[[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    assert len(basket) == 4
    assert sum(basket) > 0


def test_fraud_model_trains() -> None:
    model = train_fraud_model([
        ([0.1, 0.2, 0.3], 0),
        ([0.5, 0.6, 0.7], 1),
    ])
    assert len(model.weights) == 3


def test_vqe_optimization() -> None:
    weights = vqe_portfolio([0.25, 0.25, 0.25, 0.25], [0.05, 0.08, 0.03, 0.06])
    assert abs(sum(weights) - 1.0) < 1e-3
    assert all(w >= 0 for w in weights)


@pytest.mark.quantum_hardware  # slow, opt-in
def test_qiskit_circuit_budgets() -> None:
    qc = qaoa_circuit(4, [0.05, 0.08, 0.03, 0.06], [[0.01] * 4] * 4, p=2)
    assert circuit_depth(qc) <= 200
    assert two_qubit_gate_count(qc) <= 600
    counts = simulate(qc, shots=16)
    assert len(counts) > 0
    qasm = export_openqasm3(qc)
    assert "OPENQASM 3" in qasm or "qreg" in qasm


def test_qiskit_qaoa_currency_basket() -> None:
    basket = qaoa_qiskit(
        [0.05, 0.08, 0.03, 0.06],
        [[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    assert len(basket) == 4


def test_variational_fraud_classifier_score() -> None:
    score = variational_fraud_classifier([0.1, 0.2, 0.3], [0.4, 0.5, 0.6])
    assert 0.0 <= score <= 1.0


@pytest.mark.benchmark
def test_qrng_throughput() -> None:
    start = time.time()
    for _ in range(100):
        qrng_bits(64)
    elapsed = time.time() - start
    assert elapsed < 10.0  # 100 calls < 10s


def _dummy() -> dict[str, Any]:
    return {}
