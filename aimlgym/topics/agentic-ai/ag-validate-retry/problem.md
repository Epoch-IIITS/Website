# AG-14 · Validating Tool Arguments and Retrying

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** langchain-core

**Builds on:** AG-13 Dependency-Ordered Plans, AG-09 Conversation Memory with trim_messages, LM-19 Structured Output with Pydantic and Retries

Read the lesson first: [article.md](article.md)

## Task

1. `class BookingArgs(BaseModel)` with `room: str = Field(pattern=r"^R\d{3}$")` and
   `hour: int = Field(ge=9, le=17)`.
2. `book_room` — a `@tool(args_schema=BookingArgs)` with docstring `"Book a meeting room for one hour."`
   returning `f"booked {room} at {hour}:00"`.
3. `call_with_validation(model, tool, messages, max_attempts=3)` repeats up to `max_attempts` times:
   `reply = model.invoke(messages)`; if the reply has no tool calls, return `(None, attempt)`; otherwise
   invoke `tool` with the first call's args. On success return `(result, attempt)`. On
   `ValidationError`, append the reply and a `ToolMessage` with
   `content="Invalid arguments: " + "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in error.errors())`,
   `status="error"` and the call's id, and continue. After the last failed attempt return
   `(None, max_attempts)`. Attempts are counted from 1; the caller's `messages` list must not be modified.

## Hints

<details><summary>Hint 1</summary>

Copy the conversation first: `history = list(messages)`.

</details>

<details><summary>Hint 2</summary>

Inside the loop: `call = reply.tool_calls[0]`, then `tool.invoke(call["args"])` in a try block.

</details>

<details><summary>Hint 3</summary>

On ValidationError: `history += [reply, ToolMessage(content=..., tool_call_id=call["id"], status="error")]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_schema` | Use Field(pattern=r'^R\d{3}$') for room and Field(ge=9, le=17) for hour, and @tool(args_schema=BookingArgs). |
| `test_retry_with_feedback` | Append the reply and an error ToolMessage listing each invalid field. |
| `test_gives_up` | Stop after max_attempts and return (None, max_attempts). |
| `test_caller_messages_unchanged` | Work on a copy of messages. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The Pydantic schema states the constraints once; the tool enforces them on every call. Each failure is
summarised field by field and sent back as an error tool message tied to the call, so the model can
correct itself; the attempt counter bounds the loop.

## References

- [Tools (LangChain docs)](https://docs.langchain.com/oss/python/langchain/tools) — LangChain (`S134`)
- [Validators (Pydantic docs)](https://docs.pydantic.dev/latest/concepts/validators/) — Pydantic (`S140`)
