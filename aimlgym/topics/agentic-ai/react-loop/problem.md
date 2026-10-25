# AG-06 · ReAct Loop with a Scripted Model

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** AG-02 Parsing Model Tool Calls, AG-05 Goal Tests and Step Budgets

Read the lesson first: [article.md](article.md)

## Task

Write `react_agent(model, registry, question, max_steps=5)` returning
`{"status": "final" | "step_limit", "answer": str | None, "transcript": list, "tool_calls": int}`
following the procedure above. Include your own copies of the AG-01 registry interface usage
(`registry.dispatch(call)`) and AG-02 parser (copy `parse_model_output`). `json.dumps` tool results with
default settings. `model(transcript)` receives a *copy* of the transcript list.

**Example**
```python
r = react_agent(scripted_model, reg, "What is 2 + 3?")
r["status"], r["answer"], r["tool_calls"]    # ('final', '5', 1)
```

## Hints

<details><summary>Hint 1</summary>

`transcript = [{'role': 'user', 'content': question}]`.

</details>

<details><summary>Hint 2</summary>

After parsing a tool call: `res = registry.dispatch({'tool': p['tool'], 'args': p['args']})`.

</details>

<details><summary>Hint 3</summary>

Append `{'role': 'tool', 'content': json.dumps(res)}`; count tool calls.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_transcript_shape` | Append the assistant message, then a tool message with json.dumps(result). |
| `test_invalid_reported` | Report parse errors to the model as {'ok': False, 'error': ...}. |
| `test_step_limit` | Stop after max_steps model calls with status 'step_limit'. |
| `test_model_sees_observation` | Call the model with the transcript including previous observations. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each iteration asks the model for its next message, parses it, and either finishes, executes a tool,
or reports a parse error — always appending an observation so the model sees the consequence of its
action. The step limit guarantees termination.

## References

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
