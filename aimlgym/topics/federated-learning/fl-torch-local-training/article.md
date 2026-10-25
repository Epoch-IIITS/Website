# Client Training with a PyTorch Model

## Learning outcomes

After this lesson you can:

- Copy the global model for a client with copy.deepcopy
- Train the copy for a few local epochs on the client's data only
- Return the client's state_dict and sample count without touching the global model

## Intuition
In federated learning the data never leaves the clients (phones, hospitals, departments). The server
sends its current model to each client; the client trains a **copy** for a short while on its own data
and sends back only the updated weights and how many examples it used.

## Precise explanation
```python
import copy
local = copy.deepcopy(global_model)          # never train the server's object in place
opt = torch.optim.SGD(local.parameters(), lr=lr)
for _ in range(epochs):                      # a few local epochs over the client's batches
    for xb, yb in loader:
        opt.zero_grad(); loss_fn(local(xb), yb).backward(); opt.step()
return local.state_dict(), len(y)
```

* `copy.deepcopy` duplicates parameters and buffers, so the global model is unchanged.
* The optimiser is created **per client** for the copy; its state (momentum, Adam averages) is not
  shared across clients in plain FedAvg.
* Return the weights as a `state_dict` (name → tensor) — what a real client would serialise and upload.
* Seed the client's data order (`torch.Generator().manual_seed(seed)`) so simulations are reproducible.

## Worked example
A linear model y = w·x + b starts at w = 0. A client whose data follows y = 2x trains for one epoch and
returns w ≈ 1.6; the server's own w stays 0 until it aggregates.

## What the library does inside
The same gradient steps as your NumPy FL-06 (the optional deep dive after this step), with
autograd computing the gradients of any model.

## Common mistakes
* Training `global_model` directly, so every client starts from the previous client's weights.
* Sending the model object instead of a state dict.
* Forgetting the sample count, which FedAvg needs for weighting.

## Why this matters
The next step averages these state dicts into a new global model — one round of FedAvg with real
PyTorch models.

## References

- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
- [Saving and Loading Models (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) — PyTorch (`S108`)
