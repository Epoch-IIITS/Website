import unittest
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = ""


def create_app():
    app = FastAPI()
    notes = []

    def check_token(x_token: Annotated[str | None, Header()] = None):
        if x_token != "secret":
            raise HTTPException(status_code=401, detail="Bad token")

    @app.post("/notes", status_code=201, dependencies=[Depends(check_token)])
    def create(note: NoteIn):
        record = {"id": len(notes) + 1, **note.model_dump()}
        notes.append(record)
        return record

    @app.get("/notes/{note_id}")
    def read(note_id: int):
        for n in notes:
            if n["id"] == note_id:
                return n
        raise HTTPException(status_code=404, detail="Note not found")

    @app.get("/notes")
    def list_notes():
        return notes

    return app


TOKEN = {"X-Token": "secret"}


class ApiTests(unittest.TestCase):
    make_app = staticmethod(create_app)

    def setUp(self):
        self.client = TestClient(self.make_app())

    def test_list_starts_empty(self):
        self.assertEqual(self.client.get("/notes").json(), [])

    # TODO: add tests for creation status, token, 404, validation, ids and order
