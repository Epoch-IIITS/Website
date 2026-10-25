r"""Reference solution for DL-22 Batch Normalisation with nn.BatchNorm1d.

In training mode each batch is standardised with its own (biased) statistics and the running
averages move towards the batch's mean and unbiased variance. After switching to evaluation, the
layer standardises with the running averages, so its output no longer depends on the batch.
"""
import torch
from torch import nn


def run_batchnorm(batches, x_eval, momentum=0.1):
    tensors = [torch.as_tensor(b, dtype=torch.float32) for b in batches]
    if not tensors or any(t.ndim != 2 or t.shape[0] < 2 for t in tensors):
        raise ValueError("need at least one batch, each with two or more rows")
    bn = nn.BatchNorm1d(tensors[0].shape[1], momentum=momentum)
    with torch.no_grad():
        bn.train()
        for t in tensors:
            train_output = bn(t)
        bn.eval()
        eval_output = bn(torch.as_tensor(x_eval, dtype=torch.float32))
    return {"running_mean": bn.running_mean.tolist(), "running_var": bn.running_var.tolist(),
            "train_output": train_output.tolist(), "eval_output": eval_output.tolist()}
