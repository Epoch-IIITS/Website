r"""Reference solution for PY-16 Unique Words in Order.

Each token is normalised by stripping punctuation from its ends and lowercasing. The set gives
constant-time duplicate checks while the list records first-occurrence order. Empty tokens
(pure punctuation) are skipped by the `if word` condition.
"""
import string


def unique_words(sentence):
    seen = set()
    out = []
    for token in sentence.split():
        word = token.strip(string.punctuation).lower()
        if word and word not in seen:
            seen.add(word)
            out.append(word)
    return out
