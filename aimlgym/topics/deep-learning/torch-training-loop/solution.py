r"""Reference solution for DL-18 A Full Training Loop.

Seeding before the model fixes the initial weights, and the seeded generator fixes the batch
order, so the whole run is reproducible. Each batch does one optimisation step; the epoch loss is
the size-weighted mean. Prediction switches to evaluation mode and disables gradient tracking.
"""
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.long)
    torch.manual_seed(seed)
    model = nn.Sequential(nn.Linear(X.shape[1], n_hidden), nn.ReLU(), nn.Linear(n_hidden, int(y.max()) + 1))
    loader = DataLoader(TensorDataset(X, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    for _ in range(epochs):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += loss.item() * len(yb)
        history.append(total / len(y))
    model.eval()
    return model, history


def predict(model, X):
    model.eval()
    with torch.no_grad():
        return model(torch.as_tensor(X, dtype=torch.float32)).argmax(dim=1).tolist()
