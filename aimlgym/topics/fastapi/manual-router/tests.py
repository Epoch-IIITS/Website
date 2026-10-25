"""Tests for FA-05 A Router by Hand.

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


def make_router():
    r = S.Router()

    @r.route("GET", "/items/{item_id:int}")
    def get_item(item_id, query):
        return {"item_id": item_id, "q": query.get("q")}

    @r.route("delete", "/items/{item_id:int}")
    def delete_item(item_id, query):
        return 204, {}

    @r.route("GET", "/users/me")
    def me(query):
        return {"user": "current"}

    @r.route("GET", "/users/{name}")
    def user(name, query):
        return {"user": name}

    r.add("POST", "/items", lambda query: (201, {"created": True}))
    return r


class TestRouter(unittest.TestCase):
    def test_typed_param_and_query(self):
        self.assertEqual(make_router().dispatch("GET", "/items/42", {"q": "x"}), (200, {}, {"item_id": 42, "q": "x"}))

    def test_status_tuple(self):
        self.assertEqual(make_router().dispatch("POST", "/items"), (201, {}, {"created": True}))
        self.assertEqual(make_router().dispatch("DELETE", "/items/1"), (204, {}, {}))

    def test_404(self):
        r = make_router()
        for path in ("/nothing", "/items/1/extra", "/"):
            self.assertEqual(r.dispatch("GET", path), (404, {}, {"detail": "Not Found"}))

    def test_405_allow(self):
        self.assertEqual(make_router().dispatch("PUT", "/items/3"),
                         (405, {"allow": "DELETE, GET"}, {"detail": "Method Not Allowed"}))
        self.assertEqual(make_router().dispatch("GET", "/items")[1], {"allow": "POST"})

    def test_422(self):
        self.assertEqual(make_router().dispatch("GET", "/items/abc"),
                         (422, {}, {"detail": [{"loc": ["path", "item_id"], "msg": "value is not a valid integer"}]}))

    def test_order_and_str_param(self):
        r = make_router()
        self.assertEqual(r.dispatch("GET", "/users/me")[2], {"user": "current"})
        self.assertEqual(r.dispatch("get", "/users/ada")[2], {"user": "ada"})

    def test_decorator_returns_function(self):
        r = S.Router()

        @r.route("GET", "/ping")
        def ping(query):
            return {"pong": True}
        self.assertEqual(ping(query={}), {"pong": True})
        self.assertEqual(len(r.routes), 1)


if __name__ == "__main__":
    unittest.main()
