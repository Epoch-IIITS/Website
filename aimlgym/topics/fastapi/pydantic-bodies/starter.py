from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    name: str
    price: float
    # TODO: constraints, tags, quantity, model_config


def parse_item(data):
    # TODO
    return Item(**data)


app = FastAPI()

# TODO: POST /items
