"""Tests for AG-16 Orchestrator and Workers in LangGraph.

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


def words(section):
    return f"{len(section.split())} words"


def state(document):
    return {"document": document, "sections": [], "results": [], "report": ""}


class TestOrchestrator(unittest.TestCase):
    def test_worked_example(self):
        app = S.build_report_graph(words)
        out = app.invoke(state("intro text\n\nmethods text\n\nresults text"))
        self.assertEqual(out["report"], "1: 2 words | 2: 2 words | 3: 2 words")

    def test_order_restored(self):
        app = S.build_report_graph(lambda s: s.upper())
        out = app.invoke(state("c\n\nb b\n\na a a"))
        self.assertEqual(out["report"], "1: C | 2: B B | 3: A A A")

    def test_one_worker_per_section(self):
        calls = []
        app = S.build_report_graph(lambda s: calls.append(s) or "ok")
        out = app.invoke(state("one\n\n\n\ntwo\n\n   \n\nthree"))
        self.assertEqual(sorted(calls), ["one", "three", "two"])
        self.assertEqual(out["sections"], ["one", "two", "three"])

    def test_results_collected(self):
        out = S.build_report_graph(len).invoke(state("ab\n\ncde"))
        self.assertEqual(sorted(out["results"]), [(0, 2), (1, 3)])

    def test_single_section(self):
        out = S.build_report_graph(words).invoke(state("just one section here"))
        self.assertEqual(out["report"], "1: 4 words")

    def test_nodes(self):
        nodes = set(S.build_report_graph(words).get_graph().nodes)
        self.assertTrue({"orchestrator", "worker", "synthesise"} <= nodes)


if __name__ == "__main__":
    unittest.main()
