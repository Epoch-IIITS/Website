# AG-10 · Conversation Memory Window by Hand

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** AG-06 ReAct Loop with a Scripted Model

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `count_tokens(text)` → `len(text.split())`.
* `fit_context(messages, budget)` → new list per the algorithm (the newest kept message is never
  dropped to make room for the marker; omit the marker instead), cost of a message =
  `count_tokens(content) + 4`. The marker text is exactly `f"[{n} earlier messages omitted]"`.

**Example**
```python
msgs = [{"role": "system", "content": "be helpful"},
        {"role": "user", "content": "one two three four five six"},
        {"role": "assistant", "content": "a b c"},
        {"role": "user", "content": "ok"}]
[m["content"] for m in fit_context(msgs, 20)]
# ['be helpful', '[2 earlier messages omitted]', 'ok']
```

## Hints

<details><summary>Hint 1</summary>

Split off the system message: `head = messages[:1] if messages and messages[0]['role'] == 'system' else []`.

</details>

<details><summary>Hint 2</summary>

Walk `reversed(rest)` adding while `used + cost <= budget`; stop at the first that doesn't fit.

</details>

<details><summary>Hint 3</summary>

If dropped > 0: build the marker; while it doesn't fit, pop the oldest kept message (unless only one is left) and recompute n.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Keep newest messages first; if the marker doesn't fit, drop the oldest kept message. |
| `test_budget_respected` | Count 4 overhead tokens per message, including the marker. |
| `test_marker_fits` | Insert the marker right after the system message when something was dropped. |
| `test_no_system` | Only keep a system message if the first message has role 'system'. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The system message is always kept. Recent messages are added newest-first until the budget would be
exceeded, which yields a contiguous recent window. If history was dropped, a marker is inserted; when
the marker itself doesn't fit, the oldest kept message is sacrificed and the count updated.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
