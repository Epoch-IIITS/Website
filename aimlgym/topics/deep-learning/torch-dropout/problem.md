# DL-20 · Dropout with train() and eval()

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** DL-18 A Full Training Loop

Read the lesson first: [article.md](article.md)

## Task

1. Write `class DropoutMLP(nn.Module)` with `__init__(self, n_in, n_hidden, n_out, p=0.5)` storing
   `self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p), nn.Linear(n_hidden, n_out))`
   and `forward(x)` returning `self.net(x)`. Raise `ValueError` unless `0 <= p < 1`.
2. Write `predict_proba(model, x)` returning softmax probabilities (a tensor) computed in
   evaluation mode under `torch.no_grad()`, and then **restoring** the model's previous mode.

## Hints

<details><summary>Hint 1</summary>

Validate p before building the layers; remember `super().__init__()`.

</details>

<details><summary>Hint 2</summary>

Save `was_training = model.training`, call `model.eval()`, compute under `torch.no_grad()`.

</details>

<details><summary>Hint 3</summary>

`torch.softmax(logits, dim=1)`; finally `model.train(was_training)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_training_outputs_vary` | Put nn.Dropout(p) between the ReLU and the last Linear layer. |
| `test_predictions_deterministic` | Switch to model.eval() before predicting and return softmax probabilities. |
| `test_mode_restored` | Remember model.training and call model.train(was_training) at the end. |
| `test_no_gradients_tracked` | Compute predictions inside torch.no_grad(). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`nn.Dropout` reads the module's mode: random masking with 1/(1 − p) scaling while training, the
identity during evaluation. The helper switches to evaluation for deterministic probabilities, turns
off gradient tracking, and restores whatever mode it found, even if an error occurs.

## References

- [torch.nn.Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html) — PyTorch (`S113`)
- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)
