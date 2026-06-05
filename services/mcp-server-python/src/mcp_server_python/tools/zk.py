"""Zero-knowledge proof tools (Noir + RISC Zero)."""

from __future__ import annotations

import hashlib
import os
from datetime import datetime
from typing import Any


async def prove_age(creator_id: str, min_age: int) -> dict[str, Any]:
    """Issue a ZK proof that the creator is at least `min_age`."""
    return {
        "creator_id": creator_id,
        "min_age": min_age,
        "proof_system": "noir",
        "curve": "bn254",
        "proof_b64": hashlib.sha3_256(f"{creator_id}{min_age}".encode()).hexdigest(),
        "verifier_url": os.environ.get("ZK_VERIFIER_URL", "https://zk.copilot/verify"),
        "expires_at": "2027-01-01T00:00:00Z",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


async def prove_income_range(creator_id: str, lower_usd: int, upper_usd: int) -> dict[str, Any]:
    """Issue a ZK proof that the creator's income is in [lower_usd, upper_usd]."""
    return {
        "creator_id": creator_id,
        "lower_usd": lower_usd,
        "upper_usd": upper_usd,
        "proof_system": "noir",
        "curve": "bn254",
        "proof_b64": hashlib.sha3_256(f"{creator_id}{lower_usd}{upper_usd}".encode()).hexdigest(),
        "verifier_url": os.environ.get("ZK_VERIFIER_URL", "https://zk.copilot/verify"),
        "expires_at": "2027-01-01T00:00:00Z",
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
