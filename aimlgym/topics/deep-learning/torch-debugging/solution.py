r"""Reference solution for DL-27 Debugging Training.

`diagnose` encodes the loss-curve table. Overfitting one batch is a plain training loop on a tiny
fixed batch; reaching a near-zero loss shows the model, labels and loss are wired correctly.
Clipping rescales the gradients after `backward()` so that no single step can be enormous.
"""
import math

import torch
from torch import nn


def diagnose(losses):
    if len(losses) < 2:
        raise ValueError("need at least two losses")
    if not all(math.isfinite(v) for v in losses) or losses[-1] > 2 * losses[0]:
        return "diverging"
    if losses[-1] > 0.95 * losses[0]:
        return "stuck"
    return "learning"


def overfit_one_batch(model, X, y, steps=200, lr=0.01):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.long)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    for _ in range(steps):
        opt.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        opt.step()
    with torch.no_grad():
        return float(loss_fn(model(X), y))


def train_with_clipping(model, X, y, lr, steps, max_norm=None):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.float32)
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    losses = []
    for _ in range(steps):
        opt.zero_grad()
        loss = loss_fn(model(X), y)
        losses.append(loss.item())
        loss.backward()
        if max_norm is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
        opt.step()
    return losses
