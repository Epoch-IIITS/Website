# LangGraph Basics: State, Nodes and Edges

## Learning outcomes

After this lesson you can:

- Describe a workflow as a StateGraph with a typed state
- Write nodes that return partial state updates and use a reducer to accumulate lists
- Route between nodes with conditional edges, including loops

## Intuition
Your agent loops so far were `while` loops with `if`s inside. As workflows grow — retries,
approvals, several workers — that control flow becomes hard to read and test. LangGraph makes it
explicit: a **state** dict, **nodes** that read the state and return updates, and **edges** that
decide which node runs next.

## Precise explanation
```python
import operator
from typing import Annotated, TypedDict
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]      # reducer: updates are appended, not replaced

def strip(state):
    return {"text": state["text"].strip(), "steps": ["strip"]}    # return only what changes

graph = StateGraph(State)
graph.add_node("strip", strip)
graph.add_edge(START, "strip")
graph.add_conditional_edges("check", route)        # route(state) returns a node name or END
app = graph.compile()
app.invoke({"text": "  Hello ", "steps": []})      # the final state
```

* A node returns a **partial update**. Keys without a reducer are overwritten; a key annotated with a
  reducer such as `operator.add` combines the old and new values. (`operator.add(a, b)` is `a + b` as a
  function, from the standard-library `operator` module; for lists it concatenates.)
* `add_conditional_edges(node, route)` calls `route(state)` after the node and follows the returned
  name, which may point back to an earlier node to form a loop.
* `compile()` checks the graph (unknown nodes, unreachable nodes) and returns a runnable with
  `invoke`. `app.get_graph().nodes` lists the nodes; LangGraph can also draw the graph.
* A loop that never ends stops with `GraphRecursionError` after `recursion_limit` steps (default 25).

## Worked example
For "  The Quick Brown Fox Jumps  " and `max_words=3`: strip, lower, check (5 words, too long),
shorten, check (4), shorten, check (3, done). The final text is "the quick brown" and `steps` is
["strip", "lower", "shorten", "shorten"].

## Common mistakes
* Mutating `state` inside a node instead of returning an update.
* Forgetting the reducer, so each node's list replaces the previous one.
* A routing function that returns a name that is not a node.

## Why this matters
The ReAct agent, orchestrator and guardrail steps that follow are LangGraph graphs; reading and
drawing them is how you debug agents.

## References

- [Graph API (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/graph-api) — LangChain (`S136`)
- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
