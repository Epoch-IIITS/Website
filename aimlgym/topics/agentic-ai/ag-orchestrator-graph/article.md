# Orchestrator and Workers in LangGraph

## Learning outcomes

After this lesson you can:

- Fan out work to parallel workers with Send
- Collect worker results with a reducer and restore their order
- Combine results in a synthesiser node

## Intuition
Some tasks split naturally: summarise each section of a report, check each file, answer each
sub-question. An **orchestrator** decides the pieces, **workers** handle one piece each (in parallel
when possible), and a **synthesiser** combines their results. How many workers are needed is known
only at run time.

## Precise explanation
```python
from langgraph.types import Send

def assign(state):                                   # a conditional edge that fans out
    return [Send("worker", {"index": i, "section": s}) for i, s in enumerate(state["sections"])]

graph.add_conditional_edges("orchestrator", assign, ["worker"])
graph.add_edge("worker", "synthesise")
```

* `Send(node, payload)` runs `node` with its own payload instead of the shared state; returning a list
  of `Send`s starts one worker per item.
* Workers write to a key with a reducer (`Annotated[list, operator.add]`), so their results are
  collected rather than overwritten. Parallel results arrive in no guaranteed order — include an index
  and sort in the synthesiser.
* The synthesiser runs once, after all workers of that step have finished.
* With zero items no worker runs, and nothing after them runs either; handle that case where it matters.

## Worked example
A document with sections "intro text", "methods text" and "results text" becomes three worker calls.
With a worker that returns the section's word count, the synthesiser writes
"1: 2 words | 2: 2 words | 3: 2 words".

## What the library does inside
The task splitting and merging of AG-17 (the optional deep dive after this step),
with LangGraph scheduling the workers and merging their state updates.

## Common mistakes
* Workers returning plain values for a key without a reducer, so only one result survives.
* Assuming results arrive in order.
* Passing the whole state to each worker when it needs only its piece.

## Why this matters
Research assistants, code reviewers and report writers use this pattern to split large jobs across
many model calls.

## References

- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
- [Graph API (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/graph-api) — LangChain (`S136`)
