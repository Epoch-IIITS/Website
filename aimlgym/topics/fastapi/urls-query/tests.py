"""Tests for FA-03 URLs, Paths and Query Strings.

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


class TestUrls(unittest.TestCase):
    def test_split_full(self):
        self.assertEqual(S.split_url("https://api.example.com:8443/search?q=deep+learning&tag=ml#top"),
                         {"scheme": "https", "host": "api.example.com", "port": 8443, "path": "/search",
                          "query": "q=deep+learning&tag=ml", "fragment": "top"})

    def test_split_defaults(self):
        u = S.split_url("http://localhost")
        self.assertEqual((u["port"], u["path"], u["query"], u["fragment"]), (80, "/", "", ""))
        self.assertEqual(S.split_url("https://x.org?a=1")["path"], "/")
        with self.assertRaises(ValueError):
            S.split_url("ftp://x.org/file")

    def test_percent_decode(self):
        self.assertEqual(S.percent_decode("caf%C3%A9+au+lait"), "café au lait")
        self.assertEqual(S.percent_decode("a+b", plus_as_space=False), "a+b")
        with self.assertRaises(ValueError):
            S.percent_decode("100%")

    def test_parse_query(self):
        self.assertEqual(S.parse_query("q=deep+learning&tag=ml&tag=ai&empty&&x=a%3Db"),
                         {"q": ["deep learning"], "tag": ["ml", "ai"], "empty": [""], "x": ["a=b"]})
        self.assertEqual(S.parse_query(""), {})

    def test_value_with_equals(self):
        self.assertEqual(S.parse_query("expr=a=b"), {"expr": ["a=b"]})

    def test_build_round_trip(self):
        params = {"q": ["café au lait"], "tag": ["ml", "a&b"], "x": "1/2"}
        qs = S.build_query(params)
        self.assertEqual(qs, "q=caf%C3%A9+au+lait&tag=ml&tag=a%26b&x=1%2F2")
        self.assertEqual(S.parse_query(qs), {"q": ["café au lait"], "tag": ["ml", "a&b"], "x": ["1/2"]})


from urllib.parse import parse_qs, unquote_plus, urlencode, urlsplit


class TestAgainstLibrary(unittest.TestCase):
    def test_split_matches_urlsplit(self):
        url = "https://api.example.com:8443/a/b?x=1#frag"
        ours, theirs = S.split_url(url), urlsplit(url)
        self.assertEqual((ours["host"], ours["port"], ours["path"], ours["query"], ours["fragment"]),
                         (theirs.hostname, theirs.port, theirs.path, theirs.query, theirs.fragment))

    def test_query_matches_parse_qs(self):
        qs = "q=deep+learning&tag=ml&tag=ai&empty=&z=%E2%82%AC"
        self.assertEqual(S.parse_query(qs), parse_qs(qs, keep_blank_values=True))
        self.assertEqual(S.percent_decode("%E2%82%AC+5"), unquote_plus("%E2%82%AC+5"))

    def test_build_matches_urlencode(self):
        params = {"q": ["café au lait"], "n": ["1", "2"]}
        self.assertEqual(S.build_query(params), urlencode(params, doseq=True))


if __name__ == "__main__":
    unittest.main()
