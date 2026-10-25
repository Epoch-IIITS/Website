"""Tests for FA-07 A Minimal ASGI Application.

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


import asyncio
import json


def run_raw(scope, chunks):
    """Independent harness: feeds the body in several chunks and records events."""
    events, queue = [], list(chunks)

    async def receive():
        body = queue.pop(0) if queue else b""
        return {"type": "http.request", "body": body, "more_body": bool(queue)}

    async def send(event):
        events.append(event)
    asyncio.run(S.app(scope, receive, send))
    return events


def scope(method, path, qs=b""):
    return {"type": "http", "method": method, "path": path, "query_string": qs, "headers": []}


class TestAsgi(unittest.TestCase):
    def test_root_events(self):
        events = run_raw(scope("GET", "/"), [b""])
        self.assertEqual([e["type"] for e in events], ["http.response.start", "http.response.body"])
        self.assertEqual(events[0]["status"], 200)
        self.assertIn((b"content-type", b"application/json"), events[0]["headers"])
        self.assertEqual(events[1]["body"], b'{"message":"hello"}')

    def test_echo_query(self):
        events = run_raw(scope("GET", "/echo", b"name=ada&n=3"), [b""])
        self.assertEqual(json.loads(events[1]["body"]), {"params": {"name": "ada", "n": "3"}})

    def test_sum_chunked(self):
        events = run_raw(scope("POST", "/sum"), [b'{"numbers": [1,', b' 2, 3.5]}'])
        self.assertEqual((events[0]["status"], json.loads(events[1]["body"])), (200, {"sum": 6.5}))

    def test_errors(self):
        self.assertEqual(run_raw(scope("GET", "/nope"), [b""])[0]["status"], 404)
        self.assertEqual(run_raw(scope("GET", "/sum"), [b""])[0]["status"], 405)
        for body in (b"not json", b'{"nums": []}', b'{"numbers": 5}', b'{"numbers": ["a", 1]}'):
            events = run_raw(scope("POST", "/sum"), [body])
            self.assertEqual((events[0]["status"], events[1]["body"]), (400, b'{"detail":"bad body"}'), body)

    def test_call_asgi_client(self):
        self.assertEqual(S.call_asgi(S.app, "GET", "/"), (200, {"content-type": "application/json"}, b'{"message":"hello"}'))
        status, _, body = S.call_asgi(S.app, "POST", "/sum", body=b'{"numbers": [2, 2]}')
        self.assertEqual((status, body), (200, b'{"sum":4}'))

    def test_call_asgi_with_other_app(self):
        async def teapot(scope, receive, send):
            await send({"type": "http.response.start", "status": 418, "headers": [(b"x-kind", b"tea")]})
            await send({"type": "http.response.body", "body": b"short and "})
            await send({"type": "http.response.body", "body": b"stout"})
        self.assertEqual(S.call_asgi(teapot, "GET", "/"), (418, {"x-kind": "tea"}, b"short and stout"))


if __name__ == "__main__":
    unittest.main()
