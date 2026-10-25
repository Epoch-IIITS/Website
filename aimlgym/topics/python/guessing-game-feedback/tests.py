"""Tests for PY-22 Guessing Game Feedback.

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


class TestGuess(unittest.TestCase):
    def test_win(self):
        self.assertEqual(S.guess_feedback(42, [50, 25, 42, 10]),
                         {"feedback": ["too high", "too low", "correct"], "attempts": 3, "won": True})

    def test_limit(self):
        self.assertEqual(S.guess_feedback(5, [1, 2, 3], max_attempts=2),
                         {"feedback": ["too low", "too low"], "attempts": 2, "won": False})

    def test_first_try(self):
        self.assertEqual(S.guess_feedback(7, [7, 7]),
                         {"feedback": ["correct"], "attempts": 1, "won": True})

    def test_no_guesses(self):
        self.assertEqual(S.guess_feedback(3, []), {"feedback": [], "attempts": 0, "won": False})

    def test_win_on_last_allowed(self):
        r = S.guess_feedback(10, [1, 2, 10], max_attempts=3)
        self.assertTrue(r["won"])
        self.assertEqual(r["attempts"], 3)

    def test_correct_after_limit_ignored(self):
        r = S.guess_feedback(10, [1, 2, 10], max_attempts=2)
        self.assertFalse(r["won"])

    def test_bad_limit(self):
        with self.assertRaises(ValueError):
            S.guess_feedback(1, [1], max_attempts=0)


if __name__ == "__main__":
    unittest.main()
