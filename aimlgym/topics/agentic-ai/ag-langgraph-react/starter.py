from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def build_agent(model, tools):
    # TODO
    pass


def run_agent(app, question, thread_id, max_steps=8):
    # TODO
    pass
