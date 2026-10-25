from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError


class BookingArgs(BaseModel):
    # TODO
    pass


# TODO: book_room tool


def call_with_validation(model, tool, messages, max_attempts=3):
    # TODO
    pass
