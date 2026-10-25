r"""Reference solution for NL-06 Character n-grams by Hand.

Markers are added once; each n contributes all windows of that length in order. Jaccard compares
n-gram sets, handling the empty case explicitly.
"""
def char_ngrams(word, n_min=3, n_max=3):
    if n_min < 1 or n_max < n_min:
        raise ValueError("need 1 <= n_min <= n_max")
    s = "<" + word + ">"
    out = []
    for n in range(n_min, n_max + 1):
        out.extend(s[i:i + n] for i in range(len(s) - n + 1))
    return out


def jaccard(a, b, n=3):
    A, B = set(char_ngrams(a, n, n)), set(char_ngrams(b, n, n))
    union = A | B
    return 1.0 if not union else len(A & B) / len(union)
