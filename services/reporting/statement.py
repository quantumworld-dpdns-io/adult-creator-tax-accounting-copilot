"""Reporting service (Python + DuckDB)."""

from __future__ import annotations

import os
from typing import Any

try:
    import duckdb
except ImportError:
    duckdb = None  # type: ignore


def generate_monthly_statement(creator_id: str, year: int, month: int) -> dict[str, Any]:
    """Generate a monthly statement for a creator using DuckDB."""
    if duckdb is None:
        return {"creator_id": creator_id, "year": year, "month": month, "stub": True}
    con = duckdb.connect(":memory:")
    con.execute(
        """
        CREATE TABLE payouts AS
        SELECT * FROM read_parquet('s3://copilot-data/payouts/*.parquet', hive_partitioning=true)
        """
    )
    result = con.execute(
        """
        SELECT platform, SUM(gross) AS gross, SUM(fees) AS fees, SUM(net) AS net
        FROM payouts
        WHERE creator_id = ? AND year = ? AND month = ?
        GROUP BY platform
        """,
        [creator_id, year, month],
    ).fetchall()
    return {
        "creator_id": creator_id,
        "year": year,
        "month": month,
        "rows": [{"platform": r[0], "gross": r[1], "fees": r[2], "net": r[3]} for r in result],
    }


if __name__ == "__main__":
    print(generate_monthly_statement("alice", 2026, 1))
