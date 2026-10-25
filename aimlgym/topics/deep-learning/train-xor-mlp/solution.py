r"""Reference solution for DL-19 Train an MLP on XOR.

The forward pass stores h and p, the backward pass propagates δ from the output to the hidden
layer using the tanh derivative, and all gradients are computed before any update. Full-batch
gradient descent then drives the loss toward zero; the hidden layer makes XOR linearly separable.
"""
import numpy as np

X_XOR = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
Y_XOR = np.array([0., 1., 1., 0.])


def _sigmoid(z):
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


def init_params(n_hidden, seed):
    rng = np.random.default_rng(seed)
    W1 = rng.normal(0, 1, (2, n_hidden))
    W2 = rng.normal(0, 1, (n_hidden, 1))
    return {"W1": W1, "b1": np.zeros(n_hidden), "W2": W2, "b2": np.zeros(1)}


def forward_backward(X, y, params):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    h = np.tanh(X @ params["W1"] + params["b1"])
    p = _sigmoid(h @ params["W2"] + params["b2"])[:, 0]
    pc = np.clip(p, 1e-12, 1 - 1e-12)
    loss = float(-np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc)))
    d2 = ((p - y) / n)[:, None]
    d1 = (d2 @ params["W2"].T) * (1 - h ** 2)
    grads = {"W2": h.T @ d2, "b2": d2.sum(axis=0), "W1": X.T @ d1, "b1": d1.sum(axis=0)}
    return loss, grads


def train_xor(n_hidden=8, lr=1.0, epochs=3000, seed=0):
    params = init_params(n_hidden, seed)
    history = []
    for _ in range(epochs):
        loss, g = forward_backward(X_XOR, Y_XOR, params)
        history.append(loss)
        params = {k: params[k] - lr * g[k] for k in params}
    return params, history
