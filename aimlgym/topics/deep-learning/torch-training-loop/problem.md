# DL-18 · A Full Training Loop

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy, torch

**Builds on:** DL-17 Datasets and DataLoader

Read the lesson first: [article.md](article.md)

## Task

Write `train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0)` returning
`(model, history)` where `history` lists the mean training loss of each epoch.

* Call `torch.manual_seed(seed)` first, then build
  `nn.Sequential(nn.Linear(n_features, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_classes))`
  with `n_classes = max(y) + 1`.
* Batches come from `DataLoader(TensorDataset(X_float32, y_long), batch_size, shuffle=True,
  generator=torch.Generator().manual_seed(seed))`; use `nn.CrossEntropyLoss` and `torch.optim.Adam`.
* Each epoch's loss is the batch losses weighted by batch size, divided by the number of examples.
* Leave the model in `eval()` mode.

Also write `predict(model, X)` returning a list of predicted class indices, computed with
`model.eval()` and `torch.no_grad()`.

## Hints

<details><summary>Hint 1</summary>

Convert once: `X = torch.as_tensor(X, dtype=torch.float32)`, `y = torch.as_tensor(y, dtype=torch.long)`; seed before building the model.

</details>

<details><summary>Hint 2</summary>

Per batch: `opt.zero_grad()`, `loss = loss_fn(model(xb), yb)`, `loss.backward()`, `opt.step()`, `total += loss.item() * len(yb)`.

</details>

<details><summary>Hint 3</summary>

`predict`: `model.eval()`, then `with torch.no_grad(): return model(X).argmax(dim=1).tolist()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_learns_xor` | Use CrossEntropyLoss on logits and run zero_grad / backward / step for every batch. |
| `test_reproducible` | Seed with torch.manual_seed(seed) before building the model and pass a seeded generator to the DataLoader. |
| `test_eval_mode_and_shapes` | Call model.eval() before returning; the last layer has max(y) + 1 outputs. |
| `test_loss_falls` | Record the size-weighted mean loss once per epoch. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Seeding before the model fixes the initial weights, and the seeded generator fixes the batch
order, so the whole run is reproducible. Each batch does one optimisation step; the epoch loss is
the size-weighted mean. Prediction switches to evaluation mode and disables gradient tracking.

## References

- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
