# A ReAct Agent in LangGraph

## Learning outcomes

After this lesson you can:

- Build an agent graph from a model node, a ToolNode and tools_condition
- Limit the number of steps with recursion_limit
- Keep conversations per thread with an InMemorySaver checkpointer

## Intuition
The ReAct loop of AG-06 alternates thinking and acting: the model decides on a tool, the
tool runs, the model reads the result, and so on until it answers. In LangGraph that loop is two nodes
and a conditional edge — plus, for free, a step limit and saved conversation history.

## Precise explanation
```python
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

bound = model.bind_tools(tools)
def agent(state):
    return {"messages": [bound.invoke(state["messages"])]}

graph = StateGraph(MessagesState)                    # {"messages": [...]} with an add_messages reducer
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))            # runs the tool calls of the last AI message
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)   # "tools" if there are tool calls, else END
graph.add_edge("tools", "agent")
app = graph.compile(checkpointer=InMemorySaver())
app.invoke({"messages": [HumanMessage("...")]}, {"configurable": {"thread_id": "alice"}, "recursion_limit": 8})
```

* `MessagesState`'s reducer appends new messages, so the history grows: human, ai (tool calls), tool,
  ai, …
* `ToolNode` executes the calls and returns `ToolMessage`s, turning tool errors into messages.
* `recursion_limit` caps the total number of node executions; reaching it raises
  `GraphRecursionError` — the budget of AG-05.
* With a **checkpointer**, each `thread_id` keeps its own state between calls; the next `invoke` on
  the same thread continues the conversation. `app.get_state(config).values` shows it.

## Worked example
"What is 17 × 23 + 5?" The model calls `multiply(17, 23)`, reads 391, calls `add(391, 5)`, reads 396
and answers "396". The thread then holds six messages: human, ai, tool, ai, tool, ai.

## Common mistakes
* Forgetting the edge from tools back to the agent, so the model never sees the result.
* No step limit, so a confused model loops until the default limit (or your bill) stops it.
* Reusing one thread id for different users.

## Why this matters
This graph is the core of most tool-using assistants; the study-planner project idea after this step
adds real tools to it.

## References

- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
- [Persistence (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/persistence) — LangChain (`S137`)
