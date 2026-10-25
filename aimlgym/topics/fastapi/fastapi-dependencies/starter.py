from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field


class NoteStore:
    def __init__(self):
        self.notes = []

    def add(self, owner, text):
        # TODO
        return {}

    def for_owner(self, owner):
        # TODO
        return []


STORE = NoteStore()
API_KEYS = {"key-ada": "ada", "key-bob": "bob"}
EVENTS = []


def get_store():
    return STORE


def current_user(x_api_key: Annotated[str | None, Header()] = None):
    # TODO: 401 for missing or unknown keys
    return "ada"


def pagination(limit: int = 10, offset: int = 0):
    # TODO: constraints
    return {"limit": limit, "offset": offset}


def request_log():
    # TODO: yield with cleanup
    return EVENTS


class NoteIn(BaseModel):
    text: str = Field(min_length=1)


def create_app():
    app = FastAPI()
    # TODO: POST /notes and GET /notes with Depends
    return app
