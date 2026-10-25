"""Federated learning with PyTorch (library revision, Phase 6).

[[local-sgd]] (local training by hand in NumPy) follows the PyTorch client step as an optional deep dive.
"""

PROBLEMS = [
# ---------------------------------------------------------------- fl-torch-local-training
{
"slug": "fl-torch-local-training", "title": "Client Training with a PyTorch Model",
"difficulty": "intermediate", "prereqs": ["label-skew-partition", "torch-training-loop"], "packages": ["torch"],
"objectives": ["Copy the global model for a client with copy.deepcopy",
               "Train the copy for a few local epochs on the client's data only",
               "Return the client's state_dict and sample count without touching the global model"],
"tags": ["pytorch", "federated-learning", "local-training", "state-dict"],
"sources": ["S039", "S108"], "entry": "client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0)",
"article": r'''
# Client Training with a PyTorch Model

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
The same gradient steps as your NumPy [[local-sgd]] (the optional deep dive after this step), with
autograd computing the gradients of any model.

## Common mistakes
* Training `global_model` directly, so every client starts from the previous client's weights.
* Sending the model object instead of a state dict.
* Forgetting the sample count, which FedAvg needs for weighting.

## Why this matters
The next step averages these state dicts into a new global model — one round of FedAvg with real
PyTorch models.
''',
"statement": r'''
Write `client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0)` for a regression
model: deep-copy the model, train the copy with `nn.MSELoss` and `torch.optim.SGD(lr)` over a
`DataLoader(TensorDataset(X, y), batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed))`
for `epochs` epochs, and return `(state_dict, n_samples)`.

* Convert `X` and `y` to float32 tensors (`y` with shape `(n, 1)`).
* The global model must not change. Raise `ValueError` if `epochs < 1` or `X` is empty.
''',
"starter": r'''
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0):
    # TODO
    pass
''',
"hints": [
    "`local = copy.deepcopy(global_model)` before anything else touches the weights.",
    "`y = torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1)`.",
    "Return `local.state_dict(), len(y)` after the training loop.",
],
"solution": r'''
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1)
    if epochs < 1 or len(X) == 0:
        raise ValueError("need epochs >= 1 and some data")
    local = copy.deepcopy(global_model)
    opt = torch.optim.SGD(local.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    loader = DataLoader(TensorDataset(X, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    local.train()
    for _ in range(epochs):
        for xb, yb in loader:
            opt.zero_grad()
            loss_fn(local(xb), yb).backward()
            opt.step()
    return local.state_dict(), len(y)
''',
"explanation": r'''
The client works on a deep copy, so the server's model is untouched; a fresh optimiser and a seeded
loader run the local epochs; the result is the copy's state dict plus the number of examples, which is
all the server needs.
''',
"tests": r'''
import torch
from torch import nn


def line(seed, n=40, slope=2.0):
    g = torch.Generator().manual_seed(seed)
    X = torch.rand(n, 1, generator=g) * 2 - 1
    return X, slope * X[:, 0] + 0.5


def zero_model():
    model = nn.Linear(1, 1)
    with torch.no_grad():
        model.weight.zero_(); model.bias.zero_()
    return model


class TestClientUpdate(unittest.TestCase):
    def test_global_unchanged(self):
        model = zero_model()
        X, y = line(0)
        S.client_update(model, X, y, epochs=3)
        self.assertEqual((model.weight.item(), model.bias.item()), (0.0, 0.0))

    def test_learns_towards_client_data(self):
        X, y = line(1)
        state, n = S.client_update(zero_model(), X, y, epochs=20, lr=0.1)
        self.assertEqual(n, 40)
        self.assertAlmostEqual(state["weight"].item(), 2.0, delta=0.2)
        self.assertAlmostEqual(state["bias"].item(), 0.5, delta=0.1)

    def test_more_epochs_lower_loss(self):
        X, y = line(2)
        def loss(state):
            m = zero_model(); m.load_state_dict(state)
            return nn.functional.mse_loss(m(X), y.reshape(-1, 1)).item()
        one, _ = S.client_update(zero_model(), X, y, epochs=1)
        five, _ = S.client_update(zero_model(), X, y, epochs=5)
        self.assertLess(loss(five), loss(one))

    def test_reproducible(self):
        X, y = line(3)
        a, _ = S.client_update(zero_model(), X, y, seed=4)
        b, _ = S.client_update(zero_model(), X, y, seed=4)
        self.assertTrue(all(torch.equal(a[k], b[k]) for k in a))

    def test_state_dict_keys(self):
        X, y = line(4)
        model = nn.Sequential(nn.Linear(1, 4), nn.ReLU(), nn.Linear(4, 1))
        state, _ = S.client_update(model, X, y)
        self.assertEqual(list(state), list(model.state_dict()))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.client_update(zero_model(), torch.zeros(0, 1), torch.zeros(0), epochs=1)
        with self.assertRaises(ValueError):
            S.client_update(zero_model(), *line(5), epochs=0)
''',
"feedback": [
    ("test_global_unchanged", "Train copy.deepcopy(global_model), never the global model itself."),
    ("test_learns_towards_client_data", "Use MSELoss with y reshaped to (n, 1) and SGD with the given lr."),
    ("test_reproducible", "Shuffle with a DataLoader generator seeded with seed."),
    ("test_invalid", "Reject epochs < 1 and empty data."),
],
},
# ---------------------------------------------------------------- fl-torch-fedavg
{
"slug": "fl-torch-fedavg", "title": "FedAvg with PyTorch state_dicts",
"difficulty": "advanced", "prereqs": ["fedavg-training", "fl-torch-local-training"], "packages": ["torch"],
"objectives": ["Average client state_dicts weighted by their sample counts",
               "Handle integer buffers that must not be averaged",
               "Run several federated rounds and watch the global model improve"],
"tags": ["pytorch", "federated-learning", "fedavg", "aggregation"],
"sources": ["S108", "S039"], "entry": "average_states(states, counts); federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0)",
"article": r'''
# FedAvg with PyTorch state_dicts

## Intuition
After a round of local training, each client has slightly different weights. FedAvg combines them
into the next global model by averaging each parameter, giving clients with more data more say —
exactly the weighted average of [[weighted-fedavg]], now applied tensor by tensor to a state dict.

## Precise explanation
$$\theta^{\text{global}}_k = \sum_i \frac{n_i}{\sum_j n_j}\,\theta^{(i)}_k \quad\text{for every tensor } k.$$

```python
total = sum(counts)
averaged = {k: sum(state[k] * (n / total) for state, n in zip(states, counts)) for k in states[0]}
model.load_state_dict(averaged)
```

* All clients must share one architecture, so their state dicts have the same keys and shapes.
* Floating-point tensors are averaged. **Integer buffers** — for example BatchNorm's
  `num_batches_tracked` — cannot be averaged meaningfully; copy them from the first client.
* A **round**: send the global model to every client ([[fl-torch-local-training]]), collect
  `(state_dict, n)`, average, load into the global model. Repeat for several rounds.
* With non-IID clients ([[label-skew-partition]]) local models drift apart; more rounds with fewer local
  epochs, or FedProx ([[fedprox]]), help.

## Worked example
Two clients with 30 and 10 examples and weights w = 1.0 and 2.0 give 0.75·1.0 + 0.25·2.0 = 1.25.

## Common mistakes
* Averaging without weights when client sizes differ.
* Averaging `num_batches_tracked` and getting a float or a type error.
* Reusing the same seed for every client, so all shuffles are identical.

## Why this matters
This is the algorithm behind federated keyboards and hospital collaborations; frameworks such as Flower
implement the same loop across real devices. The project idea after this step simulates departments.
''',
"statement": r'''
1. `average_states(states, counts)` returns a new state dict: floating-point tensors are the weighted
   average by `counts`; other tensors (integers) are copied from the first state. Raise `ValueError`
   if the lists are empty, differ in length, any count is ≤ 0, or the key sets differ.
2. `federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0)` where `clients` is a list of
   `(X, y)`: for each round, call `client_update(model, X, y, epochs, lr, seed=seed + 1000 * round_index + client_index)`
   for every client, average the results and load them into `model`. Return the list of global MSE
   losses on all clients' data combined, measured **after** each round.

Copy your `client_update` from the previous step into this file.
''',
"starter": r'''
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0):
    # TODO: from the previous step
    pass


def average_states(states, counts):
    # TODO
    pass


def federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0):
    # TODO
    pass
''',
"hints": [
    "Check `tensor.is_floating_point()` to decide between averaging and copying.",
    "`sum(state[k] * (n / total) for state, n in zip(states, counts))` averages one tensor.",
    "After each round, measure `nn.functional.mse_loss(model(X_all), y_all)` under `torch.no_grad()`.",
],
"solution": r'''
import copy

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def client_update(global_model, X, y, epochs=1, lr=0.1, batch_size=8, seed=0):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1)
    if epochs < 1 or len(X) == 0:
        raise ValueError("need epochs >= 1 and some data")
    local = copy.deepcopy(global_model)
    opt = torch.optim.SGD(local.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    loader = DataLoader(TensorDataset(X, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    local.train()
    for _ in range(epochs):
        for xb, yb in loader:
            opt.zero_grad()
            loss_fn(local(xb), yb).backward()
            opt.step()
    return local.state_dict(), len(y)


def average_states(states, counts):
    if not states or len(states) != len(counts) or any(n <= 0 for n in counts):
        raise ValueError("need one positive count per state")
    keys = list(states[0])
    if any(list(s) != keys for s in states):
        raise ValueError("all states must have the same keys")
    total = sum(counts)
    averaged = {}
    for k in keys:
        if states[0][k].is_floating_point():
            averaged[k] = sum(s[k] * (n / total) for s, n in zip(states, counts))
        else:
            averaged[k] = states[0][k].clone()
    return averaged


def federated_training(model, clients, rounds, epochs=1, lr=0.1, seed=0):
    X_all = torch.cat([torch.as_tensor(X, dtype=torch.float32) for X, _ in clients])
    y_all = torch.cat([torch.as_tensor(y, dtype=torch.float32).reshape(-1, 1) for _, y in clients])
    losses = []
    for r in range(rounds):
        results = [client_update(model, X, y, epochs, lr, seed=seed + 1000 * r + i) for i, (X, y) in enumerate(clients)]
        model.load_state_dict(average_states([s for s, _ in results], [n for _, n in results]))
        with torch.no_grad():
            losses.append(nn.functional.mse_loss(model(X_all), y_all).item())
    return losses
''',
"explanation": r'''
The average is taken tensor by tensor with weights proportional to client data; integer buffers are
copied because they cannot be averaged. Each round sends the current global model to every client,
averages the returned weights and loads them, and the combined-data loss shows the global model improving.
''',
"tests": r'''
import torch
from torch import nn


def client(seed, n, slope=2.0, shift=0.0):
    g = torch.Generator().manual_seed(seed)
    X = torch.rand(n, 1, generator=g) * 2 - 1 + shift
    return X, slope * X[:, 0] + 0.5


class TestFedAvg(unittest.TestCase):
    def test_weighted_average(self):
        a = {"w": torch.tensor([1.0]), "steps": torch.tensor(3)}
        b = {"w": torch.tensor([2.0]), "steps": torch.tensor(7)}
        out = S.average_states([a, b], [30, 10])
        self.assertAlmostEqual(out["w"].item(), 1.25)
        self.assertEqual((out["steps"].item(), out["steps"].dtype), (3, torch.int64))

    def test_equal_counts_is_mean(self):
        torch.manual_seed(0)
        states = [nn.Linear(3, 2).state_dict() for _ in range(3)]
        out = S.average_states(states, [5, 5, 5])
        self.assertTrue(torch.allclose(out["weight"], sum(s["weight"] for s in states) / 3))

    def test_batchnorm_model(self):
        torch.manual_seed(1)
        states = [nn.Sequential(nn.Linear(2, 2), nn.BatchNorm1d(2)).state_dict() for _ in range(2)]
        out = S.average_states(states, [1, 3])
        self.assertEqual(out["1.num_batches_tracked"].dtype, torch.int64)
        nn.Sequential(nn.Linear(2, 2), nn.BatchNorm1d(2)).load_state_dict(out)

    def test_training_improves(self):
        torch.manual_seed(2)
        model = nn.Linear(1, 1)
        clients = [client(0, 30), client(1, 10, shift=0.5), client(2, 20, shift=-0.5)]
        losses = S.federated_training(model, clients, rounds=8, epochs=2, lr=0.1)
        self.assertEqual(len(losses), 8)
        self.assertLess(losses[-1], losses[0] / 4)
        self.assertAlmostEqual(model.weight.item(), 2.0, delta=0.2)

    def test_reproducible(self):
        clients = [client(3, 16), client(4, 16)]
        torch.manual_seed(3); a = S.federated_training(nn.Linear(1, 1), clients, rounds=3)
        torch.manual_seed(3); b = S.federated_training(nn.Linear(1, 1), clients, rounds=3)
        self.assertEqual(a, b)

    def test_invalid(self):
        s = nn.Linear(1, 1).state_dict()
        with self.assertRaises(ValueError):
            S.average_states([], [])
        with self.assertRaises(ValueError):
            S.average_states([s, s], [1, 0])
        with self.assertRaises(ValueError):
            S.average_states([s, {"weight": s["weight"]}], [1, 1])
''',
"feedback": [
    ("test_weighted_average", "Weight each client by n_i / total and copy integer tensors from the first state."),
    ("test_batchnorm_model", "num_batches_tracked is an integer buffer: copy it instead of averaging."),
    ("test_training_improves", "Each round: update every client from the current model, average, load_state_dict."),
    ("test_invalid", "Reject empty input, non-positive counts and mismatched keys."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "federated-departments", "title": "Federated Training across Departments",
"tags": ["federated-learning", "non-iid", "flower"],
"brief": r'''
Simulate several college departments that want a shared model (for example, predicting which students
need extra support) without pooling their records. Compare federated training with central training,
and see how uneven, non-IID data across departments affects the result.
''',
"uses": ["label-skew-partition", "fl-torch-local-training", "fl-torch-fedavg", "dp-aggregation", "fedprox"],
"milestones": [
    "Generate or load a tabular dataset and split it into 4–6 'departments' with different label mixes.",
    "Train a central model on all data as the reference.",
    "Run FedAvg with the PyTorch steps and plot global accuracy per round.",
    "Vary local epochs and client sampling and record how many rounds each setting needs.",
    "Add update clipping and noise (differential privacy) and measure the accuracy cost.",
],
"stretch": [
    "Implement FedProx in PyTorch and compare on the most uneven split.",
    "Run the same experiment with the Flower framework, with clients as separate processes.",
    "Personalise: fine-tune the global model on each department and report per-department accuracy.",
],
"data": r'''
Synthetic data from `sklearn.datasets.make_classification` works well; split it by a feature to create
non-IID departments. See the [Flower framework documentation](https://flower.ai/docs/framework/) for
running real federated clients.
''',
"setup": r'''
```bash
pip install torch scikit-learn flwr
python simulate.py --clients 5 --rounds 30
```
''',
},
]
