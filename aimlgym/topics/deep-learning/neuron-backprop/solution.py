r"""Reference solution for DL-10 Backprop Through One Neuron.

The forward pass computes and stores z and p. The backward pass multiplies local derivatives
from the loss back to the parameters, exactly following the graph. The product dL/dp · dp/dz
simplifies to p − y, which the tests check.
"""
import numpy as np


def neuron_forward_backward(x, y, w, b):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    z = float(w @ x + b)
    p = float(1.0 / (1.0 + np.exp(-z))) if z >= 0 else float(np.exp(z) / (1.0 + np.exp(z)))
    pc = min(max(p, 1e-12), 1 - 1e-12)
    loss = float(-(y * np.log(pc) + (1 - y) * np.log(1 - pc)))
    dL_dp = -y / pc + (1 - y) / (1 - pc)
    dp_dz = p * (1 - p)
    dL_dz = dL_dp * dp_dz
    return {"z": z, "p": p, "loss": loss, "dL_dp": float(dL_dp), "dp_dz": float(dp_dz),
            "dL_dz": float(dL_dz), "grad_w": dL_dz * x, "grad_b": float(dL_dz)}
