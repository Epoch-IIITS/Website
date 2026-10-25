"""Tests for FA-06 async and await with asyncio.

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


class TestAsyncio(unittest.TestCase):
    def test_sequential(self):
        log = []
        self.assertEqual(S.run_in_order(log), ["a", "b"])
        self.assertEqual(log, ["a1", "a2", "b1", "b2"])

    def test_concurrent(self):
        log = []
        self.assertEqual(S.run_together(log), ["a", "b"])
        self.assertEqual(log, ["a1", "b1", "a2", "b2"])

    def test_gather_keeps_input_order(self):
        self.assertEqual(S.gather_in_order([3, 0, 2, 1]), [30, 0, 20, 10])
        self.assertEqual(S.gather_in_order([]), [])

    def test_limited(self):
        state = {"active": 0, "peak": 0}

        def make(i):
            async def job():
                state["active"] += 1
                state["peak"] = max(state["peak"], state["active"])
                await asyncio.sleep(0)
                await asyncio.sleep(0)
                state["active"] -= 1
                return i * i
            return job
        self.assertEqual(S.limited([make(i) for i in range(6)], 2), [0, 1, 4, 9, 16, 25])
        self.assertEqual(state["peak"], 2)

    def test_limited_unbounded(self):
        state = {"active": 0, "peak": 0}

        def make():
            async def job():
                state["active"] += 1
                state["peak"] = max(state["peak"], state["active"])
                await asyncio.sleep(0)
                state["active"] -= 1
                return True
            return job
        S.limited([make() for _ in range(5)], 10)
        self.assertEqual(state["peak"], 5)

    def test_timeout(self):
        async def never():
            await asyncio.Event().wait()

        async def quick():
            return 42
        self.assertEqual(S.with_timeout(never(), 0.01), ("timeout", None))
        self.assertEqual(S.with_timeout(quick(), 1.0), ("ok", 42))


if __name__ == "__main__":
    unittest.main()
