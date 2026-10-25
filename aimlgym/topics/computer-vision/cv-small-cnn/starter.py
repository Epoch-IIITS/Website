import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SmallCNN(nn.Module):
    def __init__(self, n_classes=3, size=16):
        super().__init__()
        # TODO

    def forward(self, x):
        # TODO
        pass


def train_cnn(images, labels, epochs=8, lr=0.01, seed=0):
    # TODO
    pass


def predict(model, images):
    # TODO
    pass
