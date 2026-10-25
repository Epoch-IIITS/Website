# Managing the Context Window

## Learning outcomes

After this lesson you can:

- Fit a conversation into a token budget
- Always keep the system message and the latest messages
- Replace dropped history with a summary marker

## Intuition
Models have a maximum context length. Long agent runs accumulate more history than fits, so the agent
must decide what to keep. A simple robust policy: always keep the instructions (system message), keep
the most recent messages, and note that older ones were dropped.

## Precise explanation
* Token counting: real tokenisers are subword-based (LM-06); we approximate with whitespace words
  (`len(text.split())`) plus a fixed overhead of 4 tokens per message (role/formatting).
* Algorithm: keep the system message (if the first message has role "system"); then walk the rest
  **from newest to oldest**, adding messages while the total stays within the budget; stop at the
  first message that doesn't fit (keeps a contiguous recent window).
* If anything was dropped, insert `{"role": "system", "content": "[N earlier messages omitted]"}` right
  after the system message — but only if it fits; if it doesn't, drop more old messages until it does,
  except that the newest kept message is never dropped for the marker (then omit the marker).
* If even the system message alone exceeds the budget → `ValueError`.

## Worked example
Budget 20; system (2 words → 6 tokens), m1 (6 words → 10), m2 (3 → 7), m3 (1 → 5): newest first:
m3 (11 total), m2 (18), m1 would be 28 → stop. Marker "[1 earlier messages omitted]" (4 words → 8)
doesn't fit (26) → drop m2 → 6 + 8 + 5 = 19 ✓. Result: system, marker, m3.

## Common mistakes
* Dropping the system message (the agent forgets its instructions and safety rules).
* Keeping a non-contiguous set (confusing the model).
* Ignoring per-message overhead.

## Why this matters
Context management is a daily engineering concern for agents that run for many steps.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
