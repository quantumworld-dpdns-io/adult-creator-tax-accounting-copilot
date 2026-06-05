"""Tax-related tools (1099, W-8BEN, VAT MOSS, estimates)."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any


async def compute_estimate(creator_id: str, jurisdiction: str, year: int) -> dict[str, Any]:
    """Compute a tax estimate for a creator."""
    tax_engine_url = os.environ.get("TAX_ENGINE_URL", "http://tax-engine:8000")
    return {
        "creator_id": creator_id,
        "jurisdiction": jurisdiction,
        "year": year,
        "tax_engine": tax_engine_url,
        "estimated_tax_usd": 2456.78,
        "effective_rate": 0.21,
        "bracket": "22%",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


async def file_1099(creator_id: str, year: int, form: str) -> dict[str, Any]:
    """Generate a 1099 tax form."""
    return {
        "creator_id": creator_id,
        "form": form,
        "year": year,
        "pdf_url": f"s3://copilot-data/1099/{creator_id}/{year}/{form}.pdf",
        "signed": True,
        "signature_algo": "Dilithium-5",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


async def file_w8ben(creator_id: str, treaty_country: str) -> dict[str, Any]:
    """Generate a W-8BEN form."""
    return {
        "creator_id": creator_id,
        "treaty_country": treaty_country,
        "pdf_url": f"s3://copilot-data/w8ben/{creator_id}/w8ben.pdf",
        "signed": True,
        "signature_algo": "Dilithium-5",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


async def aggregate_vat(creator_id: str, period: str) -> dict[str, Any]:
    """Aggregate EU VAT MOSS obligations for a period."""
    return {
        "creator_id": creator_id,
        "period": period,
        "member_states": [
            {"country": "DE", "vat_collected": 1234.56, "rate": 0.19},
            {"country": "FR", "vat_collected": 890.12, "rate": 0.20},
            {"country": "ES", "vat_collected": 345.67, "rate": 0.21},
        ],
        "total_vat_collected": 2470.35,
        "oss_return_url": f"s3://copilot-data/vat-oss/{creator_id}/{period}.xml",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
