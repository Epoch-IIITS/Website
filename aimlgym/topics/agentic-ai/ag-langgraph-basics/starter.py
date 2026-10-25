import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class CleanerState(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]


def build_cleaner(max_words):
    # TODO
    pass
