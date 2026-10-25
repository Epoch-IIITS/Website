# Dropout with train() and eval()

## Learning outcomes

After this lesson you can:

- Add nn.Dropout to a model and explain inverted dropout scaling
- Get deterministic predictions with model.eval() and torch.no_grad()
- Restore a model's previous mode after evaluation

## Intuition
Dropout randomly switches off a fraction p of a layer's activations during training, so the
network cannot rely on any single unit. At prediction time nothing is dropped. To keep the
expected activation the same in both cases, surviving activations are scaled up by 1/(1 − p)
during training — "inverted" dropout.

## Precise explanation
```python
class DropoutMLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out, p=0.5):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p),
                                 nn.Linear(n_hidden, n_out))
```

* In `model.train()` mode, `nn.Dropout(p)` zeroes each element with probability p and multiplies
  the rest by 1/(1 − p). Two forward passes give different outputs.
* In `model.eval()` mode it does nothing: predictions are deterministic.
* `model.training` tells you the current mode. A helper that evaluates should restore the mode it
  found, so it can be called in the middle of training.

## Worked example
With p = 0.5 an activation 2.0 becomes either 0 or 4.0 in training (expected value 2.0) and stays
2.0 in evaluation.

## What the library does inside
The mask-and-scale of DL-21 (the optional deep dive after this step), drawn from
PyTorch's random generator, with the mode taken from the module's `training` flag.

## Common mistakes
* Evaluating in training mode: noisy, worse-looking metrics.
* Scaling at test time as well as in training (double compensation).
* Calling `model.eval()` inside a helper and never switching back, so training continues without dropout.

## Why this matters
Dropout is a standard regulariser in MLPs and transformers, and the train/eval switch matters for
every layer that behaves differently during training.

## References

- [torch.nn.Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html) — PyTorch (`S113`)
- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)
