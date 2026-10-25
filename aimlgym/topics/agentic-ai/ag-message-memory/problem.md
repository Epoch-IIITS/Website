# AG-09 · Conversation Memory with trim_messages

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** langchain-core

**Builds on:** AG-08 A ReAct Agent in LangGraph

Read the lesson first: [article.md](article.md)

## Task

1. `trim_history(messages, max_messages)` returns `trim_messages(messages, max_tokens=max_messages,
   token_counter=len, strategy="last", include_system=True, start_on="human")`.
2. `count_words(messages)` returns the total number of whitespace-separated words in the messages'
   `content`.
3. `trim_by_words(messages, max_words)` trims the same way but with `count_words` as the counter.

Raise `ValueError` in the trimming functions for a budget below 1.

## Hints

<details><summary>Hint 1</summary>

Both trimming functions call `trim_messages` with `strategy="last"`, `include_system=True`, `start_on="human"`.

</details>

<details><summary>Hint 2</summary>

A token counter receives a list of messages: `sum(len(str(m.content).split()) for m in messages)`.

</details>

<details><summary>Hint 3</summary>

Pass the function itself (`token_counter=count_words`), not its result.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_budget_three` | Use strategy='last' and include_system=True. |
| `test_starts_on_human` | start_on='human' drops a leading AI message from the kept window. |
| `test_trim_by_words` | Pass count_words itself as token_counter. |
| `test_original_unchanged_and_invalid` | Return a trimmed copy and reject budgets below 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One helper holds the policy — keep the latest turns, the system message, and start on a human turn —
and the two public functions differ only in how size is measured: number of messages or number of
words.

## References

- [Short-term memory (LangChain docs)](https://docs.langchain.com/oss/python/langchain/short-term-memory) — LangChain (`S135`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
