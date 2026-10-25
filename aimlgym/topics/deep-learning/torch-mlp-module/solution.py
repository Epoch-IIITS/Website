r"""Reference solution for DL-06 Models with nn.Module.

Assigning an `nn.Sequential` to an attribute registers all its layers, so `parameters()` finds the
two weight matrices and two bias vectors. `forward` only describes the data flow; calling the model
runs it. Counting is a sum of `numel()` over the registered tensors.
"""
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def count_parameters(model):
    return int(sum(p.numel() for p in model.parameters()))
