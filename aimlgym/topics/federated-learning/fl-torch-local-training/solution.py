r"""Reference solution for FL-05 Client Training with a PyTorch Model.

The client works on a deep copy, so the server's model is untouched; a fresh optimiser and a seeded
loader run the local epochs; the result is the copy's state dict plus the number of examples, which is
all the server needs.
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
