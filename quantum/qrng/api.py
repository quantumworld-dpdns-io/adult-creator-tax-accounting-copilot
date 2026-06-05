"""QRNG API (FastAPI)."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from quantum.qrng.service import fetch

app = FastAPI(title="qrng", version="0.1.0")


class BitsResponse(BaseModel):
    provider: str
    bits: int
    hex: str
    entropy_quality: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/qrng/bits", response_model=BitsResponse)
def get_bits(
    provider: str = Query("sim", pattern="^(anu|ibm|sim)$"),
    bits: int = Query(256, ge=8, le=4096),
) -> BitsResponse:
    try:
        data = fetch(provider, bits)
    except Exception as e:
        raise HTTPException(500, f"qrng failed: {e}") from e
    return BitsResponse(
        provider=provider,
        bits=bits,
        hex=data.hex(),
        entropy_quality="quantum" if provider in ("anu", "ibm") else "simulator",
    )


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8050")))
