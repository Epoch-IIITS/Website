"""Tests for FA-11 Handling Errors in FastAPI.

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


class TestErrors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(S.create_app())

    def test_read_ok_and_404(self):
        self.assertEqual(self.client.get("/items/1").json(), {"id": 1, "name": "pen", "stock": 3})
        r = self.client.get("/items/9")
        self.assertEqual((r.status_code, r.json(), r.headers["x-error"]), (404, {"detail": "Item not found"}, "missing"))

    def test_buy_reduces_stock(self):
        self.assertEqual(self.client.post("/items/1/buy", params={"qty": 2}).json(), {"item": "pen", "remaining": 1})
        self.assertEqual(self.client.get("/items/1").json()["stock"], 1)
        self.assertEqual(self.client.post("/items/1/buy").json(), {"item": "pen", "remaining": 0})

    def test_out_of_stock_409(self):
        r = self.client.post("/items/2/buy")
        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json(), {"error": "out_of_stock", "item": "ink", "requested": 1, "available": 0})
        r = self.client.post("/items/1/buy", params={"qty": 5})
        self.assertEqual(r.json()["available"], 3)
        self.assertEqual(self.client.get("/items/1").json()["stock"], 3)

    def test_buy_unknown_404(self):
        self.assertEqual(self.client.post("/items/7/buy").status_code, 404)

    def test_validation_format(self):
        r = self.client.post("/items/abc/buy", params={"qty": 0})
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json(), {"error": "validation_error", "fields": ["path.item_id", "query.qty"]})

    def test_fresh_state_per_app(self):
        self.client.post("/items/1/buy", params={"qty": 3})
        fresh = TestClient(S.create_app())
        self.assertEqual(fresh.get("/items/1").json()["stock"], 3)

    def test_exception_is_plain_python(self):
        e = S.OutOfStock("pen", 5, 3)
        self.assertEqual((e.item, e.requested, e.available), ("pen", 5, 3))
        self.assertIsInstance(e, Exception)


if __name__ == "__main__":
    unittest.main()
