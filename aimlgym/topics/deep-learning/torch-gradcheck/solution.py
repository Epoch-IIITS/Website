r"""Reference solution for DL-12 Custom Gradients and gradcheck.

The forward pass saves its input and uses `logaddexp`, which never overflows. The backward pass
multiplies the upstream gradient by the local derivative σ(x). gradcheck compares that backward
with central differences on a float64 input and reports whether they agree.
"""
import torch


class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return torch.logaddexp(x, torch.zeros_like(x))

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * torch.sigmoid(x)


def softplus(x):
    return Softplus.apply(x)


def passes_gradcheck(fn, shape, seed=0):
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(shape, generator=g, dtype=torch.float64, requires_grad=True)
    return bool(torch.autograd.gradcheck(fn, (x,), raise_exception=False))
