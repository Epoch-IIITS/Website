r"""Reference solution for AG-14 Validating Tool Arguments and Retrying.

The Pydantic schema states the constraints once; the tool enforces them on every call. Each failure is
summarised field by field and sent back as an error tool message tied to the call, so the model can
correct itself; the attempt counter bounds the loop.
"""
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError


class BookingArgs(BaseModel):
    room: str = Field(pattern=r"^R\d{3}$")
    hour: int = Field(ge=9, le=17)


@tool(args_schema=BookingArgs)
def book_room(room: str, hour: int) -> str:
    """Book a meeting room for one hour."""
    return f"booked {room} at {hour}:00"


def call_with_validation(model, tool, messages, max_attempts=3):
    history = list(messages)
    for attempt in range(1, max_attempts + 1):
        reply = model.invoke(history)
        if not reply.tool_calls:
            return None, attempt
        call = reply.tool_calls[0]
        try:
            return tool.invoke(call["args"]), attempt
        except ValidationError as error:
            summary = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in error.errors())
            history = history + [reply, ToolMessage(content="Invalid arguments: " + summary,
                                                    tool_call_id=call["id"], status="error")]
    return None, max_attempts
