# DL-26 · Saving, Loading and Reproducibility

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy, torch

**Builds on:** DL-24 1-D Convolution with nn.Conv1d

Read the lesson first: [article.md](article.md)

## Task

1. `set_seed(seed)` seeds `random`, `numpy.random` and `torch`.
2. `class MLP(nn.Module)` with `self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))`.
3. `save_model(model, path)` saves `model.state_dict()` to `path`.
4. `load_model(path, n_in, n_hidden, n_out)` builds an `MLP`, loads the state dict with
   `torch.load(path, weights_only=True)`, switches it to `eval()` and returns it.

## Hints

<details><summary>Hint 1</summary>

`random.seed(seed)`, `np.random.seed(seed)`, `torch.manual_seed(seed)`.

</details>

<details><summary>Hint 2</summary>

`torch.save(model.state_dict(), path)`.

</details>

<details><summary>Hint 3</summary>

`model.load_state_dict(torch.load(path, weights_only=True))`, then `model.eval()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_roundtrip_same_outputs` | Save model.state_dict() and load it into a freshly built MLP. |
| `test_file_holds_state_dict` | torch.save the state_dict, not the model object. |
| `test_loaded_model_in_eval` | Call model.eval() after loading. |
| `test_seed_controls_all_generators` | Seed random, numpy.random and torch. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Only the state dict is written, so the file contains tensors keyed by parameter name. Loading
rebuilds the architecture, copies the tensors in (checking every name and shape) and switches to
evaluation. Seeding all three generators makes any later random choice repeatable.

## References

- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
- [Reproducibility (PyTorch notes)](https://docs.pytorch.org/docs/stable/notes/randomness.html) — PyTorch (`S109`)
