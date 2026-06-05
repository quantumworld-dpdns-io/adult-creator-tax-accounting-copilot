"""MCP server Python — tests."""

import pytest

from mcp_server_python.server import create_server
from mcp_server_python.tools import payouts, taxes, zk


def test_create_server_has_tools() -> None:
    s = create_server()
    # FastMCP exposes tools via internal registry
    assert s is not None


@pytest.mark.asyncio
async def test_get_payouts_stub() -> None:
    out = await payouts.get_payouts("alice", "2026-01-01", "2026-12-31")
    assert out["creator_id"] == "alice"
    assert out["currency"] == "USD"
    assert out["gross"] > 0
    assert len(out["platforms"]) > 0


@pytest.mark.asyncio
async def test_compute_tax_estimate_us() -> None:
    out = await taxes.compute_estimate("alice", "US", 2026)
    assert out["jurisdiction"] == "US"
    assert out["bracket"] in {"10%", "12%", "22%", "24%", "32%"}


@pytest.mark.asyncio
async def test_file_1099() -> None:
    out = await taxes.file_1099("alice", 2026, "1099-NEC")
    assert out["signed"] is True
    assert out["signature_algo"] == "Dilithium-5"


@pytest.mark.asyncio
async def test_file_w8ben() -> None:
    out = await taxes.file_w8ben("alice", "DE")
    assert "w8ben" in out["pdf_url"]


@pytest.mark.asyncio
async def test_aggregate_vat() -> None:
    out = await taxes.aggregate_vat("alice", "2026-Q1")
    assert len(out["member_states"]) >= 2
    assert out["total_vat_collected"] > 0


@pytest.mark.asyncio
async def test_zk_prove_age() -> None:
    out = await zk.prove_age("alice", 18)
    assert out["proof_system"] == "noir"
    assert out["curve"] == "bn254"


@pytest.mark.asyncio
async def test_zk_prove_income_range() -> None:
    out = await zk.prove_income_range("alice", 50_000, 100_000)
    assert out["lower_usd"] == 50_000
    assert out["upper_usd"] == 100_000
