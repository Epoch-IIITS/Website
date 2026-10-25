r"""Reference solution for PY-27 Writing Unit Tests.

Each test targets one rule of the specification, so each mutant — which breaks exactly one
rule — fails at least one test, while the correct implementation passes them all. The empty
and punctuation-only inputs cover the edge cases that crash naive implementations.
"""
import unittest


def slugify(text):
    """Return a URL-friendly slug: 'Hello, World!' -> 'hello-world'."""
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


class SlugifyTests(unittest.TestCase):
    slugify = staticmethod(slugify)

    def test_example(self):
        self.assertEqual(self.slugify("Hello World"), "hello-world")

    def test_lowercases(self):
        self.assertEqual(self.slugify("ABC"), "abc")

    def test_punctuation_becomes_dash(self):
        self.assertEqual(self.slugify("a!b"), "a-b")

    def test_runs_collapse(self):
        self.assertEqual(self.slugify("a,  b"), "a-b")

    def test_no_leading_or_trailing_dash(self):
        self.assertEqual(self.slugify("  --a--  "), "a")

    def test_digits_kept(self):
        self.assertEqual(self.slugify("R2D2 v10"), "r2d2-v10")

    def test_empty(self):
        self.assertEqual(self.slugify(""), "")
        self.assertEqual(self.slugify("!!!"), "")
