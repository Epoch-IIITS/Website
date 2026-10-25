r"""Reference solution for FA-13 Dependencies and Dependency Overrides.

Each concern — storage, authentication, paging, request logging — is a small function that
endpoints declare with `Depends`. FastAPI resolves them per request, validates their parameters
and runs the code after `yield` once the response is done. Because endpoints never reach for
globals directly, tests can substitute any dependency through `dependency_overrides`.
"""
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field


class NoteStore:
    def __init__(self):
        self.notes = []

    def add(self, owner, text):
        note = {"id": len(self.notes) + 1, "owner": owner, "text": text}
        self.notes.append(note)
        return note

    def for_owner(self, owner):
        return [n for n in self.notes if n["owner"] == owner]


STORE = NoteStore()
API_KEYS = {"key-ada": "ada", "key-bob": "bob"}
EVENTS = []


def get_store():
    return STORE


def current_user(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key", headers={"WWW-Authenticate": "ApiKey"})
    return API_KEYS[x_api_key]


def pagination(limit: Annotated[int, Query(ge=1, le=50)] = 10,
               offset: Annotated[int, Query(ge=0)] = 0):
    return {"limit": limit, "offset": offset}


def request_log():
    EVENTS.append("open")
    try:
        yield EVENTS
    finally:
        EVENTS.append("close")


class NoteIn(BaseModel):
    text: str = Field(min_length=1)


def create_app():
    app = FastAPI()

    @app.post("/notes", status_code=201)
    def create_note(note: NoteIn,
                    user: Annotated[str, Depends(current_user)],
                    store: Annotated[NoteStore, Depends(get_store)]):
        return store.add(user, note.text)

    @app.get("/notes")
    def list_notes(user: Annotated[str, Depends(current_user)],
                   store: Annotated[NoteStore, Depends(get_store)],
                   page: Annotated[dict, Depends(pagination)],
                   log: Annotated[list, Depends(request_log)]):
        log.append("list")
        notes = store.for_owner(user)
        return notes[page["offset"]:page["offset"] + page["limit"]]

    return app
