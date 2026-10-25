"""Tests for DL-08 A Tiny Autograd Engine.

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


def numeric(f, xs, i, h=1e-6):
    up = list(xs); down = list(xs)
    up[i] += h; down[i] -= h
    return (f(*up) - f(*down)) / (2 * h)


class TestAutograd(unittest.TestCase):
    def test_example(self):
        a, b = S.Value(2.0), S.Value(-3.0)
        c = a * b + a
        c.backward()
        self.assertEqual((c.data, a.grad, b.grad), (-4.0, -2.0, 2.0))

    def test_reused_value_accumulates(self):
        a = S.Value(3.0)
        y = a * a + a
        y.backward()
        self.assertAlmostEqual(a.grad, 2 * 3.0 + 1)

    def test_reflected_and_sub(self):
        a = S.Value(4.0)
        y = 2 * a + 1 - a
        z = 10 - a
        self.assertEqual(y.data, 5.0)
        self.assertEqual(z.data, 6.0)
        y.backward()
        self.assertAlmostEqual(a.grad, 1.0)

    def test_pow_and_neg(self):
        a = S.Value(1.5)
        y = -(a ** 3)
        y.backward()
        self.assertAlmostEqual(y.data, -3.375)
        self.assertAlmostEqual(a.grad, -3 * 1.5 ** 2)

    def test_tanh_exp(self):
        a = S.Value(0.3)
        y = a.tanh() * a.exp()
        y.backward()
        f = lambda x: math.tanh(x) * math.exp(x)
        self.assertAlmostEqual(y.data, f(0.3))
        self.assertAlmostEqual(a.grad, numeric(f, [0.3], 0), places=6)

    def test_neuron_matches_numeric(self):
        def f(x1, x2, w1, w2, b):
            return math.tanh(x1 * w1 + x2 * w2 + b) ** 2
        vals = [2.0, -1.0, -0.4, 0.7, 0.1]
        x1, x2, w1, w2, b = [S.Value(v) for v in vals]
        out = (x1 * w1 + x2 * w2 + b).tanh() ** 2
        out.backward()
        for i, node in enumerate([x1, x2, w1, w2, b]):
            self.assertAlmostEqual(node.grad, numeric(f, vals, i), places=6)

    def test_deep_chain_order(self):
        x = S.Value(0.5)
        y = x
        for _ in range(30):
            y = y * 1.1 + 0.01
        y.backward()
        self.assertAlmostEqual(x.grad, 1.1 ** 30, places=6)


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_autograd(self):
        vals = [0.8, -1.2, 0.3]
        a, b, c = [S.Value(v) for v in vals]
        out = ((a * b + c).tanh() * (a ** 2)).exp() - 3 * b
        out.backward()
        ta, tb, tc = [torch.tensor(v, dtype=torch.float64, requires_grad=True) for v in vals]
        tout = (torch.tanh(ta * tb + tc) * ta ** 2).exp() - 3 * tb
        tout.backward()
        self.assertAlmostEqual(out.data, tout.item(), places=10)
        for mine, theirs in zip((a, b, c), (ta, tb, tc)):
            self.assertAlmostEqual(mine.grad, theirs.grad.item(), places=10)


if __name__ == "__main__":
    unittest.main()
