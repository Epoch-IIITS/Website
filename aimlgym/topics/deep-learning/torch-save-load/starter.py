import random

import numpy as np
import torch
from torch import nn


def set_seed(seed):
    # TODO
    pass


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        # TODO

    def forward(self, x):
        # TODO
        pass


def save_model(model, path):
    # TODO
    pass


def load_model(path, n_in, n_hidden, n_out):
    # TODO
    pass
