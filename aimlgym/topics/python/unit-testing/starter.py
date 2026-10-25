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

    # TODO: add tests for case, punctuation runs, leading/trailing separators,
    #       digits and the empty string
