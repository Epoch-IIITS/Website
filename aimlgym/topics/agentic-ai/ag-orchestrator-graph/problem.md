# AG-16 · Orchestrator and Workers in LangGraph

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** langgraph

**Builds on:** AG-14 Validating Tool Arguments and Retrying

Read the lesson first: [article.md](article.md)

## Task

Write `build_report_graph(worker_fn)` returning a compiled graph over the state
`{"document": str, "sections": list, "results": Annotated[list, operator.add], "report": str}`:

* `"orchestrator"` splits the document on blank lines (`"\n\n"`), keeping non-empty, stripped sections;
* a conditional edge sends each section to `"worker"` with `Send("worker", {"index": i, "section": s})`;
* `"worker"` returns `{"results": [(index, worker_fn(section))]}`;
* `"synthesise"` sorts the results by index and sets `report` to
  `" | ".join(f"{i + 1}: {summary}" for i, summary in sorted_results)`.

Edges: START → orchestrator → (Send) worker → synthesise → END.

## Hints

<details><summary>Hint 1</summary>

`orchestrator` returns `{"sections": [s.strip() for s in state["document"].split("\n\n") if s.strip()]}`.

</details>

<details><summary>Hint 2</summary>

The fan-out function returns a list of `Send("worker", {...})`; register it with `add_conditional_edges("orchestrator", assign, ["worker"])`.

</details>

<details><summary>Hint 3</summary>

The worker receives the Send payload (with `index` and `section`), not the whole state.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_worked_example` | Fan out with Send('worker', {'index': i, 'section': s}) and join results in synthesise. |
| `test_order_restored` | Sort the collected (index, summary) pairs before joining. |
| `test_one_worker_per_section` | Split on blank lines and drop empty sections. |
| `test_results_collected` | Annotate results with operator.add so every worker's update is kept. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The orchestrator decides the work; `Send` starts one worker per section with only that section; the
reducer collects the indexed results; the synthesiser restores the order and writes one report.

## References

- [Workflows and agents (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — LangChain (`S139`)
- [Graph API (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/graph-api) — LangChain (`S136`)
