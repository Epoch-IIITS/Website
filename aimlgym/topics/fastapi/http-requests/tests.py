"""Tests for FA-01 Anatomy of an HTTP Request.

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


RAW = ('POST /items?debug=1 HTTP/1.1\r\nHost: api.example.com\r\nContent-Type: application/json\r\n'
       'Content-Length: 15\r\n\r\n{"name": "pen"}')


class TestHttpRequest(unittest.TestCase):
    def test_parse(self):
        r = S.parse_request(RAW)
        self.assertEqual((r["method"], r["target"], r["version"]), ("POST", "/items?debug=1", "HTTP/1.1"))
        self.assertEqual(r["headers"], {"host": "api.example.com", "content-type": "application/json",
                                        "content-length": "15"})
        self.assertEqual(r["body"], '{"name": "pen"}')

    def test_header_values_with_colons(self):
        r = S.parse_request("GET / HTTP/1.1\r\nReferer:  http://x.org:8080/a \r\n\r\n")
        self.assertEqual(r["headers"]["referer"], "http://x.org:8080/a")
        self.assertEqual(r["body"], "")

    def test_rejects_malformed(self):
        bad = ["GET / HTTP/1.1\r\nHost: x\r\n",
               "GET /  HTTP/1.1\r\n\r\n",
               "get / HTTP/1.1\r\n\r\n",
               "GET / HTTP/2\r\n\r\n",
               "GET / HTTP/1.1\r\nNoColonHere\r\n\r\n",
               "POST / HTTP/1.1\r\nContent-Length: 3\r\n\r\nab"]
        for raw in bad:
            with self.assertRaises(ValueError, msg=raw):
                S.parse_request(raw)

    def test_length_in_bytes(self):
        r = S.parse_request("POST / HTTP/1.1\r\nContent-Length: 6\r\n\r\ncafé!")
        self.assertEqual(r["body"], "café!")

    def test_build_round_trip(self):
        raw = S.build_request("PUT", "/items/3", {"Host": "x", "Content-Type": "text/plain"}, "héllo")
        self.assertEqual(raw, "PUT /items/3 HTTP/1.1\r\nHost: x\r\nContent-Type: text/plain\r\nContent-Length: 6\r\n\r\nhéllo")
        self.assertEqual(S.parse_request(raw)["body"], "héllo")
        self.assertEqual(S.build_request("GET", "/"), "GET / HTTP/1.1\r\n\r\n")

    def test_methods(self):
        self.assertEqual([S.is_safe(m) for m in ("GET", "head", "POST", "DELETE")], [True, True, False, False])
        self.assertEqual([S.is_idempotent(m) for m in ("GET", "PUT", "delete", "POST", "PATCH", "BREW")],
                         [True, True, True, False, False, False])


import http.client
import io


class TestAgainstLibrary(unittest.TestCase):
    def test_headers_match_http_client(self):
        head = RAW.split("\r\n\r\n")[0].split("\r\n", 1)[1] + "\r\n\r\n"
        msg = http.client.parse_headers(io.BytesIO(head.encode()))
        ours = S.parse_request(RAW)["headers"]
        self.assertEqual(ours, {k.lower(): v for k, v in msg.items()})


if __name__ == "__main__":
    unittest.main()
