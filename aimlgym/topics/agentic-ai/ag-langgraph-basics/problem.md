# AG-07 · LangGraph Basics: State, Nodes and Edges

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** langgraph

**Builds on:** AG-06 ReAct Loop with a Scripted Model, AG-03 Tools and Tool Calling with LangChain

Read the lesson first: [article.md](article.md)

## Task

Write `build_cleaner(max_words)` returning a compiled graph over the state
`{"text": str, "steps": Annotated[list[str], operator.add]}` with nodes:

* `"strip"`: strips surrounding whitespace, step `"strip"`;
* `"lower"`: lowercases, step `"lower"`;
* `"check"`: no change (return `{}`);
* `"shorten"`: removes the last word, step `"shorten"`.

Edges: START → strip → lower → check; after `check`, go to `"shorten"` if the text has more than
`max_words` words, otherwise END; shorten → check. Raise `ValueError` if `max_words < 1`.

## Hints

<details><summary>Hint 1</summary>

Each node is a small function returning a dict, e.g. `lambda s: {"text": s["text"].lower(), "steps": ["lower"]}`.

</details>

<details><summary>Hint 2</summary>

`route = lambda s: "shorten" if len(s["text"].split()) > max_words else END`.

</details>

<details><summary>Hint 3</summary>

Add the nodes, the fixed edges, `add_conditional_edges("check", route)` and `add_edge("shorten", "check")`, then `compile()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_worked_example` | Route from check to shorten while there are more than max_words words; shorten loops back to check. |
| `test_reducer_keeps_existing_steps` | Annotate steps with operator.add and return only new steps from each node. |
| `test_nodes` | Name the nodes strip, lower, check and shorten. |
| `test_invalid` | Raise ValueError when max_words < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each node returns only the keys it changes; the `operator.add` reducer appends step names. The
conditional edge after `check` either loops through `shorten` or ends, so the loop's condition lives
in one routing function rather than inside the nodes.

## References

- [Graph API (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/graph-api) — LangChain (`S136`)
- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
