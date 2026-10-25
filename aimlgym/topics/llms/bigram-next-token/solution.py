r"""Reference solution for LM-02 Next-Token Probabilities (Add-k).

Counts for the context are gathered over the full vocabulary, k pseudo-counts are added to each
word, and everything is divided by the adjusted total, which guarantees a proper distribution.
"""
def next_token_dist(bigrams, prev, vocab, k=1.0):
    if k < 0:
        raise ValueError("k must be >= 0")
    counts = {w: bigrams.get((prev, w), 0) for w in vocab}
    total = sum(counts.values())
    denom = total + k * len(vocab)
    if denom == 0:
        raise ValueError("unseen context with k = 0")
    return {w: (c + k) / denom for w, c in counts.items()}
