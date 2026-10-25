# Saving, Loading and Reproducibility

## Learning outcomes

After this lesson you can:

- Save and restore a model through its state_dict
- Load weights safely with weights_only=True
- Seed Python, NumPy and PyTorch together for reproducible runs

## Intuition
Training can take hours, so you save the result. PyTorch saves the **weights** — a dictionary from
parameter names to tensors — not the Python object. To load, you rebuild the same architecture
and pour the weights in. And to rerun an experiment exactly, every random generator must start
from the same seed.

## Precise explanation
```python
torch.save(model.state_dict(), "model.pt")            # an ordered dict of tensors

model = MLP(4, 8, 3)                                    # same architecture, random weights
model.load_state_dict(torch.load("model.pt", weights_only=True))
model.eval()                                            # ready for inference
```

* `state_dict()` keys look like `net.0.weight`; buffers such as BatchNorm's running statistics are
  included too. A different architecture fails to load with a clear `RuntimeError`.
* `weights_only=True` loads only tensors and simple containers. Loading arbitrary pickled objects
  can execute code, so never load untrusted files without it.
* To continue training, also save the optimiser's `state_dict()` (Adam's running averages) and the
  epoch number in one checkpoint dict.
* Reproducibility: seed `random`, `numpy` and `torch` (`torch.manual_seed`) and pass seeded
  generators to DataLoaders. `torch.use_deterministic_algorithms(True)` makes PyTorch raise an
  error instead of silently using a nondeterministic algorithm.

## Worked example
Train, save, then load into a fresh `MLP(4, 8, 3)`: both models give identical outputs on the same
input. Loading the file into `MLP(4, 16, 3)` raises "size mismatch for net.0.weight".

## Common mistakes
* `torch.save(model)` (pickling the whole object): breaks when the class moves or changes.
* Forgetting `model.eval()` after loading a model with dropout or batch normalisation.
* Seeding only PyTorch while the data split uses NumPy's or Python's random generator.

## Why this matters
Checkpoints let you resume, share and deploy models; seeds let others reproduce your results —
and let you check that a change, not luck, improved a metric.

## References

- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
- [Reproducibility (PyTorch notes)](https://docs.pytorch.org/docs/stable/notes/randomness.html) — PyTorch (`S109`)
