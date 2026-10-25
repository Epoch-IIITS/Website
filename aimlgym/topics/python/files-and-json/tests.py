"""Tests for PY-23 Files, CSV and JSON.

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
import tempfile
from pathlib import Path


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_csv(self, text):
        p = self.dir / "scores.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_write_and_read_lines(self):
        p = self.dir / "notes.txt"
        self.assertEqual(S.write_lines(p, ["alpha", "beta"]), 2)
        self.assertEqual(p.read_text(encoding="utf-8"), "alpha\nbeta\n")
        self.assertEqual(S.read_lines(p), ["alpha", "beta"])

    def test_write_replaces(self):
        p = self.dir / "notes.txt"
        S.write_lines(str(p), ["old", "old"])
        S.write_lines(str(p), ["new"])
        self.assertEqual(S.read_lines(str(p)), ["new"])

    def test_load_scores_csv(self):
        p = self.write_csv('name,score\nada,91\n"Lovelace, Ada",88\n')
        self.assertEqual(S.load_scores_csv(p), [("ada", 91), ("Lovelace, Ada", 88)])

    def test_json_roundtrip(self):
        p = self.dir / "data.json"
        data = {"b": [1, 2], "a": {"x": None, "y": True}}
        S.save_json(p, data)
        self.assertEqual(S.load_json(p), data)
        self.assertEqual(p.read_text(encoding="utf-8"), json.dumps(data, indent=2, sort_keys=True))

    def test_summary(self):
        p = self.write_csv("name,score\nada,90\nbob,95\ncy,95\n")
        out = self.dir / "summary.json"
        expected = {"count": 3, "mean": 93.33, "top": "bob"}
        self.assertEqual(S.summarize_scores(p, out), expected)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")), expected)

    def test_summary_empty(self):
        p = self.write_csv("name,score\n")
        out = self.dir / "summary.json"
        self.assertEqual(S.summarize_scores(p, out), {"count": 0, "mean": None, "top": None})

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            S.read_lines(self.dir / "missing.txt")


if __name__ == "__main__":
    unittest.main()
