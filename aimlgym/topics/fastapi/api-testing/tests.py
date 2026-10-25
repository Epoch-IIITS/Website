"""Tests for FA-15 Testing an API.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field


def build_app(create_status=201, check_token=True, missing_404=True, min_title=1,
              unique_ids=True, newest_first=False):
    class NoteIn(BaseModel):
        title: str = Field(min_length=min_title, max_length=100)
        body: str = ""

    app = FastAPI()
    notes = []

    def token(x_token: Annotated[str | None, Header()] = None):
        if check_token and x_token != "secret":
            raise HTTPException(status_code=401, detail="Bad token")

    @app.post("/notes", status_code=create_status, dependencies=[Depends(token)])
    def create(note: NoteIn):
        record = {"id": len(notes) + 1 if unique_ids else 1, **note.model_dump()}
        notes.append(record)
        return record

    @app.get("/notes/{note_id}")
    def read(note_id: int):
        for n in notes:
            if n["id"] == note_id:
                return n
        if missing_404:
            raise HTTPException(status_code=404, detail="Note not found")
        return None

    @app.get("/notes")
    def list_notes():
        return list(reversed(notes)) if newest_first else notes

    return app


def run_learner_tests(**flags):
    probe = type("Probe", (S.ApiTests,), {"make_app": staticmethod(lambda: build_app(**flags))})
    result = unittest.TestResult()
    unittest.defaultTestLoader.loadTestsFromTestCase(probe).run(result)
    return result


class TestYourApiTests(unittest.TestCase):
    def test_at_least_six_tests(self):
        self.assertGreaterEqual(len(unittest.defaultTestLoader.getTestCaseNames(S.ApiTests)), 6)

    def test_pass_on_correct_app(self):
        result = run_learner_tests()
        self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_catches_wrong_create_status(self):
        self.assertFalse(run_learner_tests(create_status=200).wasSuccessful())

    def test_catches_missing_token_check(self):
        self.assertFalse(run_learner_tests(check_token=False).wasSuccessful())

    def test_catches_missing_404(self):
        self.assertFalse(run_learner_tests(missing_404=False).wasSuccessful())

    def test_catches_empty_title(self):
        self.assertFalse(run_learner_tests(min_title=0).wasSuccessful())

    def test_catches_duplicate_ids(self):
        self.assertFalse(run_learner_tests(unique_ids=False).wasSuccessful())

    def test_catches_wrong_order(self):
        self.assertFalse(run_learner_tests(newest_first=True).wasSuccessful())


if __name__ == "__main__":
    unittest.main()
