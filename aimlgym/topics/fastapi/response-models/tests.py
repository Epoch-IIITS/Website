"""Tests for FA-12 Response Models and Status Codes.

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


import hashlib

from fastapi.testclient import TestClient

ADA = {"username": "ada", "email": "ada@x.org", "password": "correct horse"}


class TestResponseModels(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(S.create_app())

    def test_create_201_without_secrets(self):
        r = self.client.post("/users", json=ADA)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json(), {"id": 1, "username": "ada", "email": "ada@x.org"})
        self.assertNotIn("password", r.text)
        self.assertNotIn(hashlib.sha256(b"correct horse").hexdigest(), r.text)

    def test_input_validation(self):
        for bad in ({**ADA, "username": "Ada!"}, {**ADA, "username": "ab"}, {**ADA, "password": "short"},
                    {**ADA, "email": "nope"}):
            self.assertEqual(self.client.post("/users", json=bad).status_code, 422, bad)

    def test_duplicate_409(self):
        self.client.post("/users", json=ADA)
        r = self.client.post("/users", json={**ADA, "email": "other@x.org"})
        self.assertEqual((r.status_code, r.json()), (409, {"detail": "Username taken"}))

    def test_list_and_read(self):
        self.client.post("/users", json=ADA)
        self.client.post("/users", json={**ADA, "username": "bob"})
        self.assertEqual([u["username"] for u in self.client.get("/users").json()], ["ada", "bob"])
        self.assertEqual(self.client.get("/users/2").json()["username"], "bob")
        self.assertNotIn("password_hash", self.client.get("/users").text)
        self.assertEqual(self.client.get("/users/9").status_code, 404)

    def test_delete_204_and_no_reuse(self):
        self.client.post("/users", json=ADA)
        r = self.client.delete("/users/1")
        self.assertEqual((r.status_code, r.content), (204, b""))
        self.assertEqual(self.client.get("/users/1").status_code, 404)
        self.assertEqual(self.client.delete("/users/1").status_code, 404)
        self.assertEqual(self.client.post("/users", json=ADA).json()["id"], 2)

    def test_openapi_response_schema(self):
        app = S.create_app()
        schema = app.openapi()["components"]["schemas"]
        self.assertNotIn("password", schema["UserOut"]["properties"])
        self.assertIn("201", app.openapi()["paths"]["/users"]["post"]["responses"])


if __name__ == "__main__":
    unittest.main()
