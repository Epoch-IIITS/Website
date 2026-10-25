# AG-18 · Guardrails with Human Approval

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** langgraph

**Builds on:** AG-16 Orchestrator and Workers in LangGraph

Read the lesson first: [article.md](article.md)

## Task

1. `build_guarded_graph(tools, sensitive)` (`tools` is a dict from name to a function taking `**args`;
   `sensitive` a set of names) returns a graph compiled with `InMemorySaver` over the state
   `{"action": dict, "outcome": str}` with nodes:
   * `"guard"`: unknown tool → `{"outcome": "blocked"}`; sensitive tool → `decision = interrupt({"action": action})`,
     and anything other than `"approve"` → `{"outcome": "rejected"}`; otherwise continue to execute;
   * `"execute"`: runs `tools[name](**args)` and sets `outcome` to `f"approved: {result}"`.
   Edges: START → guard; from guard to `"execute"` unless the outcome is already `"blocked"` or
   `"rejected"` (then END); execute → END.
2. `run_with_approval(app, action, thread_id, decide)` invokes the graph with
   `{"action": action, "outcome": ""}`; if the result contains `"__interrupt__"`, calls
   `decide(payload)` with the interrupt's value and resumes with `Command(resume=decision)`.
   Return the final `outcome`.

## Hints

<details><summary>Hint 1</summary>

The guard node returns `{}` when the action may run, so the router can send it to execute.

</details>

<details><summary>Hint 2</summary>

`route = lambda s: END if s["outcome"] in ("blocked", "rejected") else "execute"`.

</details>

<details><summary>Hint 3</summary>

`result = app.invoke(...)`; `if "__interrupt__" in result: result = app.invoke(Command(resume=decide(result["__interrupt__"][0].value)), config)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_safe_action_runs_without_asking` | Only sensitive tools call interrupt(). |
| `test_sensitive_action_approved` | Resume with Command(resume=decision) on the same thread_id. |
| `test_only_exact_approve` | Treat anything except 'approve' as a rejection. |
| `test_sent_once_after_resume` | Run the tool in the execute node, after the approval, not inside guard. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The guard classifies every action. For sensitive ones `interrupt` saves the state and returns control
to the caller with the action to review; resuming on the same thread feeds the decision back into the
guard. Only an exact "approve" lets the action reach the execute node, where the side effect happens.

## References

- [Interrupts (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/interrupts) — LangChain (`S138`)
- [Persistence (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/persistence) — LangChain (`S137`)
