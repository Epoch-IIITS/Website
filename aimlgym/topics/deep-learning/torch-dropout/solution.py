r"""Reference solution for DL-20 Dropout with train() and eval().

`nn.Dropout` reads the module's mode: random masking with 1/(1 − p) scaling while training, the
identity during evaluation. The helper switches to evaluation for deterministic probabilities, turns
off gradient tracking, and restores whatever mode it found, even if an error occurs.
"""
import torch
from torch import nn


class DropoutMLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out, p=0.5):
        super().__init__()
        if not 0 <= p < 1:
            raise ValueError("p must be in [0, 1)")
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p),
                                 nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def predict_proba(model, x):
    was_training = model.training
    model.eval()
    try:
        with torch.no_grad():
            return torch.softmax(model(torch.as_tensor(x, dtype=torch.float32)), dim=1)
    finally:
        model.train(was_training)
