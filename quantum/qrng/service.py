"""Quantum Random Number Generation service."""

from __future__ import annotations

import hashlib
import os
import secrets
from typing import Literal

Provider = Literal["anu", "ibm", "sim"]


def fetch_anu(bits: int = 256) -> bytes:
    """Fetch bits from the ANU QRNG API.

    Falls back to a CSPRNG on failure. Real implementation uses HTTPS.
    """
    try:
        import httpx

        url = f"https://qrng.anu.edu.au/API/jsonI.php?length={bits // 8}&type=hex16"
        r = httpx.get(url, timeout=5.0)
        r.raise_for_status()
        data = r.json()
        return bytes.fromhex("".join(data["data"]))
    except Exception:  # pragma: no cover
        return secrets.token_bytes(bits // 8)


def fetch_ibm(bits: int = 256) -> bytes:
    """Fetch bits from the IBM Quantum back-end via Qiskit Runtime.

    Falls back to the simulator or CSPRNG.
    """
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler

        service = QiskitRuntimeService(channel="ibm_quantum", token=os.environ.get("IBM_QUANTUM_TOKEN"))
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=5)
        sampler = Sampler(backend=backend)
        from qiskit import QuantumCircuit

        n = bits
        qc = QuantumCircuit(n)
        qc.h(range(n))
        qc.measure_all()
        job = sampler.run([qc], shots=1)
        result = job.result()
        counts = result[0].data.meas.get_counts()
        bits_str = list(counts.keys())[0]
        return int(bits_str, 2).to_bytes(n // 8, "big")
    except Exception:  # pragma: no cover
        return secrets.token_bytes(bits // 8)


def fetch_simulator(bits: int = 256) -> bytes:
    """Generate bits using a Qiskit Aer simulator."""
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        n = bits
        qc = QuantumCircuit(n)
        qc.h(range(n))
        qc.measure_all()
        backend = AerSimulator()
        job = backend.run(qc, shots=1)
        counts = job.result().get_counts()
        bits_str = list(counts.keys())[0]
        return int(bits_str, 2).to_bytes(n // 8, "big")
    except Exception:  # pragma: no cover
        return secrets.token_bytes(bits // 8)


def fetch(provider: Provider = "anu", bits: int = 256) -> bytes:
    if provider == "anu":
        raw = fetch_anu(bits)
    elif provider == "ibm":
        raw = fetch_ibm(bits)
    else:
        raw = fetch_simulator(bits)
    # Mix through BLAKE3 for additional whitening.
    return hashlib.blake2b(raw, digest_size=bits // 8).digest()


if __name__ == "__main__":
    print("ANU QRNG:", fetch("anu", 256).hex())
    print("Sim QRNG:", fetch("sim", 256).hex())
