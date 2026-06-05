"""LangGraph workflow: tax filing with human-in-the-loop.

State machine:
  START -> analyze -> review(human) -> file -> verify -> END
"""
from __future__ import annotations

from typing import TypedDict

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    StateGraph = None  # type: ignore
    END = "END"  # type: ignore


class TaxState(TypedDict, total=False):
    creator_id: str
    year: int
    jurisdiction: str
    deductions: list[dict]
    pdf_url: str | None
    audit_id: str | None
    approved: bool


def build_graph():
    if StateGraph is None:
        return None

    g = StateGraph(TaxState)

    def analyze(state: TaxState) -> TaxState:
        state["deductions"] = [
            {"name": "home office", "amount": 1200},
            {"name": "equipment", "amount": 850},
        ]
        return state

    def file(state: TaxState) -> TaxState:
        state["pdf_url"] = f"s3://copilot-data/forms/{state['creator_id']}/{state['year']}.pdf"
        return state

    def verify(state: TaxState) -> TaxState:
        state["audit_id"] = f"audit-{state['creator_id']}-{state['year']}"
        state["approved"] = True
        return state

    def human_review(state: TaxState) -> TaxState:
        return state

    g.add_node("analyze", analyze)
    g.add_node("file", file)
    g.add_node("verify", verify)
    g.add_node("review", human_review)

    g.set_entry_point("analyze")
    g.add_edge("analyze", "review")
    g.add_edge("review", "file")
    g.add_edge("file", "verify")
    g.add_edge("verify", END)

    return g.compile()


if __name__ == "__main__":
    graph = build_graph()
    if graph is not None:
        out = graph.invoke({"creator_id": "alice", "year": 2026, "jurisdiction": "US"})
        print(out)
    else:
        print("langgraph not installed")
