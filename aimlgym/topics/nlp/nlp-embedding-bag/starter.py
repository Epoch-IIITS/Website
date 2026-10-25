from collections import Counter

import torch
from torch import nn


def build_vocab(texts, min_count=1):
    # TODO
    pass


def encode(texts, vocab):
    # TODO
    pass


class BagClassifier(nn.Module):
    def __init__(self, vocab_size, dim, n_classes):
        super().__init__()
        # TODO

    def forward(self, ids, offsets):
        # TODO
        pass


def train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0):
    # TODO
    pass
