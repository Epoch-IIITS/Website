# Conversation Memory with trim_messages

## Learning outcomes

After this lesson you can:

- Keep a conversation within a budget with trim_messages
- Keep the system message and start the kept history on a human turn
- Write a custom token counter

## Intuition
A model can only read a limited context, and every token costs time and money. Long conversations must
be cut down: keep the system instructions, keep the most recent turns, drop the oldest — without
leaving a reply whose question was dropped.

## Precise explanation
```python
from langchain_core.messages import trim_messages

trim_messages(messages, max_tokens=4, token_counter=len,       # len counts messages
              strategy="last", include_system=True, start_on="human")
```

* `strategy="last"` keeps the end of the conversation; `include_system=True` always keeps a leading
  system message (it counts towards the budget).
* `start_on="human"` drops messages from the front of the kept window until it starts with a human
  message, so the history never opens with an orphaned AI reply or tool result.
* `token_counter` is either a model (to count real tokens) or a function that receives a **list of
  messages** and returns a number. `len` counts messages; a word counter approximates tokens.
* Trimming returns a new list; the stored history is unchanged.

## Worked example
[system, human "a", ai "b", human "c", ai "d"] with a budget of 3 messages keeps system, human "c" and
ai "d". With a budget of 4, the window [ai "b", human "c", ai "d"] would start with an AI message, so
"b" is dropped too.

## What the library does inside
The sliding window of AG-10 (the optional deep dive after this step), measured in the
units you choose and aware of message roles.

## Common mistakes
* Dropping the system message and losing the instructions.
* Cutting a tool result away from the AI message that requested it.
* Counting characters when the limit is in tokens; use the model's own counter in production.

## Why this matters
Every long-running assistant needs a memory policy; trimming is the simplest, and summarising old turns
is the next step.

## References

- [Short-term memory (LangChain docs)](https://docs.langchain.com/oss/python/langchain/short-term-memory) — LangChain (`S135`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
