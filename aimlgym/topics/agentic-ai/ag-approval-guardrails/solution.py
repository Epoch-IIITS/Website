r"""Reference solution for AG-18 Guardrails with Human Approval.

The guard classifies every action. For sensitive ones `interrupt` saves the state and returns control
to the caller with the action to review; resuming on the same thread feeds the decision back into the
guard. Only an exact "approve" lets the action reach the execute node, where the side effect happens.
"""
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class GuardState(TypedDict):
    action: dict
    outcome: str


def build_guarded_graph(tools, sensitive):
    def guard(state):
        name = state["action"]["tool"]
        if name not in tools:
            return {"outcome": "blocked"}
        if name in sensitive:
            decision = interrupt({"action": state["action"]})
            if decision != "approve":
                return {"outcome": "rejected"}
        return {}

    def execute(state):
        action = state["action"]
        result = tools[action["tool"]](**action.get("args", {}))
        return {"outcome": f"approved: {result}"}

    def route(state):
        return END if state["outcome"] in ("blocked", "rejected") else "execute"

    graph = StateGraph(GuardState)
    graph.add_node("guard", guard)
    graph.add_node("execute", execute)
    graph.add_edge(START, "guard")
    graph.add_conditional_edges("guard", route)
    graph.add_edge("execute", END)
    return graph.compile(checkpointer=InMemorySaver())


def run_with_approval(app, action, thread_id, decide):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"action": action, "outcome": ""}, config)
    if "__interrupt__" in result:
        decision = decide(result["__interrupt__"][0].value)
        result = app.invoke(Command(resume=decision), config)
    return result["outcome"]
