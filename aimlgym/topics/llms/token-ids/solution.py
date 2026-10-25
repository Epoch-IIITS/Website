r"""Reference solution for LM-01 Vocabularies and Token IDs.

Special tokens are inserted first so their IDs never change; frequency-then-alphabetical sorting
makes the remaining IDs reproducible. Encoding falls back to `<unk>`, decoding uses the inverted
mapping, and padding builds the ID matrix and its mask in the same pass.
"""
from collections import Counter

SPECIALS = ["<pad>", "<unk>", "<bos>", "<eos>"]


def build_vocab(texts, min_count=1):
    vocab = {tok: i for i, tok in enumerate(SPECIALS)}
    counts = Counter(tok for t in texts for tok in t.lower().split())
    for tok, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if c >= min_count and tok not in vocab:
            vocab[tok] = len(vocab)
    return vocab


def encode(text, vocab, add_special=True):
    ids = [vocab.get(tok, vocab["<unk>"]) for tok in text.lower().split()]
    if add_special:
        ids = [vocab["<bos>"]] + ids + [vocab["<eos>"]]
    return ids


def decode(ids, vocab, skip_special=True):
    inverse = {i: t for t, i in vocab.items()}
    toks = [inverse[i] for i in ids]
    if skip_special:
        toks = [t for t in toks if t not in SPECIALS]
    return " ".join(toks)


def pad_batch(seqs, pad_id=0):
    longest = max((len(s) for s in seqs), default=0)
    padded = [list(s) + [pad_id] * (longest - len(s)) for s in seqs]
    mask = [[1] * len(s) + [0] * (longest - len(s)) for s in seqs]
    return padded, mask
