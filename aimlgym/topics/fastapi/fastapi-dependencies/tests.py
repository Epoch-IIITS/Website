"""Tests for FA-13 Dependencies and Dependency Overrides.

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


from fastapi.testclient import TestClient

ADA = {"X-API-Key": "key-ada"}
BOB = {"X-API-Key": "key-bob"}


class TestDependencies(unittest.TestCase):
    def setUp(self):
        self.store = S.NoteStore()
        self.app = S.create_app()
        self.app.dependency_overrides[S.get_store] = lambda: self.store
        self.client = TestClient(self.app)

    def test_store_class(self):
        s = S.NoteStore()
        self.assertEqual(s.add("ada", "x"), {"id": 1, "owner": "ada", "text": "x"})
        s.add("bob", "y")
        self.assertEqual([n["id"] for n in s.for_owner("bob")], [2])

    def test_auth_required(self):
        r = self.client.get("/notes")
        self.assertEqual((r.status_code, r.json()), (401, {"detail": "Invalid API key"}))
        self.assertEqual(r.headers["www-authenticate"], "ApiKey")
        self.assertEqual(self.client.get("/notes", headers={"X-API-Key": "wrong"}).status_code, 401)

    def test_create_and_list_per_user(self):
        r = self.client.post("/notes", json={"text": "hello"}, headers=ADA)
        self.assertEqual((r.status_code, r.json()), (201, {"id": 1, "owner": "ada", "text": "hello"}))
        self.client.post("/notes", json={"text": "bob's"}, headers=BOB)
        self.assertEqual([n["text"] for n in self.client.get("/notes", headers=ADA).json()], ["hello"])
        self.assertEqual(self.client.post("/notes", json={"text": ""}, headers=ADA).status_code, 422)

    def test_pagination(self):
        for i in range(5):
            self.client.post("/notes", json={"text": f"n{i}"}, headers=ADA)
        r = self.client.get("/notes", params={"limit": 2, "offset": 1}, headers=ADA)
        self.assertEqual([n["text"] for n in r.json()], ["n1", "n2"])
        self.assertEqual(self.client.get("/notes", params={"limit": 51}, headers=ADA).status_code, 422)

    def test_override_isolates_global_store(self):
        self.client.post("/notes", json={"text": "kept local"}, headers=ADA)
        self.assertEqual(S.STORE.for_owner("ada"), [])
        self.assertEqual(len(self.store.notes), 1)

    def test_override_user(self):
        self.app.dependency_overrides[S.current_user] = lambda: "tester"
        r = self.client.post("/notes", json={"text": "no key needed"})
        self.assertEqual(r.json()["owner"], "tester")

    def test_yield_cleanup(self):
        S.EVENTS.clear()
        self.client.get("/notes", headers=ADA)
        self.assertEqual(S.EVENTS, ["open", "list", "close"])


if __name__ == "__main__":
    unittest.main()
