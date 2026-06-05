# Quantum Gallery

This document is the human-readable index of every quantum circuit in the
repository.

## Kernels (CUDA-Q)

| Kernel | Purpose | Location |
| ------ | ------- | -------- |
| `qrng_bits` | Quantum RNG via Hadamard + measure | `quantum/cudaq/kernels.py` |
| `qaoa_currency_basket` | Currency-basket selection | `quantum/cudaq/kernels.py` |
| `train_fraud_model` | Variational fraud classifier | `quantum/cudaq/kernels.py` |
| `vqe_portfolio` | Portfolio optimization (VQE) | `quantum/cudaq/kernels.py` |

## Kernels (Qiskit)

| Kernel | Purpose | Location |
| ------ | ------- | -------- |
| `qaoa_circuit` | Build QAOA circuit | `quantum/qiskit/kernels.py` |
| `simulate` | Aer simulator wrapper | `quantum/qiskit/kernels.py` |
| `qaoa_currency_basket` | Top basket from QAOA | `quantum/qiskit/kernels.py` |
| `variational_fraud_classifier` | QML classifier | `quantum/qiskit/kernels.py` |

## QRNG Service

| Endpoint | Purpose |
| -------- | ------- |
| `GET /v1/qrng/bits?provider=anu&bits=256` | Fetch quantum-random bits |

## Backends

| Backend | Type | Cost | Use case |
| ------- | ---- | ---- | -------- |
| `sim` | Qiskit Aer simulator | Free | Dev / CI |
| `anu` | ANU QRNG | Free / rate-limited | Production entropy |
| `ibm` | IBM Quantum | Free tier / paid | Real hardware validation |
| `cudaq:cpu` | CUDA-Q CPU | Free | Heavy QAOA / VQE |
| `cudaq:gpu` | CUDA-Q cuQuantum | GPU cost | Largest circuits |
