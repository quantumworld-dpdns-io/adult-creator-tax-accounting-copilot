"""Tests for the QRNG API."""

import os
import sys
from unittest.mock import patch

import pytest

# Skip if fastapi is missing
fastapi = pytest.importorskip("fastapi")

from fastapi.testclient import TestClient  # noqa: E402

# Make the quantum package importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from quantum.qrng.api import app  # noqa: E402

client = TestClient(app)


def test_healthz() -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_qrng_sim_64() -> None:
    r = client.get("/v1/qrng/bits?provider=sim&bits=64")
    assert r.status_code == 200
    body = r.json()
    assert body["bits"] == 64
    assert len(body["hex"]) == 16


def test_qrng_sim_128() -> None:
    r = client.get("/v1/qrng/bits?provider=sim&bits=128")
    assert r.status_code == 200
    body = r.json()
    assert body["bits"] == 128
    assert len(body["hex"]) == 32


def test_qrng_invalid_provider() -> None:
    r = client.get("/v1/qrng/bits?provider=bogus&bits=128")
    assert r.status_code == 422


def test_qrng_too_many_bits() -> None:
    r = client.get("/v1/qrng/bits?provider=sim&bits=99999")
    assert r.status_code == 422


def test_qrng_too_few_bits() -> None:
    r = client.get("/v1/qrng/bits?provider=sim&bits=4")
    assert r.status_code == 422


def test_qrng_unique() -> None:
    a = client.get("/v1/qrng/bits?provider=sim&bits=128").json()["hex"]
    b = client.get("/v1/qrng/bits?provider=sim&bits=128").json()["hex"]
    assert a != b
