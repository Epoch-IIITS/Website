# Validate and Retry

## Learning outcomes

After this lesson you can:

- Validate structured output against a schema (types, required fields, enums, ranges)
- Feed precise errors back to the model and retry
- Bound retries and report every attempt

## Intuition
Models make formatting mistakes: a missing field, "5" instead of 5, a value outside the allowed list.
Instead of failing, check the output against a schema, tell the model exactly what was wrong, and let it
try again — a few times at most.

## Precise explanation
Schema format used here: dict field → spec with keys `type` (Python type), optional `required`
(default True), `enum` (allowed values), `min`/`max` (numeric bounds).
`validate` returns a **list of error strings** (empty = valid), checking in a fixed order per field
(sorted field names): missing required → type (bools are not ints) → enum → range; then unexpected
fields.
The retry loop:
```text
messages = [prompt]
for attempt in 1..max_attempts:
    text = model(messages); parse JSON; validate
    if ok: return success
    messages.append(text); messages.append("Your output was invalid: " + "; ".join(errors))
return failure with all errors
```
This is the "evaluator–optimizer" pattern in miniature (Anthropic's agent guide) and mirrors ReAct's use
of observations to correct course.

## Worked example
Schema {city: str, days: int (1..14)}; attempt 1 `{"city": "Pune", "days": "3"}` → error
"days: expected int"; attempt 2 `{"city": "Pune", "days": 3}` → success.

## Common mistakes
* Vague feedback ("invalid") — the model can't fix what it can't see.
* Unlimited retries.
* Coercing types silently ("3" → 3) and hiding real bugs.

## Why this matters
Reliable structured outputs are what let agents call real APIs safely.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
