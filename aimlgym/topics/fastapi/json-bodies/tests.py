"""Tests for FA-04 JSON Request Bodies and Validation.

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


import json

JSON = {"content-type": "application/json"}


class TestJsonBodies(unittest.TestCase):
    def test_read_ok_with_charset(self):
        self.assertEqual(S.read_json({"content-type": "Application/JSON; charset=utf-8"}, '{"a": 1}'), (200, {"a": 1}))

    def test_read_415(self):
        self.assertEqual(S.read_json({"content-type": "text/plain"}, "{}")[0], 415)
        self.assertEqual(S.read_json({}, "{}")[0], 415)

    def test_read_400(self):
        self.assertEqual(S.read_json(JSON, "{'a': 1}"), (400, {"detail": "Invalid JSON"}))

    def test_valid_item(self):
        self.assertEqual(S.validate_item({"name": " pen ", "price": 2}), ({"name": "pen", "price": 2, "tags": []}, []))
        item, errs = S.validate_item({"name": "ink", "price": 0.5, "tags": ["blue"]})
        self.assertEqual((item["tags"], errs), (["blue"], []))

    def test_all_errors_reported(self):
        item, errs = S.validate_item({"name": "  ", "price": -1, "tags": ["ok", 3], "zeta": 1, "alpha": 2})
        self.assertIsNone(item)
        self.assertEqual(errs, [
            {"loc": ["body", "name"], "msg": "must be a non-empty string"},
            {"loc": ["body", "price"], "msg": "must be >= 0"},
            {"loc": ["body", "tags"], "msg": "must be a list of strings"},
            {"loc": ["body", "alpha"], "msg": "extra field not allowed"},
            {"loc": ["body", "zeta"], "msg": "extra field not allowed"}])

    def test_required_and_bool(self):
        self.assertEqual(S.validate_item({})[1], [{"loc": ["body", "name"], "msg": "field required"},
                                                  {"loc": ["body", "price"], "msg": "field required"}])
        self.assertEqual(S.validate_item({"name": "x", "price": True})[1], [{"loc": ["body", "price"], "msg": "must be a number"}])
        self.assertEqual(S.validate_item([1, 2]), (None, [{"loc": ["body"], "msg": "must be an object"}]))

    def test_json_response(self):
        status, headers, text = S.json_response(201, {"id": 1, "tags": ["a"]})
        self.assertEqual((status, headers, text), (201, {"content-type": "application/json"}, '{"id":1,"tags":["a"]}'))
        self.assertEqual(json.loads(text), {"id": 1, "tags": ["a"]})


if __name__ == "__main__":
    unittest.main()
