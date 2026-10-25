r"""Reference solution for DL-05 PyTorch Tensors.

`torch.as_tensor` converts lists and arrays to float32 tensors (without copying when no conversion
is needed). The shape checks give a clear error before the matrix product; the bias broadcasts
over the batch exactly as it does in NumPy, and ReLU clips negatives to zero.
"""
import torch


def dense_relu(x, W, b):
    x = torch.as_tensor(x, dtype=torch.float32)
    W = torch.as_tensor(W, dtype=torch.float32)
    b = torch.as_tensor(b, dtype=torch.float32)
    if x.ndim != 2 or W.ndim != 2 or x.shape[1] != W.shape[0] or tuple(b.shape) != (W.shape[1],):
        raise ValueError("shapes do not fit: need x (batch, n_in), W (n_in, n_out), b (n_out,)")
    return torch.relu(x @ W + b)
