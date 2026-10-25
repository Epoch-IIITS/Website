# Validating Tool Arguments and Retrying

## Learning outcomes

After this lesson you can:

- Give a tool a Pydantic argument schema with constraints
- Return validation errors to the model as tool messages
- Retry a fixed number of times and stop cleanly

## Intuition
Models make plausible mistakes: a room "101" where the format is "R101", a meeting at 8 pm when the
building closes at 5. If the tool simply runs, it does damage; if it crashes, the agent stops. The
middle way: validate the arguments, tell the model exactly what was wrong, and let it try again.

## Precise explanation
```python
class BookingArgs(BaseModel):
    room: str = Field(pattern=r"^R\d{3}$", description="Room id such as R101")
    hour: int = Field(ge=9, le=17, description="Start hour, 9 to 17")

@tool(args_schema=BookingArgs)
def book_room(room: str, hour: int) -> str:
    """Book a meeting room for one hour."""
```

* `args_schema` makes the schema (including the descriptions) visible to the model and enforces it:
  `book_room.invoke(bad_args)` raises `pydantic.ValidationError`.
* `error.errors()` lists each problem with its field (`loc`) and message (`msg`); a compact summary such
  as `room: String should match pattern '^R\d{3}$'` is what the model needs.
* Loop: invoke the model → take its first tool call → validate and run. On failure append the AI message
  and a `ToolMessage(content="Invalid arguments: ...", tool_call_id=..., status="error")`, then ask again.
  Stop after `max_attempts` and report failure instead of looping.

## Worked example
Attempt 1: `{"room": "101", "hour": 20}` → "Invalid arguments: room: String should match pattern
'^R\d{3}$'; hour: Input should be less than or equal to 17". Attempt 2: `{"room": "R101", "hour": 16}`
→ "booked R101 at 16:00".

## What the library does inside
Pydantic validation replaces the hand-written checks in AG-15 (the optional deep dive
after this step); the retry loop is the same idea with real messages.

## Common mistakes
* Retrying without the error, so the model repeats the same mistake.
* Catching all exceptions, including bugs inside the tool, as if they were bad arguments.
* Unlimited retries.

## Why this matters
Validated tools are the first line of defence for agents that act in the world — booking, paying,
editing files.

## References

- [Tools (LangChain docs)](https://docs.langchain.com/oss/python/langchain/tools) — LangChain (`S134`)
- [Validators (Pydantic docs)](https://docs.pydantic.dev/latest/concepts/validators/) — Pydantic (`S140`)
