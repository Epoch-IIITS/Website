r"""Reference solution for FL-11 FedAvg with PyTorch state_dicts.

The average is taken tensor by tensor with weights proportional to client data; integer buffers are
copied because they cannot be averaged. Each round sends the current global model to every client,
averages the returned weights and loads them, and the combined-data loss shows the global model improving.
"""
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
