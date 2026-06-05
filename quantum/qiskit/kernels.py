"""Qiskit quantum kernels for the Adult Creator Tax Copilot."""

from __future__ import annotations

import os
from typing import Sequence

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel
except ImportError:  # pragma: no cover
    QuantumCircuit = None  # type: ignore[assignment]
    Statevector = None  # type: ignore[assignment]
    AerSimulator = None  # type: ignore[assignment]
    NoiseModel = None  # type: ignore[assignment]


def qaoa_circuit(
    n: int,
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    p: int = 2,
) -> "QuantumCircuit":
    """Build a QAOA circuit for currency-basket selection."""
    if QuantumCircuit is None:
        raise RuntimeError("qiskit is not installed")
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    for layer in range(p):
        gamma = 0.1 * (layer + 1)
        for i in range(n):
            for j in range(n):
                if i < j:
                    qc.cx(i, j)
                    qc.rz(2 * gamma * covariance[i][j], j)
                    qc.cx(i, j)
        for i in range(n):
            qc.rx(2 * gamma * expected_returns[i], i)
        beta = 0.2 * (layer + 1)
        for i in range(n):
            qc.rz(2 * beta, i)
    qc.measure_all()
    return qc


def simulate(qc: "QuantumCircuit", shots: int = 1024) -> dict[str, int]:
    """Simulate the circuit with the Aer backend."""
    if AerSimulator is None:
        raise RuntimeError("qiskit-aer is not installed")
    backend = AerSimulator()
    job = backend.run(qc, shots=shots)
    return job.result().get_counts()


def circuit_depth(qc: "QuantumCircuit") -> int:
    return qc.depth()


def two_qubit_gate_count(qc: "QuantumCircuit") -> int:
    return sum(1 for instr in qc.data if instr.operation.num_qubits == 2)


def export_openqasm3(qc: "QuantumCircuit") -> str:
    return qc.qasm3() if hasattr(qc, "qasm3") else qc.qasm()


# ────────────────────────────────────────────────────────────────────
# High-level helpers
# ────────────────────────────────────────────────────────────────────

def qaoa_currency_basket(
    expected_returns: Sequence[float],
    covariance: Sequence[Sequence[float]],
    p: int = 2,
) -> list[int]:
    """Return the most-likely basket from QAOA."""
    if QuantumCircuit is None:
        # classical proxy
        n = len(expected_returns)
        scores = [r / (sum(c) + 1e-9) for r, c in zip(expected_returns, covariance)]
        ranked = sorted(range(n), key=lambda i: scores[i], reverse=True)
        basket = [0] * n
        for i in ranked[: max(1, n // 2)]:
            basket[i] = 1
        return basket
    n = len(expected_returns)
    qc = qaoa_circuit(n, expected_returns, covariance, p)
    counts = simulate(qc, shots=512)
    best = max(counts.items(), key=lambda kv: kv[1])[0]
    return [int(b) for b in best[::-1]][:n]


def variational_fraud_classifier(features: Sequence[float], weights: Sequence[float]) -> float:
    """Tiny variational classifier (classical surrogate)."""
    return 1.0 / (1.0 + pow(2.71828, -sum(w * x for w, x in zip(weights, features))))


if __name__ == "__main__":
    basket = qaoa_currency_basket(
        expected_returns=[0.05, 0.08, 0.03, 0.06],
        covariance=[[0.01, 0.002, 0.001, 0.001]] * 4,
    )
    print("QAOA basket:", basket)
    print("Variational fraud score:", variational_fraud_classifier([0.1, 0.2, 0.3], [0.4, 0.5, 0.6]))
