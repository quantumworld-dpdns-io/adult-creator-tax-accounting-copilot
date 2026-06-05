"""Tax-engine tests."""
from fastapi.testclient import TestClient

from tax_engine.app import app

client = TestClient(app)


def test_healthz() -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_estimate_us_low_bracket() -> None:
    r = client.post(
        "/v1/tax/estimate",
        json={
            "creator_id": "alice",
            "jurisdiction": "US",
            "year": 2026,
            "payouts": [{"platform": "OnlyFans", "currency": "USD", "gross": 10000.0, "fees": 200.0, "net": 9800.0}],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["bracket"] == "12%"
    assert body["effective_rate"] == 0.12
    assert body["estimated_tax_usd"] == 10000.0 * 0.12


def test_estimate_uk_basic_rate() -> None:
    r = client.post(
        "/v1/tax/estimate",
        json={"creator_id": "bob", "jurisdiction": "UK", "year": 2026, "payouts": []},
    )
    assert r.status_code == 200
    assert r.json()["bracket"] == "basic-rate"


def test_file_1099() -> None:
    r = client.post("/v1/tax/file/1099", json={"creator_id": "alice", "year": 2026, "form": "1099-NEC"})
    assert r.status_code == 200
    body = r.json()
    assert body["signed"] is True
    assert body["signature_algo"] == "Dilithium-5"


def test_file_w8ben() -> None:
    r = client.post("/v1/tax/file/w8ben", json={"creator_id": "alice", "treaty_country": "DE"})
    assert r.status_code == 200


def test_aggregate_vat() -> None:
    r = client.post("/v1/tax/aggregate/vat", json={"creator_id": "alice", "period": "2026-Q1"})
    assert r.status_code == 200
    body = r.json()
    assert body["total_vat_collected"] > 0
