r"""Reference solution for FL-10 Full FedAvg Training Loop.

Each round samples participants, trains each from the current global model with a unique seed,
aggregates only the participants' models by size, and evaluates the loss on all clients' data. The
seed scheme makes every run fully reproducible.
"""
import numpy as np


def sample_clients(n_clients, fraction, seed, round_idx):
    m = max(1, round(fraction * n_clients))
    return np.sort(np.random.default_rng([seed, round_idx]).choice(n_clients, m, replace=False))


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.array(w, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(y)
    for _ in range(epochs):
        order = rng.permutation(n)
        for s in range(0, n, batch_size):
            b = order[s:s + batch_size]
            w = w - lr * 2.0 / len(b) * X[b].T @ (X[b] @ w - y[b])
    return w


def global_loss(w, clients):
    se = sum(float(((X @ w - y) ** 2).sum()) for X, y in clients)
    return se / sum(len(y) for _, y in clients)


def train_fedavg(clients, w0, rounds, fraction, lr, epochs, batch_size, seed):
    if rounds < 1 or not clients:
        raise ValueError("need rounds >= 1 and at least one client")
    K = len(clients)
    w = np.array(w0, dtype=float)
    history = []
    for t in range(rounds):
        chosen = sample_clients(K, fraction, seed, t)
        locs, sizes = [], []
        for k in chosen:
            X, y = clients[k]
            bs = len(y) if batch_size is None else batch_size
            locs.append(local_sgd(w, X, y, lr, epochs, bs, seed * 1000 + t * K + int(k)))
            sizes.append(len(y))
        total = float(sum(sizes))
        w = sum((n / total) * wk for n, wk in zip(sizes, locs))
        history.append(global_loss(w, clients))
    return w, history
