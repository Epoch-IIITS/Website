r"""Reference solution for DL-09 Autograd in PyTorch.

`w` and `b` become leaf tensors that require gradients; every operation on them is recorded.
`backward()` applies the chain rule from the loss back to the leaves, so `.grad` holds ∂L/∂w and
∂L/∂b. New tensors are created on each call, so gradients never accumulate between calls.
"""
import torch


def neuron_gradients(x, w, b, target):
    if len(x) != len(w):
        raise ValueError("x and w must have the same length")
    x_t = torch.tensor(x, dtype=torch.float32)
    w_t = torch.tensor(w, dtype=torch.float32, requires_grad=True)
    b_t = torch.tensor(float(b), requires_grad=True)
    loss = (torch.sigmoid((w_t * x_t).sum() + b_t) - target) ** 2
    loss.backward()
    return {"loss": loss.item(), "dw": w_t.grad.tolist(), "db": b_t.grad.item()}
