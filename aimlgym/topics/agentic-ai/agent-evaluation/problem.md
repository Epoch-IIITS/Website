# AG-20 · Evaluating Agents

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** AG-06 ReAct Loop with a Scripted Model, AG-18 Guardrails with Human Approval

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `normalize_answer(text)` — `None` → `""`; otherwise lowercase, strip, collapse internal
   whitespace to single spaces, then remove trailing `.` and `!` characters (and strip again).
2. `evaluate(agent, tasks)` → `{"results": [...], "pass_rate": float, "mean_tool_calls": float}`.
   Each result is `{"id": ..., "passed": bool, "reasons": [...]}` in task order, using the rules
   above. Call `agent(task["input"])` exactly once per task; catch any `Exception`.
   `mean_tool_calls` averages over tasks that did not error (0.0 if none). An empty task list
   gives pass rate 0.0.
3. `regressions(old_report, new_report)` → sorted list of task ids that passed in `old_report` and
   failed (or are missing) in `new_report`.

## Hints

<details><summary>Hint 1</summary>

`" ".join(text.lower().split()).rstrip(".!").strip()` normalises.

</details>

<details><summary>Hint 2</summary>

Wrap only the agent call in `try/except Exception as e:` and record `f"error: {type(e).__name__}"`.

</details>

<details><summary>Hint 3</summary>

For regressions build `{r["id"]: r["passed"] for r in report["results"]}` for both reports.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_normalize` | Lowercase, collapse whitespace, then strip trailing '.' and '!'. |
| `test_reasons` | Check status, answer, budget and forbidden tools in that order; an exception gives only an error reason. |
| `test_summary` | Average tool calls only over tasks that returned a result. |
| `test_calls_agent_once_per_task` | Call the agent exactly once per task, in order. |
| `test_regressions` | A regression passed before and fails (or is missing) now; return ids sorted. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each task is isolated in its own `try`, so a crash becomes an `error:` result instead of stopping
the run. Every check appends a human-readable reason, which makes failures actionable, and a task
passes only when the list is empty. Comparing two reports by task id exposes regressions that an
unchanged pass rate would hide.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) — Hugging Face (`S102`)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
