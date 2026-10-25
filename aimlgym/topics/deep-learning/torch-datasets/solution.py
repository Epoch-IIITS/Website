r"""Reference solution for DL-17 Datasets and DataLoader.

The dataset converts once to the dtypes a classifier needs and fetches one row at a time; the
loader groups rows into stacked batches and, with a seeded generator, produces the same sequence
of shuffled orders on every run.
"""
import torch
from torch.utils.data import DataLoader, Dataset


class ArrayDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.as_tensor(X, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.long)
        if len(self.X) != len(self.y):
            raise ValueError("X and y must have the same length")

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        return self.X[i], self.y[i]


def make_loader(X, y, batch_size, shuffle=True, seed=0):
    generator = torch.Generator().manual_seed(seed)
    return DataLoader(ArrayDataset(X, y), batch_size=batch_size, shuffle=shuffle, generator=generator)
