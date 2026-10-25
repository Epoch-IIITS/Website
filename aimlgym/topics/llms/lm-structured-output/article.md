# Structured Output with Pydantic and Retries

## Learning outcomes

After this lesson you can:

- Describe the expected answer with a Pydantic model and format instructions
- Parse model replies with PydanticOutputParser and catch OutputParserException
- Retry with the error message when the reply is invalid

## Intuition
Programs need data, not prose: an answer, a confidence, a list of sources. Describe that shape with a
Pydantic model, tell the language model to reply in that JSON shape, and validate the reply. Models
sometimes break the format, so when parsing fails, show the model the error and ask again — a few
times at most.

## Precise explanation
```python
class Answer(BaseModel):
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    sources: list[int] = []

parser = PydanticOutputParser(pydantic_object=Answer)
parser.get_format_instructions()      # text with the JSON schema, to put in the prompt
parser.parse(reply.content)           # an Answer, or OutputParserException
```

* The parser accepts plain JSON or JSON inside a ```json fence, then validates it with Pydantic:
  wrong types, missing fields and out-of-range values all raise `OutputParserException`.
* Retry loop: keep the conversation, append the failed reply and a human message quoting the error,
  invoke again. Stop after a fixed number of retries and re-raise the last error.
* Many providers also offer native structured output (`model.with_structured_output(Answer)`);
  the validation-and-retry idea is the same.

## Worked example
Reply 1: "Sure! The answer is 4." → not JSON, parse fails. The model is told
"Your reply could not be parsed: … Reply again with only the JSON object." Reply 2:
`{"answer": "4", "confidence": 0.95, "sources": [1]}` → `Answer(answer='4', confidence=0.95, sources=[1])`
after two attempts.

## What the library does inside
It extracts the JSON, then runs Pydantic's validation (FA-10). The retry loop is the
validate-and-retry pattern you will meet again with agents.

## Common mistakes
* Trusting `json.loads` alone, without range and type validation.
* Retrying without telling the model what was wrong.
* Retrying forever (or catching every exception and hiding real bugs).

## Why this matters
Structured output connects language models to the rest of a program: databases, APIs, tool calls
and user interfaces all need validated data.

## References

- [Structured output (LangChain docs)](https://docs.langchain.com/oss/python/langchain/structured-output) — LangChain (`S131`)
- [Validators (Pydantic docs)](https://docs.pydantic.dev/latest/concepts/validators/) — Pydantic (`S140`)
