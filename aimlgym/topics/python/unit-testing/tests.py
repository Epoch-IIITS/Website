"""Tests for PY-27 Writing Unit Tests.

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


def correct(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def no_lower(text):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def no_collapse(text):
    return "".join(ch if ch.isascii() and ch.isalnum() else "-" for ch in text.lower()).strip("-")


def no_strip(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif not out or out[-1] != "-":
            out.append("-")
    return "".join(out)


def digits_split(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalpha():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def spaces_only(text):
    words = text.lower().split()
    return "-".join(words)


def crashes_on_empty(text):
    if text[0] == "":
        return ""
    return correct(text)


def run_learner_tests(impl):
    probe = type("Probe", (S.SlugifyTests,), {"slugify": staticmethod(impl)})
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(probe)
    result = unittest.TestResult()
    suite.run(result)
    return result


class TestYourTests(unittest.TestCase):
    def test_at_least_five_tests(self):
        names = unittest.defaultTestLoader.getTestCaseNames(S.SlugifyTests)
        self.assertGreaterEqual(len(names), 5)

    def test_pass_on_correct_version(self):
        result = run_learner_tests(correct)
        self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_catches_missing_lowercase(self):
        self.assertFalse(run_learner_tests(no_lower).wasSuccessful())

    def test_catches_missing_collapse(self):
        self.assertFalse(run_learner_tests(no_collapse).wasSuccessful())

    def test_catches_missing_strip(self):
        self.assertFalse(run_learner_tests(no_strip).wasSuccessful())

    def test_catches_digit_bug(self):
        self.assertFalse(run_learner_tests(digits_split).wasSuccessful())

    def test_catches_punctuation_bug(self):
        self.assertFalse(run_learner_tests(spaces_only).wasSuccessful())

    def test_catches_empty_crash(self):
        self.assertFalse(run_learner_tests(crashes_on_empty).wasSuccessful())


if __name__ == "__main__":
    unittest.main()
