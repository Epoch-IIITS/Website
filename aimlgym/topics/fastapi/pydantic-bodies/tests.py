"""Tests for FA-10 Request Bodies with Pydantic.

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
from pydantic import ValidationError

client = TestClient(S.app)


class TestPydanticBodies(unittest.TestCase):
    def test_parse_and_defaults(self):
        item = S.parse_item({"name": "  pen ", "price": 2})
        self.assertEqual(item.model_dump(), {"name": "pen", "price": 2.0, "tags": [], "quantity": 0})

    def test_errors_listed(self):
        with self.assertRaises(ValidationError) as ctx:
            S.parse_item({"name": " ", "price": "3", "colour": "red"})
        self.assertEqual(sorted(e["loc"] for e in ctx.exception.errors()), [("colour",), ("name",), ("price",)])

    def test_strict_types(self):
        for bad in ({"name": "a", "price": True}, {"name": "a", "price": 1, "quantity": 1.5},
                    {"name": "a", "price": 1, "tags": ["x", 3]}, {"name": "a" * 51, "price": 1}):
            with self.assertRaises(ValidationError, msg=bad):
                S.parse_item(bad)

    def test_post_ok(self):
        r = client.post("/items", json={"name": "ink", "price": 1.5, "quantity": 4, "tags": ["blue"]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"item": {"name": "ink", "price": 1.5, "tags": ["blue"], "quantity": 4}, "total": 6.0})

    def test_post_422(self):
        r = client.post("/items", json={"price": -1})
        self.assertEqual(r.status_code, 422)
        self.assertEqual(sorted(tuple(e["loc"]) for e in r.json()["detail"]), [("body", "name"), ("body", "price")])

    def test_schema(self):
        schema = S.Item.model_json_schema()
        self.assertEqual(schema["required"], ["name", "price"])
        self.assertFalse(schema["additionalProperties"])


def manual_ok(data):
    if not isinstance(data, dict) or set(data) - {"name", "price", "tags", "quantity"}:
        return False
    name, price = data.get("name"), data.get("price")
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 50:
        return False
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return False
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        return False
    q = data.get("quantity", 0)
    return isinstance(q, int) and not isinstance(q, bool) and q >= 0


def pydantic_ok(data):
    try:
        S.parse_item(data)
        return True
    except ValidationError:
        return False


class TestAgainstManualValidator(unittest.TestCase):
    def test_same_decisions(self):
        payloads = [{"name": "a", "price": 0}, {"name": " a ", "price": 2.5, "tags": []}, {"name": "", "price": 1},
                    {"name": "a", "price": -0.1}, {"name": "a", "price": "1"}, {"name": "a", "price": False},
                    {"name": "a", "price": 1, "quantity": -1}, {"name": "a", "price": 1, "quantity": 2},
                    {"name": "a", "price": 1, "extra": None}, {"price": 1}, {"name": 3, "price": 1},
                    {"name": "a", "price": 1, "tags": "ml"}]
        for p in payloads:
            self.assertEqual(pydantic_ok(p), manual_ok(p), p)


if __name__ == "__main__":
    unittest.main()
