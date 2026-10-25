# Datasets and DataLoader

## Learning outcomes

After this lesson you can:

- Write a Dataset with __len__ and __getitem__
- Batch and shuffle data with DataLoader
- Make shuffling reproducible with a seeded torch.Generator

## Intuition
Training uses **mini-batches**: a few dozen examples at a time, in a new random order every epoch.
PyTorch splits the job in two. A `Dataset` knows how many examples there are and how to fetch
one; a `DataLoader` decides the order, groups examples into batches and stacks them into tensors.

## Precise explanation
```python
from torch.utils.data import DataLoader, Dataset

class ArrayDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.as_tensor(X, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.long)
    def __len__(self):
        return len(self.y)
    def __getitem__(self, i):
        return self.X[i], self.y[i]

loader = DataLoader(ArrayDataset(X, y), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
for xb, yb in loader:        # xb: (32, n_features) float32, yb: (32,) int64
    ...
```

* `__getitem__` returns one example; the loader's default **collate** function stacks them.
* With `shuffle=True` the order changes every epoch; the generator makes the sequence of orders
  reproducible. `drop_last=True` drops an incomplete final batch.
* Class labels for `CrossEntropyLoss` must be integer (`torch.long`) class indices.
* For in-memory tensors, `torch.utils.data.TensorDataset(X, y)` does the same as the class above.

## Worked example
10 examples with `batch_size=4` give batches of 4, 4 and 2. With `shuffle=False` the first batch
holds examples 0–3; with shuffling and seed 0 every example still appears exactly once per epoch.

## Common mistakes
* Labels as float32, which CrossEntropyLoss rejects.
* Returning NumPy arrays from `__getitem__` with mixed dtypes.
* Shuffling the test loader (harmless but confusing) or not shuffling the training loader.
* Expecting identical shuffles across runs without passing a generator.

## Why this matters
Real datasets do not fit in one batch; images and text are read lazily in `__getitem__`. The
training loop in the next step iterates over a DataLoader.

## References

- [Datasets & DataLoaders (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html) — PyTorch (`S105`)
- [Reproducibility (PyTorch notes)](https://docs.pytorch.org/docs/stable/notes/randomness.html) — PyTorch (`S109`)
