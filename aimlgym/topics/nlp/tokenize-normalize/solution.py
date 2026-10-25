r"""Reference solution for NL-02 Tokenize and Normalize.

NFKD splits accented letters into base letters plus combining marks, which are then removed.
Lowercasing finishes normalisation. A compiled regex extracts alphanumeric runs with an optional
apostrophe suffix, so contractions remain one token.
"""
import re
import unicodedata

TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def normalize(text):
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def tokenize(text):
    return TOKEN_RE.findall(normalize(text))
