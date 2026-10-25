"""Tests for FA-08 First FastAPI Routes.

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


class TestFirstRoutes(unittest.TestCase):
    def test_root_and_health(self):
        self.assertEqual(client.get("/").json(), {"message": "Hello, Epoch Learn"})
        self.assertEqual(client.get("/health").json(), {"status": "ok"})

    def test_typed_path_param(self):
        r = client.get("/items/21")
        self.assertEqual((r.status_code, r.json()), (200, {"item_id": 21, "double": 42}))

    def test_validation_422(self):
        r = client.get("/items/abc")
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json()["detail"][0]["loc"], ["path", "item_id"])

    def test_404_and_405(self):
        self.assertEqual(client.get("/nothing").status_code, 404)
        self.assertEqual(client.post("/items/1").status_code, 405)
        self.assertEqual(client.delete("/items/5").json(), {"deleted": 5})

    def test_route_order(self):
        self.assertEqual(client.get("/users/me").json(), {"user": "current"})
        self.assertEqual(client.get("/users/ada").json(), {"user": "ada"})

    def test_route_table_and_openapi(self):
        self.assertEqual(S.route_table(S.app), [
            ("DELETE", "/items/{item_id}"), ("GET", "/"), ("GET", "/health"),
            ("GET", "/items/{item_id}"), ("GET", "/users/me"), ("GET", "/users/{name}")])
        self.assertEqual(S.app.openapi()["info"]["title"], "Epoch Learn API")
        self.assertIn("/items/{item_id}", S.app.openapi()["paths"])


class MiniRouter:
    def __init__(self):
        self.routes = []

    def add(self, method, pattern, handler):
        self.routes.append((method, pattern.strip("/").split("/"), handler))

    def dispatch(self, method, path):
        parts = path.strip("/").split("/")
        found = []
        for m, segs, h in self.routes:
            if len(segs) == len(parts) and all(s.startswith("{") or s == p for s, p in zip(segs, parts)):
                found.append((m, segs, h))
        if not found:
            return 404, None
        chosen = [(segs, h) for m, segs, h in found if m == method]
        if not chosen:
            return 405, None
        segs, h = chosen[0]
        kwargs = {}
        for s, p in zip(segs, parts):
            if s.startswith("{"):
                name, _, conv = s[1:-1].partition(":")
                if conv == "int":
                    if not p.lstrip("-").isdigit():
                        return 422, None
                    p = int(p)
                kwargs[name] = p
        return 200, h(**kwargs)


def manual_app():
    r = MiniRouter()
    r.add("GET", "/", lambda: {"message": "Hello, Epoch Learn"})
    r.add("GET", "/health", lambda: {"status": "ok"})
    r.add("GET", "/users/me", lambda: {"user": "current"})
    r.add("GET", "/users/{name}", lambda name: {"user": name})
    r.add("GET", "/items/{item_id:int}", lambda item_id: {"item_id": item_id, "double": 2 * item_id})
    r.add("DELETE", "/items/{item_id:int}", lambda item_id: {"deleted": item_id})
    return r


class TestAgainstManualRouter(unittest.TestCase):
    def test_same_behaviour(self):
        manual = manual_app()
        for method, path in [("GET", "/"), ("GET", "/users/me"), ("GET", "/users/bo"), ("GET", "/items/7"),
                             ("DELETE", "/items/7"), ("GET", "/items/x"), ("PUT", "/items/7"), ("GET", "/missing")]:
            status, body = manual.dispatch(method, path)
            r = client.request(method, path)
            self.assertEqual(r.status_code, status, (method, path))
            if status == 200:
                self.assertEqual(r.json(), body)


if __name__ == "__main__":
    unittest.main()
