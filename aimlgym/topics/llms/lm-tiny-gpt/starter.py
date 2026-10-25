import torch
import torch.nn.functional as F
from torch import nn


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, context, d_model=32, n_heads=2, n_layers=1):
        super().__init__()
        # TODO

    def forward(self, idx):
        # TODO
        pass


def train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0):
    # TODO
    pass


def generate(model, stoi, itos, prompt, n_new):
    # TODO
    pass
