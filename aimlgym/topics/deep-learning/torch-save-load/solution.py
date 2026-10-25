r"""Reference solution for DL-26 Saving, Loading and Reproducibility.

Only the state dict is written, so the file contains tensors keyed by parameter name. Loading
rebuilds the architecture, copies the tensors in (checking every name and shape) and switches to
evaluation. Seeding all three generators makes any later random choice repeatable.
"""
import random

import numpy as np
import torch
from torch import nn


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def save_model(model, path):
    torch.save(model.state_dict(), path)


def load_model(path, n_in, n_hidden, n_out):
    model = MLP(n_in, n_hidden, n_out)
    model.load_state_dict(torch.load(path, weights_only=True))
    model.eval()
    return model
