from collections import Counter

SPECIALS = ["<pad>", "<unk>", "<bos>", "<eos>"]


def build_vocab(texts, min_count=1):
    vocab = {tok: i for i, tok in enumerate(SPECIALS)}
    # TODO: count tokens, sort, append
    return vocab


def encode(text, vocab, add_special=True):
    # TODO
    return []


def decode(ids, vocab, skip_special=True):
    # TODO
    return ""


def pad_batch(seqs, pad_id=0):
    # TODO
    return [], []
