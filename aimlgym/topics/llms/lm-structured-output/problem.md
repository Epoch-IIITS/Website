# LM-19 · Structured Output with Pydantic and Retries

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** langchain-core

**Builds on:** LM-17 Chat Prompts and Messages with LangChain

Read the lesson first: [article.md](article.md)

## Task

1. `class Answer(BaseModel)` with `answer: str = Field(min_length=1)`, `confidence: float = Field(ge=0, le=1)`
   and `sources: list[int] = []`.
2. `build_messages(question, parser)` returns
   `[SystemMessage("Answer the question.\n" + parser.get_format_instructions()), HumanMessage(question)]`.
3. `ask_structured(model, question, max_retries=2)` makes a `PydanticOutputParser(pydantic_object=Answer)`,
   invokes `model` with the messages and tries to parse the reply's `content`. On
   `OutputParserException`, append the reply and
   `HumanMessage(f"Your reply could not be parsed: {error}\nReply again with only the JSON object.")`
   and try again, up to `max_retries` retries. Return `(answer, attempts)`; if every attempt fails,
   raise the last `OutputParserException`.

## Hints

<details><summary>Hint 1</summary>

`Field(ge=0, le=1)` bounds the confidence; `Field(min_length=1)` forbids an empty answer.

</details>

<details><summary>Hint 2</summary>

Loop `for attempt in range(max_retries + 1)`: `reply = model.invoke(messages)`, then `parser.parse(reply.content)` inside try.

</details>

<details><summary>Hint 3</summary>

In the except branch save the error and extend the message list with the reply and a corrective HumanMessage.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_retry_after_prose` | Catch OutputParserException and invoke the model again. |
| `test_out_of_range_is_invalid` | Bound confidence with Field(ge=0, le=1); sources defaults to []. |
| `test_gives_up` | After max_retries retries, raise the last OutputParserException. |
| `test_messages_and_feedback` | Append the failed reply and a HumanMessage containing 'could not be parsed'. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The Pydantic model is the contract; its format instructions go into the system message. Each reply is
parsed and validated; a failure becomes feedback in the conversation so the next attempt can correct
it, and the loop gives up after a fixed number of retries.

## References

- [Structured output (LangChain docs)](https://docs.langchain.com/oss/python/langchain/structured-output) — LangChain (`S131`)
- [Validators (Pydantic docs)](https://docs.pydantic.dev/latest/concepts/validators/) — Pydantic (`S140`)
