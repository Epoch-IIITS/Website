"""Tests for FA-09 Query and Path Parameters with Validation.

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

client = TestClient(S.app)


def ids(resp):
    return [b["id"] for b in resp.json()["items"]]


class TestParams(unittest.TestCase):
    def test_defaults(self):
        r = client.get("/books")
        self.assertEqual((r.json()["count"], ids(r)), (6, [2, 6, 1]))

    def test_filter_sort_page(self):
        r = client.get("/books", params={"q": "DEEP", "order": "desc"})
        self.assertEqual((r.json()["count"], ids(r)), (2, [5, 1]))
        r = client.get("/books", params={"limit": 2, "offset": 2})
        self.assertEqual(ids(r), [1, 3])

    def test_limits_validated(self):
        for params, field in [({"limit": 9}, "limit"), ({"limit": 0}, "limit"), ({"offset": -1}, "offset"),
                              ({"q": "x"}, "q"), ({"order": "random"}, "order")]:
            r = client.get("/books", params=params)
            self.assertEqual(r.status_code, 422, params)
            self.assertEqual(r.json()["detail"][0]["loc"], ["query", field])

    def test_by_year(self):
        self.assertEqual(client.get("/books/by-year/2016").json(), ["Deep Learning"])
        self.assertEqual(client.get("/books/by-year/2000").json(), [])
        self.assertEqual(client.get("/books/by-year/1800").status_code, 422)

    def test_tagged(self):
        self.assertEqual(client.get("/books/tagged", params=[("tag", "ml"), ("tag", "dl")]).json(), [1, 5])
        self.assertEqual(client.get("/books/tagged", params={"tag": "stats"}).json(), [2, 6])
        self.assertEqual(client.get("/books/tagged").json(), [1, 2, 3, 4, 5, 6])

    def test_documented_in_openapi(self):
        params = {p["name"]: p for p in S.app.openapi()["paths"]["/books"]["get"]["parameters"]}
        self.assertEqual(params["limit"]["schema"]["maximum"], 5)
        self.assertEqual(sorted(params), ["limit", "offset", "order", "q"])


if __name__ == "__main__":
    unittest.main()
