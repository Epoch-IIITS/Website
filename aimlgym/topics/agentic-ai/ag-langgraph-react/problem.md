# AG-08 · A ReAct Agent in LangGraph

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** langchain-core, langgraph

**Builds on:** AG-07 LangGraph Basics: State, Nodes and Edges

Read the lesson first: [article.md](article.md)

## Task

1. `build_agent(model, tools)` returns the compiled graph from the lesson: nodes `"agent"` (calls
   `model.bind_tools(tools)` on the messages) and `"tools"` (`ToolNode(tools)`), `tools_condition`
   routing, and an `InMemorySaver` checkpointer.
2. `run_agent(app, question, thread_id, max_steps=8)` invokes the graph with a `HumanMessage(question)`,
   `thread_id` and `recursion_limit=max_steps`, and returns the content of the last message. If the
   limit is reached (`GraphRecursionError`), return `"Stopped: step limit reached"`.

## Hints

<details><summary>Hint 1</summary>

Bind the tools once outside the node function: `bound = model.bind_tools(tools)`.

</details>

<details><summary>Hint 2</summary>

Edges: START → agent, conditional edges with tools_condition, tools → agent; compile with `checkpointer=InMemorySaver()`.

</details>

<details><summary>Hint 3</summary>

The config is `{"configurable": {"thread_id": thread_id}, "recursion_limit": max_steps}`; read `result["messages"][-1].content`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_answers_after_tools` | Route with tools_condition and add an edge from tools back to agent. |
| `test_step_limit` | Pass recursion_limit=max_steps and catch GraphRecursionError. |
| `test_threads_are_separate` | Compile with InMemorySaver() and pass the thread_id in the config. |
| `test_tool_error_reaches_model` | Use ToolNode(tools), which reports tool errors as messages. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The agent node asks the model for its next move; `tools_condition` sends tool calls to the ToolNode
and plain answers to the end, and the tool results flow back to the model. The checkpointer stores
each thread's messages, and the recursion limit turns a runaway loop into a clear message.

## References

- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
- [Persistence (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/persistence) — LangChain (`S137`)
