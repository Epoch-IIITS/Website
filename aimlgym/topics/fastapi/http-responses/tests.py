"""Tests for FA-02 HTTP Responses and Status Codes.

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


class TestHttpResponses(unittest.TestCase):
    def test_classes(self):
        self.assertEqual([S.status_class(c) for c in (101, 200, 204, 301, 404, 422, 503)],
                         ["informational", "success", "success", "redirection", "client error",
                          "client error", "server error"])
        for bad in (99, 600):
            with self.assertRaises(ValueError):
                S.status_class(bad)

    def test_reasons(self):
        self.assertEqual(S.reason(201), "Created")
        self.assertEqual(S.reason(422), "Unprocessable Content")
        self.assertEqual(S.reason(415), "Unsupported Media Type")
        self.assertEqual(S.reason(299), "Unknown")

    def test_build(self):
        self.assertEqual(S.build_response(404, "not found"),
                         "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 9\r\n\r\nnot found")

    def test_build_bytes_and_type(self):
        raw = S.build_response(201, '{"name": "café"}', "application/json")
        self.assertIn("Content-Length: 17\r\n", raw)
        self.assertTrue(raw.startswith("HTTP/1.1 201 Created\r\nContent-Type: application/json\r\n"))

    def test_no_content(self):
        self.assertEqual(S.build_response(204), "HTTP/1.1 204 No Content\r\n\r\n")
        with self.assertRaises(ValueError):
            S.build_response(204, "oops")

    def test_parse_round_trip(self):
        r = S.parse_response(S.build_response(500, "boom"))
        self.assertEqual(r, {"status": 500, "reason": "Internal Server Error",
                             "headers": {"content-type": "text/plain; charset=utf-8", "content-length": "4"},
                             "body": "boom"})


from http import HTTPStatus


class TestAgainstLibrary(unittest.TestCase):
    def test_reasons_match_httpstatus(self):
        for code in S.REASONS:
            self.assertEqual(S.reason(code), HTTPStatus(code).phrase, code)


if __name__ == "__main__":
    unittest.main()
