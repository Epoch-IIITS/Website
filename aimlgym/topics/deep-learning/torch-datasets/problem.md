# DL-17 · Datasets and DataLoader

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy, torch

**Builds on:** DL-15 Optimisers in torch.optim

Read the lesson first: [article.md](article.md)

## Task

1. Write `class ArrayDataset(Dataset)` storing `X` as float32 and `y` as `torch.long` tensors,
   with `__len__` and `__getitem__(i)` returning `(X[i], y[i])`. Raise `ValueError` in
   `__init__` if the lengths differ.
2. Write `make_loader(X, y, batch_size, shuffle=True, seed=0)` returning a `DataLoader` over an
   `ArrayDataset`, shuffled with `generator=torch.Generator().manual_seed(seed)` when `shuffle`
   is true.

## Hints

<details><summary>Hint 1</summary>

Convert in `__init__`: `torch.as_tensor(X, dtype=torch.float32)` and `torch.as_tensor(y, dtype=torch.long)`.

</details>

<details><summary>Hint 2</summary>

`__len__` returns `len(self.y)`; `__getitem__` returns `self.X[i], self.y[i]`.

</details>

<details><summary>Hint 3</summary>

`DataLoader(dataset, batch_size=..., shuffle=shuffle, generator=torch.Generator().manual_seed(seed))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_dataset_items` | Store X as float32 and y as torch.long; __getitem__ returns (X[i], y[i]). |
| `test_batch_sizes` | Pass batch_size to the DataLoader and keep the incomplete last batch. |
| `test_seeded_shuffle_reproducible` | Pass generator=torch.Generator().manual_seed(seed). |
| `test_length_mismatch` | Raise ValueError in __init__ when the lengths differ. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The dataset converts once to the dtypes a classifier needs and fetches one row at a time; the
loader groups rows into stacked batches and, with a seeded generator, produces the same sequence
of shuffled orders on every run.

## References

- [Datasets & DataLoaders (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html) — PyTorch (`S105`)
- [Reproducibility (PyTorch notes)](https://docs.pytorch.org/docs/stable/notes/randomness.html) — PyTorch (`S109`)
