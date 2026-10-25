r"""Reference solution for CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d.

Both pooling layers take the same window arguments, so one dictionary selects the class. The size
formula is the same as for convolution, with the stride defaulting to the kernel size.
"""
import torch
from torch import nn

POOLS = {"max": nn.MaxPool2d, "avg": nn.AvgPool2d}


def pool(x, kind, kernel_size, stride=None, padding=0):
    if kind not in POOLS:
        raise ValueError("kind must be 'max' or 'avg'")
    x = torch.as_tensor(x, dtype=torch.float32)
    if x.ndim != 4:
        raise ValueError("expected a (batch, channels, height, width) tensor")
    return POOLS[kind](kernel_size, stride=stride, padding=padding)(x)


def pooled_size(n, kernel_size, stride=None, padding=0):
    stride = stride or kernel_size
    return (n + 2 * padding - kernel_size) // stride + 1
