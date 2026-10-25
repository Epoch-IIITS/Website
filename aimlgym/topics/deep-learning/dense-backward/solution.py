r"""Reference solution for DL-11 Backpropagation Through a Dense Layer.

The dense rule follows from $Y_{ij} = \sum_k X_{ik}W_{kj} + b_j$; each output is a transposed product
that matches the parameter's shape. ReLU masks the upstream gradient, and the MSE gradient is
$2(\hat Y - Y)/m$. The two-layer network simply chains these pieces from the loss back to the
input, reusing values cached during the forward pass.
"""
import numpy as np


def dense_backward(X, W, dY):
    X, W, dY = (np.asarray(a, dtype=float) for a in (X, W, dY))
    return dY @ W.T, X.T @ dY, dY.sum(axis=0)


def relu_backward(Z, dA):
    return np.asarray(dA, dtype=float) * (np.asarray(Z) > 0)


def mse_and_grad(Y_hat, Y):
    diff = np.asarray(Y_hat, dtype=float) - np.asarray(Y, dtype=float)
    return float(np.mean(diff ** 2)), 2 * diff / diff.size


def two_layer_grads(X, Y, params):
    X = np.asarray(X, dtype=float)
    Z1 = X @ params["W1"] + params["b1"]
    H = np.maximum(Z1, 0)
    Y_hat = H @ params["W2"] + params["b2"]
    loss, dY = mse_and_grad(Y_hat, Y)
    dH, dW2, db2 = dense_backward(H, params["W2"], dY)
    dZ1 = relu_backward(Z1, dH)
    _, dW1, db1 = dense_backward(X, params["W1"], dZ1)
    return loss, {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}
