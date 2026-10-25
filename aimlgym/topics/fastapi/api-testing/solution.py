r"""Reference solution for FA-15 Testing an API.

Each test targets one promise of the API — status codes, authentication, validation, missing
resources, id assignment and ordering — and builds its own app in `setUp`, so tests are
independent. Because every broken version violates one of those promises, each one fails at
least one test while the correct app passes them all.
"""
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

    def create(self, title="t", body="b"):
        return self.client.post("/notes", json={"title": title, "body": body}, headers=TOKEN)

    def test_list_starts_empty(self):
        self.assertEqual(self.client.get("/notes").json(), [])

    def test_create_returns_201_and_note(self):
        r = self.create("first", "hello")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json(), {"id": 1, "title": "first", "body": "hello"})

    def test_token_required(self):
        r = self.client.post("/notes", json={"title": "t", "body": "b"})
        self.assertEqual(r.status_code, 401)
        r = self.client.post("/notes", json={"title": "t"}, headers={"X-Token": "wrong"})
        self.assertEqual(r.status_code, 401)

    def test_missing_note_404(self):
        self.assertEqual(self.client.get("/notes/99").status_code, 404)

    def test_empty_title_422(self):
        self.assertEqual(self.create(title="").status_code, 422)

    def test_ids_unique_and_readable(self):
        a, b = self.create("a").json(), self.create("b").json()
        self.assertEqual((a["id"], b["id"]), (1, 2))
        self.assertEqual(self.client.get("/notes/2").json()["title"], "b")

    def test_list_in_creation_order(self):
        self.create("old")
        self.create("new")
        self.assertEqual([n["title"] for n in self.client.get("/notes").json()], ["old", "new"])
