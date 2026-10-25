import numpy as np


def dense_backward(X, W, dY):
    # TODO
    return None, None, None


def relu_backward(Z, dA):
    # TODO
    return dA


def mse_and_grad(Y_hat, Y):
    diff = np.asarray(Y_hat, dtype=float) - np.asarray(Y, dtype=float)
    loss = float(np.mean(diff ** 2))
    # TODO: gradient
    return loss, np.zeros_like(diff)


def two_layer_grads(X, Y, params):
    # TODO: forward pass, then backward through both layers
    return 0.0, {k: np.zeros_like(v) for k, v in params.items()}
