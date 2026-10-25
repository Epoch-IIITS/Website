# AG-17 · Orchestrator-Workers Pipeline by Hand

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** AG-13 Dependency-Ordered Plans, AG-15 Validate-and-Retry Tool Calls

Read the lesson first: [article.md](article.md)

## Task

Write `orchestrate(task, planner, workers, evaluator, max_rounds=2)` returning
`{"accepted": bool, "outputs": dict, "rounds": int, "log": list}` where `log` contains strings:
`"round <r>: plan <ids in execution order>"`, `"round <r>: <id> -> <type>"` for each executed subtask,
`"round <r>: error <id>: <message>"` (unknown type: `"unknown worker '<type>'"`; exception:
`"<ExceptionType>: <msg>"`), and `"round <r>: evaluator accepted"` / `"round <r>: evaluator rejected: <feedback>"`.
`outputs` are from the last round. Cycles in a plan → `ValueError`.

**Example**
```python
r = orchestrate("brief on solar", planner, workers, evaluator)
r["accepted"], r["rounds"]   # (True, 2)
```

## Hints

<details><summary>Hint 1</summary>

Topological order of subtasks by `deps` using a heap of ready ids (AG-13).

</details>

<details><summary>Hint 2</summary>

Call `workers[s['type']](s['input'], {d: outputs[d] for d in s['deps']})` inside try/except.

</details>

<details><summary>Hint 3</summary>

On a worker error, log it, mark the round failed and skip the evaluator; set `feedback` accordingly.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_log` | Log the plan, each executed subtask and the evaluator decision with the exact formats. |
| `test_dependency_order` | Execute subtasks in dependency order (smallest ready id first). |
| `test_two_rounds` | Pass the evaluator's feedback to the planner in the next round. |
| `test_worker_exception` | Catch worker exceptions, log them and skip evaluation for that round. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each round plans, orders subtasks by dependencies, routes each to its worker with its dependencies'
outputs, and asks the evaluator to accept or give feedback. Worker failures are logged and end the
round without evaluation; the round cap prevents endless revision loops.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
