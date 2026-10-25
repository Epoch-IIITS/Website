"""Tests for ST-17 Welch's t-test with SciPy.

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


class TestCompareMeans(unittest.TestCase):
    def test_symmetric_example(self):
        from scipy import stats
        r = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        self.assertAlmostEqual(r["t"], -2.0)
        self.assertAlmostEqual(r["df"], 8.0)
        self.assertAlmostEqual(r["p_value"], 2 * stats.t(8).sf(2.0), places=12)
        self.assertAlmostEqual(r["mean_diff"], -2.0)
        self.assertFalse(r["reject"])

    def test_one_sided_halves_p(self):
        two = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        less = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less")
        greater = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="greater")
        self.assertAlmostEqual(less["p_value"], two["p_value"] / 2)
        self.assertTrue(less["reject"])
        self.assertAlmostEqual(greater["p_value"], 1 - less["p_value"])

    def test_welch_not_student(self):
        x, y = [10, 12, 14], [1, 2, 3, 4, 5, 6]
        r = S.compare_means(x, y)
        vx, vy = 4 / 3, 3.5 / 6
        self.assertAlmostEqual(r["t"], 8.5 / math.sqrt(vx + vy), places=10)
        self.assertAlmostEqual(r["df"], (vx + vy) ** 2 / (vx ** 2 / 2 + vy ** 2 / 5), places=10)

    def test_clear_difference(self):
        r = S.compare_means([20.1, 19.8, 20.4, 20.0, 19.9], [10.2, 9.9, 10.1, 10.0, 9.8])
        self.assertTrue(r["reject"])
        self.assertLess(r["p_value"], 1e-6)

    def test_plain_types(self):
        r = S.compare_means([1.0, 2.0, 4.0], [2.0, 3.0, 3.5])
        self.assertTrue(all(type(r[k]) is float for k in ("mean_diff", "t", "df", "p_value")))
        self.assertIs(type(r["reject"]), bool)

    def test_invalid_inputs(self):
        for args, kwargs in [(([1], [1, 2]), {}), (([2, 2], [3, 3]), {}),
                             (([1, 2], [3, 4]), {"alternative": "bigger"}), (([1, 2], [3, 5]), {"alpha": 0})]:
            with self.assertRaises(ValueError):
                S.compare_means(*args, **kwargs)


if __name__ == "__main__":
    unittest.main()
