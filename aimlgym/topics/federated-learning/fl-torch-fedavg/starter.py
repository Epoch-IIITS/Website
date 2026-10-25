import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0):
    # TODO: from the previous step
    pass


def average_states(states, counts):
    # TODO
    pass


def federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0):
    # TODO
    pass
