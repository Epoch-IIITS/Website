r"""Reference solution for AG-16 Orchestrator and Workers in LangGraph.

The orchestrator decides the work; `Send` starts one worker per section with only that section; the
reducer collects the indexed results; the synthesiser restores the order and writes one report.
"""
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReportState(TypedDict):
    document: str
    sections: list
    results: Annotated[list, operator.add]
    report: str


def build_report_graph(worker_fn):
    def orchestrator(state):
        return {"sections": [s.strip() for s in state["document"].split("\n\n") if s.strip()]}

    def assign(state):
        return [Send("worker", {"index": i, "section": s}) for i, s in enumerate(state["sections"])]

    def worker(payload):
        return {"results": [(payload["index"], worker_fn(payload["section"]))]}

    def synthesise(state):
        ordered = sorted(state["results"])
        return {"report": " | ".join(f"{i + 1}: {summary}" for i, summary in ordered)}

    graph = StateGraph(ReportState)
    graph.add_node("orchestrator", orchestrator)
    graph.add_node("worker", worker)
    graph.add_node("synthesise", synthesise)
    graph.add_edge(START, "orchestrator")
    graph.add_conditional_edges("orchestrator", assign, ["worker"])
    graph.add_edge("worker", "synthesise")
    graph.add_edge("synthesise", END)
    return graph.compile()
