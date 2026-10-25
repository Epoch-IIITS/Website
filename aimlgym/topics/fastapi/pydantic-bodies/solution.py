r"""Reference solution for FA-10 Request Bodies with Pydantic.

The model states every rule declaratively; strict numeric fields and `extra="forbid"` reproduce
the hand-written validator's behaviour, and whitespace stripping happens before the length check.
FastAPI validates the body against the model and passes a typed object to the endpoint.
"""
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(ge=0, strict=True)
    tags: list[str] = []
    quantity: int = Field(default=0, ge=0, strict=True)


def parse_item(data):
    return Item.model_validate(data)


app = FastAPI()


@app.post("/items")
def create_item(item: Item):
    return {"item": item.model_dump(), "total": item.price * item.quantity}
