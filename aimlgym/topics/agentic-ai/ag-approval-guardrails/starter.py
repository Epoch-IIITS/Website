from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class GuardState(TypedDict):
    action: dict
    outcome: str


def build_guarded_graph(tools, sensitive):
    # TODO
    pass


def run_with_approval(app, action, thread_id, decide):
    # TODO
    pass
