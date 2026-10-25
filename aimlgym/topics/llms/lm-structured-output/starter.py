from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Answer(BaseModel):
    # TODO
    pass


def build_messages(question, parser):
    # TODO
    pass


def ask_structured(model, question, max_retries=2):
    # TODO
    pass
