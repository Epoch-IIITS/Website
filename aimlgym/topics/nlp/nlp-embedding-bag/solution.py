r"""Reference solution for NL-19 Word Embeddings in PyTorch.

The vocabulary reserves id 0 for unknown words so any text can be encoded. Concatenating ids and
recording where each text starts lets `EmbeddingBag` average variable-length texts without padding.
The classifier learns the embeddings and the output layer together.
"""
from collections import Counter

import torch
from torch import nn


def build_vocab(texts, min_count=1):
    counts = Counter(w for text in texts for w in text.lower().split())
    words = sorted((w for w, c in counts.items() if c >= min_count), key=lambda w: (-counts[w], w))
    vocab = {"<unk>": 0}
    for i, w in enumerate(words, 1):
        vocab[w] = i
    return vocab


def encode(texts, vocab):
    ids, offsets = [], []
    for text in texts:
        offsets.append(len(ids))
        ids.extend(vocab.get(w, 0) for w in text.lower().split())
    return torch.tensor(ids, dtype=torch.long), torch.tensor(offsets, dtype=torch.long)


class BagClassifier(nn.Module):
    def __init__(self, vocab_size, dim, n_classes):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, dim, mode="mean")
        self.fc = nn.Linear(dim, n_classes)

    def forward(self, ids, offsets):
        return self.fc(self.embedding(ids, offsets))


def train_bag(texts, labels, dim=16, epochs=30, lr=0.05, seed=0):
    vocab = build_vocab(texts)
    ids, offsets = encode(texts, vocab)
    y = torch.as_tensor(labels, dtype=torch.long)
    torch.manual_seed(seed)
    model = BagClassifier(len(vocab), dim, int(y.max()) + 1)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        loss = loss_fn(model(ids, offsets), y)
        loss.backward()
        opt.step()
        history.append(loss.item())
    model.eval()
    return model, vocab, history
