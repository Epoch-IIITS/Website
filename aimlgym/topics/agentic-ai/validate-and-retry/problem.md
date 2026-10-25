# AG-15 · Validate-and-Retry Tool Calls

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** AG-02 Parsing Model Tool Calls, AG-06 ReAct Loop with a Scripted Model

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `validate(obj, schema)` → list of errors using exactly these messages:
  `"<f>: missing"`, `"<f>: expected <type>"`, `"<f>: must be one of <enum list repr>"`,
  `"<f>: must be >= <min>"`, `"<f>: must be <= <max>"`, `"<f>: unexpected field"`
  (non-dict input → `["expected a JSON object"]`). Per field only the first failing check is reported.
* `call_with_retries(model, prompt, schema, max_attempts=3)` → dict
  `{"ok": bool, "value": obj | None, "attempts": int, "errors": list_of_error_lists}`. Invalid JSON counts
  as the error list `["invalid JSON"]`. Feedback message: `"Your output was invalid: " + "; ".join(errors)`.
  `model(messages)` receives a copy of the message list (strings).

**Example**
```python
schema = {"city": {"type": str}, "days": {"type": int, "min": 1, "max": 14}}
validate({"city": "Pune", "days": "3"}, schema)    # ['days: expected int']
```

## Hints

<details><summary>Hint 1</summary>

Loop `for f in sorted(schema)`; use `continue` after the first error for a field.

</details>

<details><summary>Hint 2</summary>

Type check: reject bools when the type is int/float; accept ints for float.

</details>

<details><summary>Hint 3</summary>

Retry loop: on failure append the raw text and the feedback string to messages.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_messages` | Check fields in sorted order; report only the first failing check per field; unexpected fields last. |
| `test_feedback_sent` | Append the model's text and 'Your output was invalid: ' + '; '.join(errors). |
| `test_retry_success` | Stop at the first valid attempt and report attempts used. |
| `test_exhausted` | Give up after max_attempts and return all error lists. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Validation checks each field in a fixed order and stops at its first problem, producing precise,
stable messages. The retry loop gives the model its previous output plus those messages, stops at the
first valid result, and records every failed attempt's errors for debugging.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
