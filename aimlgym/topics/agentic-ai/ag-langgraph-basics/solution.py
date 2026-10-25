r"""Reference solution for AG-07 LangGraph Basics: State, Nodes and Edges.

Each node returns only the keys it changes; the `operator.add` reducer appends step names. The
conditional edge after `check` either loops through `shorten` or ends, so the loop's condition lives
in one routing function rather than inside the nodes.
"""
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class CleanerState(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]


def build_cleaner(max_words):
    if max_words < 1:
        raise ValueError("max_words must be at least 1")

    def route(state):
        return "shorten" if len(state["text"].split()) > max_words else END

    graph = StateGraph(CleanerState)
    graph.add_node("strip", lambda s: {"text": s["text"].strip(), "steps": ["strip"]})
    graph.add_node("lower", lambda s: {"text": s["text"].lower(), "steps": ["lower"]})
    graph.add_node("check", lambda s: {})
    graph.add_node("shorten", lambda s: {"text": " ".join(s["text"].split()[:-1]), "steps": ["shorten"]})
    graph.add_edge(START, "strip")
    graph.add_edge("strip", "lower")
    graph.add_edge("lower", "check")
    graph.add_conditional_edges("check", route)
    graph.add_edge("shorten", "check")
    return graph.compile()
