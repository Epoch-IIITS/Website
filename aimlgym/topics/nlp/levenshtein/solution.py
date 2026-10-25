r"""Reference solution for NL-12 Levenshtein Edit Distance.

The table is filled row by row keeping only the previous row. Each cell takes the cheapest of
deletion, insertion and substitution (free when characters match). Suggestions sort
(distance, word) pairs for a deterministic ranking.
"""
def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i]
        for j in range(1, len(b) + 1):
            cur.append(min(prev[j] + 1,
                           cur[j - 1] + 1,
                           prev[j - 1] + (a[i - 1] != b[j - 1])))
        prev = cur
    return prev[-1]


def suggest(word, vocab, max_dist=2):
    scored = sorted((levenshtein(word, w), w) for w in set(vocab))
    return [w for d, w in scored if d <= max_dist]
