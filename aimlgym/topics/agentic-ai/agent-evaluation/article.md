# Evaluating Agents

## Learning outcomes

After this lesson you can:

- Define pass/fail criteria for an agent task: answer, budget and forbidden actions
- Normalise answers before comparing them
- Run a suite of tasks, isolating crashes so one failure does not stop the run
- Compare two agent versions and list regressions

## Intuition
An agent that worked once may fail tomorrow after a prompt change, a new tool or a different
model. An **evaluation harness** runs the agent on a fixed set of tasks with known expected
outcomes and reports what passed, what failed and why — the agent equivalent of unit tests
(PY-27).

## Precise explanation
An evaluation task here is a dict:
```python
{"id": "add-1", "input": "What is 2 + 3?", "expected": "5",
 "max_tool_calls": 2, "forbidden_tools": ["delete_file"]}
```
The agent is any function `agent(input)` returning
`{"status": "final" | ..., "answer": str | None, "tool_calls": int, "tools_used": [names]}`
(the shape of AG-06's result plus a list of tools it used).

A task **passes** only if every check holds; each failed check adds a **reason**:
* `"not final"` — the agent did not finish (`status != "final"`);
* `"wrong answer"` — normalised answer differs from the normalised expected answer;
* `"over budget"` — more tool calls than `max_tool_calls` (when given);
* `"forbidden tool: <name>"` — for each forbidden tool it used (sorted by name);
* `"error: <ExceptionType>"` — the agent raised; this replaces all other reasons.

**Normalisation** prevents false failures: lowercase, strip, collapse whitespace, and remove
trailing `.`/`!` so `"Paris."` equals `"paris"`. Keep it minimal — over-normalising hides real
mistakes.

**Regressions**: tasks that passed with the old version and fail with the new one. Track the pass
rate *and* the list of regressions; a stable pass rate can hide one fixed task and one broken task.

## Worked example
Three tasks; the agent answers the first correctly with one tool call, answers the second
correctly but uses a forbidden tool, and crashes on the third: pass rate 1/3, reasons
`[]`, `["forbidden tool: rm"]`, `["error: KeyError"]`.

## Common mistakes
* Letting one exception abort the whole evaluation.
* Comparing raw strings, so trailing punctuation fails a correct answer.
* Measuring only final answers and ignoring unsafe or wasteful behaviour.
* Using a live model in tests, making results non-deterministic; use scripted agents for the
  harness itself.

## Why this matters
Evaluation is how teams decide whether an agent change is an improvement and whether it is safe
to deploy; guardrail checks (AG-19) become evaluation criteria.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) — Hugging Face (`S102`)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
