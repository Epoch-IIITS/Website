# Local Training on a Client

## Learning outcomes

After this lesson you can:

- Run several epochs of minibatch SGD on local data
- Shuffle reproducibly per epoch
- Return the local model without touching the global one

## Intuition
In FedAvg each client does real work: several passes (epochs) of minibatch SGD on its own data,
starting from the global model. More local work means fewer communication rounds — the central idea
of McMahan et al.

## Precise explanation
For linear regression with loss $L(w) = \frac{1}{|B|}\sum_{i\in B}(x_i\cdot w - y_i)^2$ on a batch B:
$\nabla L = \frac{2}{|B|}X_B^\top(X_Bw - y_B)$ (ML-10).
Local SGD with `E` epochs and batch size `B`:
```text
rng = default_rng(seed)
for epoch in 1..E:
    order = rng.permutation(n)
    for start in 0, B, 2B, ...:
        batch = order[start:start+B]          # last batch may be smaller
        w = w - lr * grad(w, X[batch], y[batch])
```
Hyperparameters E and B control how far a client drifts from the global model — on non-IID data,
too much local work causes **client drift** (FL-14).

## Worked example
With B = n and E = 1, local SGD is one full-batch gradient step: w − lr·∇L(w).

## Common mistakes
* Updating the caller's global array in place.
* Re-seeding inside the epoch loop (same order every epoch).
* Dividing by n instead of the batch size.

## Why this matters
This function is the "client" half of every FL simulation in the remaining problems.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
