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
    # TODO
    pass
