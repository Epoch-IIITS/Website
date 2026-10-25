r"""Reference solution for DL-24 1-D Convolution with nn.Conv1d.

After conversion and shape checks, `F.conv1d` does the sliding weighted sums for every batch item,
output channel and position at once. Padding adds zeros at both ends; stride skips positions.
"""
import torch
import torch.nn.functional as F


def conv1d_layer(x, weight, bias=None, stride=1, padding=0):
    x = torch.as_tensor(x, dtype=torch.float32)
    weight = torch.as_tensor(weight, dtype=torch.float32)
    if x.ndim != 3 or weight.ndim != 3 or x.shape[1] != weight.shape[1]:
        raise ValueError("need x (B, C_in, L) and weight (C_out, C_in, K) with matching C_in")
    if x.shape[2] + 2 * padding < weight.shape[2]:
        raise ValueError("padded input is shorter than the kernel")
    if bias is not None:
        bias = torch.as_tensor(bias, dtype=torch.float32)
        if tuple(bias.shape) != (weight.shape[0],):
            raise ValueError("bias needs one value per output channel")
    return F.conv1d(x, weight, bias, stride=stride, padding=padding)
