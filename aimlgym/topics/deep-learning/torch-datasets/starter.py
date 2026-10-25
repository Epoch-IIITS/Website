import torch
from torch.utils.data import DataLoader, Dataset


class ArrayDataset(Dataset):
    def __init__(self, X, y):
        # TODO
        pass

    def __len__(self):
        # TODO
        pass

    def __getitem__(self, i):
        # TODO
        pass


def make_loader(X, y, batch_size, shuffle=True, seed=0):
    # TODO
    pass
