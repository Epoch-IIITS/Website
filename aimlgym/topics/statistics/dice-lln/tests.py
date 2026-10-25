"""Tests for ST-10 Dice Simulation and the Law of Large Numbers.

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


import random

def _ref(n, seed):
    rng = random.Random(seed)
    return [int(rng.random() * 6) + 1 + int(rng.random() * 6) + 1 for _ in range(n)]

class TestDice(unittest.TestCase):
    def test_roll_range(self):
        rng = random.Random(3)
        faces = {S.roll(rng) for _ in range(2000)}
        self.assertEqual(faces, {1, 2, 3, 4, 5, 6})

    def test_exact_sequence(self):
        self.assertEqual(S.simulate_two_dice(50, seed=42)["sums"], _ref(50, 42))

    def test_reproducible(self):
        self.assertEqual(S.simulate_two_dice(30, 7), S.simulate_two_dice(30, 7))

    def test_running_mean(self):
        r = S.simulate_two_dice(20, seed=5)
        for i in range(20):
            self.assertAlmostEqual(r["running_mean"][i], sum(r["sums"][:i + 1]) / (i + 1))

    def test_freq_keys_and_total(self):
        r = S.simulate_two_dice(500, seed=9)
        self.assertEqual(set(r["freq"]), set(range(2, 13)))
        self.assertEqual(sum(r["freq"].values()), 500)

    def test_lln(self):
        r = S.simulate_two_dice(100000, seed=1)
        self.assertLess(abs(r["running_mean"][-1] - 7), 0.05)

    def test_seven_most_common(self):
        f = S.simulate_two_dice(60000, seed=2)["freq"]
        self.assertEqual(max(f, key=f.get), 7)

    def test_bad_n(self):
        with self.assertRaises(ValueError):
            S.simulate_two_dice(0, 1)


if __name__ == "__main__":
    unittest.main()
