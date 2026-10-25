r"""Reference solution for LM-06 Byte-Pair Encoding Merges.

Each round counts frequency-weighted adjacent pairs, picks the most frequent (smallest on ties),
records it and rewrites every word with a left-to-right, non-overlapping merge. Applying BPE replays
the merges in learned order on a new word.
"""
from collections import Counter


def _merge(symbols, pair):
    a, b = pair
    out, i = [], 0
    while i < len(symbols):
        if i + 1 < len(symbols) and symbols[i] == a and symbols[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def learn_bpe(word_counts, num_merges):
    vocab = {tuple(w) + ("</w>",): c for w, c in word_counts.items()}
    merges = []
    for _ in range(num_merges):
        pairs = Counter()
        for sym, c in vocab.items():
            for i in range(len(sym) - 1):
                pairs[(sym[i], sym[i + 1])] += c
        if not pairs:
            break
        best = min(pairs, key=lambda p: (-pairs[p], p))
        merges.append(best)
        new_vocab = Counter()
        for sym, c in vocab.items():
            new_vocab[_merge(sym, best)] += c
        vocab = dict(new_vocab)
    return merges


def apply_bpe(word, merges):
    sym = tuple(word) + ("</w>",)
    for pair in merges:
        sym = _merge(sym, pair)
    return list(sym)
