# FL-05 · Client Training with a PyTorch Model

**Topic:** Federated Learning · **Difficulty:** intermediate · **Allowed packages:** torch

**Builds on:** FL-04 Label-Skewed (non-IID) Partition, DL-18 A Full Training Loop

Read the lesson first: [article.md](article.md)

## Task

Write `client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0)` for a regression
model: deep-copy the model, train the copy with `nn.MSELoss` and `torch.optim.SGD(lr)` over a
`DataLoader(TensorDataset(X, y), batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed))`
for `epochs` epochs, and return `(state_dict, n_samples)`.

* Convert `X` and `y` to float32 tensors (`y` with shape `(n, 1)`).
* The global model must not change. Raise `ValueError` if `epochs < 1` or `X` is empty.

## Hints

<details><summary>Hint 1</summary>

`local = copy.deepcopy(global_model)` before anything else touches the weights.

</details>

<details><summary>Hint 2</summary>

`y = torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1)`.

</details>

<details><summary>Hint 3</summary>

Return `local.state_dict(), len(y)` after the training loop.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_global_unchanged` | Train copy.deepcopy(global_model), never the global model itself. |
| `test_learns_towards_client_data` | Use MSELoss with y reshaped to (n, 1) and SGD with the given lr. |
| `test_reproducible` | Shuffle with a DataLoader generator seeded with seed. |
| `test_invalid` | Reject epochs < 1 and empty data. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The client works on a deep copy, so the server's model is untouched; a fresh optimiser and a seeded
loader run the local epochs; the result is the copy's state dict plus the number of examples, which is
all the server needs.

## References

- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
