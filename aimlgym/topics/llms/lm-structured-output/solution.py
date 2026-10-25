r"""Reference solution for LM-19 Structured Output with Pydantic and Retries.

The Pydantic model is the contract; its format instructions go into the system message. Each reply is
parsed and validated; a failure becomes feedback in the conversation so the next attempt can correct
it, and the loop gives up after a fixed number of retries.
"""
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    sources: list[int] = []


def build_messages(question, parser):
    return [SystemMessage("Answer the question.\n" + parser.get_format_instructions()), HumanMessage(question)]


def ask_structured(model, question, max_retries=2):
    parser = PydanticOutputParser(pydantic_object=Answer)
    messages = build_messages(question, parser)
    last_error = None
    for attempt in range(max_retries + 1):
        reply = model.invoke(messages)
        try:
            return parser.parse(reply.content), attempt + 1
        except OutputParserException as error:
            last_error = error
            messages = messages + [reply, HumanMessage(
                f"Your reply could not be parsed: {error}\nReply again with only the JSON object.")]
    raise last_error
