"""Tests for DL-15 Optimisers in torch.optim.

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


import torch


class TestMinimise(unittest.TestCase):
    def test_one_sgd_step(self):
        r = S.minimise("sgd", [0.0, 0.0], 0.01, 1)
        # gradient at (0, 0) is (-6, 20)
        self.assertAlmostEqual(r["point"][0], 0.06, places=6)
        self.assertAlmostEqual(r["point"][1], -0.2, places=6)
        self.assertAlmostEqual(r["losses"][0], 19.0, places=5)

    def test_adam_first_step_is_lr_sized(self):
        r = S.minimise("adam", [0.0, 0.0], 0.1, 1)
        self.assertAlmostEqual(r["point"][0], 0.1, places=5)
        self.assertAlmostEqual(r["point"][1], -0.1, places=5)

    def test_adam_converges(self):
        r = S.minimise("adam", [0.0, 0.0], 0.1, 300)
        self.assertAlmostEqual(r["point"][0], 3.0, delta=0.05)
        self.assertAlmostEqual(r["point"][1], -1.0, delta=0.05)

    def test_momentum_beats_sgd(self):
        sgd = S.minimise("sgd", [0.0, 0.0], 0.005, 100)
        mom = S.minimise("momentum", [0.0, 0.0], 0.005, 100)
        self.assertLess(mom["losses"][-1], sgd["losses"][-1])

    def test_losses_recorded_and_fall(self):
        r = S.minimise("adamw", [0.0, 0.0], 0.1, 50)
        self.assertEqual(len(r["losses"]), 50)
        self.assertLess(r["losses"][-1], r["losses"][0] / 10)
        self.assertTrue(all(type(v) is float for v in r["losses"]))

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            S.minimise("lbfgs-ish", [0.0, 0.0], 0.1, 1)


if __name__ == "__main__":
    unittest.main()
