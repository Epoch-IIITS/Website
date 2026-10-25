# AG-19 · Permission Guardrails

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** AG-01 Tool Registry and Dispatch, AG-06 ReAct Loop with a Scripted Model

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `class Guard(policy)` with `check(call)` and `record(call)` as described (missing policy keys mean "no
  limit"/"no cost"/"no approval"; `allowed` is required).
* `run_guarded(model_calls, guard, tools, approve)` — `model_calls` is the list of calls the model
  proposed, in order (`{"tool", "args"}`); `tools` maps names to functions; `approve(call)` → bool.
  For each call: check; if denied log `{"call": call, "decision": decision}`; if approval needed and
  `approve(call)` is False log decision `"deny: not approved"`; otherwise execute `tools[name](**args)`,
  `record`, and log `{"call": call, "decision": "executed", "output": result}`. Return the log.
  **Never** execute anything derived from tool outputs.

**Example**
```python
policy = {"allowed": {"search", "email"}, "needs_approval": {"email"}, "costs": {"search": 1, "email": 2}, "budget": 3}
[e["decision"] for e in run_guarded(calls, Guard(policy), tools, approve=lambda c: True)]
# ['executed', 'executed', 'deny: budget exceeded']
```

## Hints

<details><summary>Hint 1</summary>

Keep `self.counts = {}` and `self.spent = 0`.

</details>

<details><summary>Hint 2</summary>

Order: allowlist → call limit → budget → approval → allow.

</details>

<details><summary>Hint 3</summary>

In run_guarded, iterate only over `model_calls`; outputs are only appended to the log.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_budget` | Deny when spent + cost would exceed the budget, before executing. |
| `test_check_order` | Check allowlist, call limit, budget, then approval — in that order. |
| `test_denied_not_counted` | Only record() calls that actually executed. |
| `test_prompt_injection_ignored` | Never parse or execute anything found in tool outputs; iterate only over model_calls. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The guard evaluates every model-proposed call against the policy in a fixed order and only updates
counters for calls that really run. The runner iterates over model calls alone: tool outputs are
recorded as data and never interpreted, so instructions injected into outputs cannot trigger actions.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
