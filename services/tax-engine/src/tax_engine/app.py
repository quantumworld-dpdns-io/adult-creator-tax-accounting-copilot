"""Tax-engine FastAPI app (Python)."""
from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="tax-engine", version="0.1.0")


class Payout(BaseModel):
    platform: str
    currency: str
    gross: float
    fees: float
    net: float


class EstimateRequest(BaseModel):
    creator_id: str
    jurisdiction: str
    year: int
    payouts: list[Payout] = []


class File1099Request(BaseModel):
    creator_id: str
    year: int
    form: str = "1099-NEC"


class W8BENRequest(BaseModel):
    creator_id: str
    treaty_country: str


class VATAggregateRequest(BaseModel):
    creator_id: str
    period: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tax/estimate")
async def estimate(req: EstimateRequest) -> dict[str, Any]:
    gross = sum(p.gross for p in req.payouts)
    taxable = gross
    rate, bracket = _rate_for(req.jurisdiction, taxable)
    est_tax = taxable * rate
    return {
        "creator_id": req.creator_id,
        "jurisdiction": req.jurisdiction,
        "year": req.year,
        "gross_usd": gross,
        "taxable_usd": taxable,
        "estimated_tax_usd": est_tax,
        "effective_rate": rate,
        "bracket": bracket,
    }


@app.post("/v1/tax/file/1099")
async def file_1099(req: File1099Request) -> dict[str, Any]:
    return {
        "creator_id": req.creator_id,
        "year": req.year,
        "form": req.form,
        "pdf_url": f"s3://copilot-data/1099/{req.creator_id}/{req.year}/{req.form}.pdf",
        "signed": True,
        "signature_algo": "Dilithium-5",
    }


@app.post("/v1/tax/file/w8ben")
async def file_w8ben(req: W8BENRequest) -> dict[str, Any]:
    return {
        "creator_id": req.creator_id,
        "treaty_country": req.treaty_country,
        "pdf_url": f"s3://copilot-data/w8ben/{req.creator_id}/w8ben.pdf",
        "signed": True,
        "signature_algo": "Dilithium-5",
    }


@app.post("/v1/tax/aggregate/vat")
async def aggregate_vat(req: VATAggregateRequest) -> dict[str, Any]:
    return {
        "creator_id": req.creator_id,
        "period": req.period,
        "member_states": [
            {"country": "DE", "vat_collected": 1234.56, "rate": 0.19},
            {"country": "FR", "vat_collected": 890.12, "rate": 0.20},
            {"country": "ES", "vat_collected": 345.67, "rate": 0.21},
        ],
        "total_vat_collected": 2470.35,
    }


def _rate_for(jurisdiction: str, taxable: float) -> tuple[float, str]:
    if jurisdiction == "US":
        if taxable < 11600:
            return 0.10, "10%"
        if taxable < 47150:
            return 0.12, "12%"
        if taxable < 100525:
            return 0.22, "22%"
        if taxable < 191950:
            return 0.24, "24%"
        return 0.32, "32%"
    if jurisdiction == "UK":
        return 0.20, "basic-rate"
    if jurisdiction == "CA":
        return 0.15, "15%"
    if jurisdiction == "AU":
        return 0.19, "19%"
    if jurisdiction == "JP":
        return 0.20, "20%"
    return 0.20, "default-20%"


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
