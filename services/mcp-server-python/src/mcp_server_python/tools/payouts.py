"""Payout aggregation tools."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any


async def get_payouts(creator_id: str, start: str, end: str) -> dict[str, Any]:
    """Fetch aggregated payouts for a creator over a date range.

    In production this queries the ledger service over gRPC. For the scaffold
    we return a deterministic stub.
    """
    ledger_url = os.environ.get("LEDGER_GRPC_URL", "localhost:50051")
    return {
        "creator_id": creator_id,
        "start": start,
        "end": end,
        "ledger_endpoint": ledger_url,
        "currency": "USD",
        "gross": 12345.67,
        "fees": 234.56,
        "net": 12111.11,
        "platforms": [
            {"platform": "OnlyFans", "gross": 8000.00, "fees": 160.00, "net": 7840.00},
            {"platform": "Fansly", "gross": 2500.00, "fees": 50.00, "net": 2450.00},
            {"platform": "Stripe", "gross": 1845.67, "fees": 24.56, "net": 1821.11},
        ],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
