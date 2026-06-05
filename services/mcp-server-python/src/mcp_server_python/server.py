"""Core MCP server factory + run loop."""

from __future__ import annotations

import os
from typing import Any

from fastmcp import FastMCP, tool
from pydantic import BaseModel, Field

from mcp_server_python.tools import payouts, taxes, zk

__all__ = ["create_server", "run"]


class PayoutsQuery(BaseModel):
    creator_id: str = Field(..., description="The creator's unique identifier")
    start: str = Field(..., description="ISO 8601 start date")
    end: str = Field(..., description="ISO 8601 end date")


class TaxEstimateQuery(BaseModel):
    creator_id: str
    jurisdiction: str = Field(..., description="ISO 3166-1 alpha-2 or 'US'/'EU'/'UK'")
    year: int


class W8BENQuery(BaseModel):
    creator_id: str
    treaty_country: str = Field(..., description="ISO 3166-1 alpha-2 treaty country")


class VATAggregateQuery(BaseModel):
    creator_id: str
    period: str = Field(..., description="YYYY-Q or YYYY-MM")


class ZKAgeProofQuery(BaseModel):
    creator_id: str
    min_age: int = 18


class ZKIncomeRangeQuery(BaseModel):
    creator_id: str
    lower_usd: int
    upper_usd: int


def create_server() -> FastMCP:
    """Build the FastMCP server with all tools registered."""
    server = FastMCP(
        name="adult-creator-tax-copilot",
        version=__version__ if "__version__" in globals() else "0.1.0",
        instructions=(
            "Use these tools to assist adult content creators with tax "
            "compliance, payout aggregation, and ZK privacy proofs."
        ),
    )

    @server.tool(
        name="get_payouts",
        description="Fetch aggregated payouts for a creator over a date range.",
    )
    async def get_payouts(query: PayoutsQuery) -> dict[str, Any]:
        return await payouts.get_payouts(**query.model_dump())

    @server.tool(
        name="compute_tax_estimate",
        description="Compute an estimated tax liability for a given jurisdiction and year.",
    )
    async def compute_tax_estimate(query: TaxEstimateQuery) -> dict[str, Any]:
        return await taxes.compute_estimate(**query.model_dump())

    @server.tool(
        name="file_1099",
        description="Generate a 1099 tax form (1099-NEC / 1099-MISC / 1099-K) for a creator.",
    )
    async def file_1099(creator_id: str, year: int, form: str = "1099-NEC") -> dict[str, Any]:
        return await taxes.file_1099(creator_id=creator_id, year=year, form=form)

    @server.tool(
        name="file_w8ben",
        description="Generate a W-8BEN form for treaty-based withholding.",
    )
    async def file_w8ben(query: W8BENQuery) -> dict[str, Any]:
        return await taxes.file_w8ben(**query.model_dump())

    @server.tool(
        name="aggregate_vat",
        description="Aggregate EU VAT MOSS obligations for a period.",
    )
    async def aggregate_vat(query: VATAggregateQuery) -> dict[str, Any]:
        return await taxes.aggregate_vat(**query.model_dump())

    @server.tool(
        name="verify_age_zk",
        description="Issue a zero-knowledge proof that a creator is at least min_age.",
    )
    async def verify_age_zk(query: ZKAgeProofQuery) -> dict[str, Any]:
        return await zk.prove_age(**query.model_dump())

    @server.tool(
        name="prove_income_range",
        description="Issue a zero-knowledge proof that creator's income is in [lower, upper] USD.",
    )
    async def prove_income_range(query: ZKIncomeRangeQuery) -> dict[str, Any]:
        return await zk.prove_income_range(**query.model_dump())

    return server


async def run(server: FastMCP) -> None:
    """Run the MCP server using the transport from MCP_TRANSPORT env var."""
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    await server.run_async(transport=transport)
