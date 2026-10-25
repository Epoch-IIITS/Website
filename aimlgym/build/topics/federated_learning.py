"""Problem definitions for the federated learning topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- iid-partition
{
"slug": "iid-partition", "title": "IID Client Partitioning",
"difficulty": "beginner", "prereqs": ["sklearn-cross-validation"], "packages": ["numpy"],
"objectives": ["Simulate clients by partitioning a dataset", "Produce disjoint, near-equal IID shards",
               "Report client dataset sizes"],
"tags": ["federated-learning", "partitioning", "iid", "simulation"],
"sources": ["S028", "S032"], "entry": "iid_partition(n, n_clients, seed); client_sizes(parts)",
"article": r'''
# Simulating Clients: IID Partitions

## Intuition
In federated learning (FL), data lives on many devices (phones, hospitals). To study FL algorithms
on one machine we split a dataset into "client" shards. The easiest split is **IID**: every client
gets a random sample, so all clients look statistically alike.

## Precise explanation
* Shuffle indices with a seeded generator: `rng.permutation(n)`.
* Split into `n_clients` nearly equal parts with `np.array_split` (sizes differ by at most 1).
* Shards must be **disjoint** and **cover** all indices.
* Real federated data is rarely IID ([[label-skew-partition]]) and client sizes are often very unequal — which is why
  FedAvg weights clients by size ([[weighted-fedavg]]).
McMahan et al. (2016) evaluate both IID and pathological non-IID partitions.

```mermaid
flowchart LR
  D[(dataset)] --> P[shuffle + split] --> C1[client 1] & C2[client 2] & C3[client 3]
```

## Worked example
n = 10, 3 clients → sizes [4, 3, 3].

## Common mistakes
* Overlapping shards (sampling with replacement).
* Forgetting the seed → irreproducible experiments.
* Assuming equal client sizes later in the pipeline.

## Why this matters
Every FL experiment starts with a partition; its realism decides whether conclusions transfer to
real deployments.
''',
"statement": r'''
Implement:
* `iid_partition(n, n_clients, seed)` → list of `n_clients` sorted index arrays from
  `np.array_split(np.random.default_rng(seed).permutation(n), n_clients)` (sort each part).
  Raise `ValueError` unless `1 <= n_clients <= n`.
* `client_sizes(parts)` → list of ints.

**Example**
```python
parts = iid_partition(10, 3, seed=0)
client_sizes(parts)                        # [4, 3, 3]
sorted(np.concatenate(parts).tolist())     # [0, 1, ..., 9]
```
''',
"starter": r'''
import numpy as np


def iid_partition(n, n_clients, seed):
    pass


def client_sizes(parts):
    pass
''',
"hints": [
    "`perm = np.random.default_rng(seed).permutation(n)`.",
    "`[np.sort(p) for p in np.array_split(perm, n_clients)]`.",
    "`[len(p) for p in parts]`.",
],
"solution": r'''
import numpy as np


def iid_partition(n, n_clients, seed):
    if not 1 <= n_clients <= n:
        raise ValueError("need 1 <= n_clients <= n")
    perm = np.random.default_rng(seed).permutation(n)
    return [np.sort(p) for p in np.array_split(perm, n_clients)]


def client_sizes(parts):
    return [int(len(p)) for p in parts]
''',
"explanation": r'''
One seeded permutation randomises assignment; `array_split` yields disjoint, covering shards whose
sizes differ by at most one. Sorting each shard only makes outputs easier to read.
''',
"tests": r'''
import numpy as np

class TestIID(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(S.client_sizes(S.iid_partition(10, 3, 0)), [4, 3, 3])

    def test_cover_disjoint(self):
        parts = S.iid_partition(53, 7, seed=4)
        allidx = np.concatenate(parts)
        self.assertEqual(sorted(allidx.tolist()), list(range(53)))
        self.assertEqual(len(set(allidx.tolist())), 53)

    def test_recipe(self):
        perm = np.random.default_rng(2).permutation(12)
        parts = S.iid_partition(12, 4, 2)
        for p, q in zip(parts, np.array_split(perm, 4)):
            np.testing.assert_array_equal(p, np.sort(q))

    def test_reproducible(self):
        a, b = S.iid_partition(20, 5, 9), S.iid_partition(20, 5, 9)
        for p, q in zip(a, b):
            np.testing.assert_array_equal(p, q)

    def test_one_client(self):
        np.testing.assert_array_equal(S.iid_partition(5, 1, 0)[0], np.arange(5))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.iid_partition(3, 4, 0)
''',
"feedback": [
    ("test_recipe", "Use default_rng(seed).permutation(n) then np.array_split; sort each part."),
    ("test_cover_disjoint", "Every index must appear in exactly one client."),
    ("test_sizes", "array_split gives the first n % k clients one extra item."),
    ("test_errors", "Reject n_clients greater than n."),
],
},
# ---------------------------------------------------------------- weighted-fedavg
{
"slug": "weighted-fedavg", "title": "Weighted Federated Averaging",
"difficulty": "beginner", "prereqs": ["iid-partition"], "packages": ["numpy"],
"objectives": ["Aggregate client models weighted by dataset size", "Handle parameter dictionaries",
               "Validate shapes and weights"],
"tags": ["fedavg", "aggregation", "weighted-average"],
"sources": ["S028"], "entry": "fedavg(client_params, sizes)",
"article": r'''
# Weighted Federated Averaging

## Intuition
The server never sees data — only model parameters trained by clients. It combines them by averaging,
giving clients with more data proportionally more say.

## Precise explanation (McMahan et al., 2016)
With client parameters $w_k$ and sample counts $n_k$, $N = \sum_k n_k$:
$$w = \sum_k \frac{n_k}{N} w_k.$$
For models with several tensors, average each tensor (dict key) separately with the same weights.
A client with $n_k = 0$ contributes nothing; if all $n_k = 0$ the average is undefined.
The unweighted mean is biased towards small clients' data distributions.

## Worked example
Client A: w = [1, 2], n = 10; client B: w = [3, 6], n = 30 → 0.25·[1, 2] + 0.75·[3, 6] = [2.5, 5.0].

## Common mistakes
* Plain mean instead of weighted mean.
* Aggregating parameters with mismatched shapes (different model versions).
* Integer division in weights.

## Why this matters
FedAvg's aggregation step is the heart of federated learning; secure aggregation ([[secure-aggregation]]) and DP
([[dp-aggregation]]) modify exactly this step.
''',
"statement": r'''
Write `fedavg(client_params, sizes)` where `client_params` is a non-empty list of dicts
name → NumPy array (same keys and shapes) and `sizes` a list of non-negative ints. Return a new dict
of weighted averages. Raise `ValueError` for empty input, length mismatch, negative sizes, zero total
size, or mismatched keys/shapes.

**Example**
```python
fedavg([{"w": np.array([1., 2.])}, {"w": np.array([3., 6.])}], [10, 30])   # {'w': array([2.5, 5. ])}
```
''',
"starter": r'''
import numpy as np


def fedavg(client_params, sizes):
    pass
''',
"hints": [
    "`N = sum(sizes)`; weights `n_k / N`.",
    "Check `set(p) == set(client_params[0])` and shapes for every client.",
    "`{k: sum(wt * p[k] for wt, p in zip(weights, client_params)) for k in keys}`.",
],
"solution": r'''
import numpy as np


def fedavg(client_params, sizes):
    if not client_params or len(client_params) != len(sizes):
        raise ValueError("need one size per client and at least one client")
    if any(s < 0 for s in sizes):
        raise ValueError("sizes must be non-negative")
    total = float(sum(sizes))
    if total == 0:
        raise ValueError("total size is zero")
    keys = set(client_params[0])
    for p in client_params:
        if set(p) != keys or any(np.shape(p[k]) != np.shape(client_params[0][k]) for k in keys):
            raise ValueError("clients have mismatched parameters")
    return {k: sum((s / total) * np.asarray(p[k], dtype=float) for s, p in zip(sizes, client_params))
            for k in client_params[0]}
''',
"explanation": r'''
After validating structure, each parameter tensor is averaged with weights n_k / N, so larger clients
count more and the weights sum to one.
''',
"tests": r'''
import numpy as np

class TestFedAvg(unittest.TestCase):
    def test_example(self):
        out = S.fedavg([{"w": np.array([1., 2.])}, {"w": np.array([3., 6.])}], [10, 30])
        np.testing.assert_allclose(out["w"], [2.5, 5.0])

    def test_multiple_keys(self):
        out = S.fedavg([{"w": np.ones((2, 2)), "b": np.array([0.])}, {"w": np.zeros((2, 2)), "b": np.array([4.])}], [1, 3])
        np.testing.assert_allclose(out["w"], 0.25)
        np.testing.assert_allclose(out["b"], [3.0])

    def test_equal_sizes_mean(self):
        ps = [{"w": np.array([float(i)])} for i in range(5)]
        np.testing.assert_allclose(S.fedavg(ps, [7] * 5)["w"], [2.0])

    def test_zero_size_client(self):
        out = S.fedavg([{"w": np.array([100.])}, {"w": np.array([1.])}], [0, 5])
        np.testing.assert_allclose(out["w"], [1.0])

    def test_not_plain_mean(self):
        out = S.fedavg([{"w": np.array([0.])}, {"w": np.array([10.])}], [9, 1])
        np.testing.assert_allclose(out["w"], [1.0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}, {"w": np.ones(3)}], [1, 1])
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}], [0])
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}, {"v": np.ones(2)}], [1, 1])
''',
"feedback": [
    ("test_not_plain_mean", "Weight each client by n_k / N, not 1/K."),
    ("test_multiple_keys", "Average every parameter tensor separately."),
    ("test_zero_size_client", "Clients with zero samples get weight zero."),
    ("test_errors", "Validate keys, shapes and the total size."),
],
},
# ---------------------------------------------------------------- client-delta
{
"slug": "client-delta", "title": "Client Updates as Deltas",
"difficulty": "beginner", "prereqs": ["weighted-fedavg"], "packages": ["numpy"],
"objectives": ["Represent client work as a model delta", "Apply aggregated deltas with a server learning rate",
               "Show equivalence with FedAvg when server_lr = 1"],
"tags": ["fedavg", "model-updates", "server-optimizer"],
"sources": ["S028", "S032"], "entry": "client_delta(global_w, local_w); server_update(global_w, deltas, sizes, server_lr=1.0)",
"article": r'''
# Sending Deltas Instead of Models

## Intuition
Clients start from the same global model and change it a little. Sending the *change* (delta) rather
than the whole model makes aggregation look like a gradient step on the server — and it is the
quantity that clipping ([[update-clipping]]) and privacy noise ([[dp-aggregation]]) operate on.

## Precise explanation
* Client delta: $\Delta_k = w_k - w$ (local minus global).
* Server: $w \leftarrow w + \eta_s \sum_k \frac{n_k}{N}\Delta_k$.
* With $\eta_s = 1$ this equals FedAvg exactly:
  $w + \sum_k \frac{n_k}{N}(w_k - w) = \sum_k \frac{n_k}{N} w_k$.
* $\eta_s \ne 1$ (or server momentum) gives "FedOpt"-style variants discussed in the FL survey.

## Worked example
w = [0, 0]; local A = [1, 1] (n 1), local B = [3, −1] (n 1) → deltas [1, 1], [3, −1] → mean [2, 0];
η_s = 0.5 → new w = [1, 0].

## Common mistakes
* Sign errors (global − local).
* Applying deltas computed from different global versions.
* Mutating the global model in place on the client side.

## Why this matters
Delta-based aggregation is how production FL systems and privacy mechanisms are described.
''',
"statement": r'''
Implement with NumPy arrays:
* `client_delta(global_w, local_w)` → `local_w - global_w` (shapes must match, else `ValueError`).
* `server_update(global_w, deltas, sizes, server_lr=1.0)` → new global array. Raise `ValueError` for
  empty deltas, length mismatch, or zero total size. Inputs must not be modified.

**Example**
```python
server_update(np.zeros(2), [np.array([1., 1.]), np.array([3., -1.])], [1, 1], server_lr=0.5)   # [1., 0.]
```
''',
"starter": r'''
import numpy as np


def client_delta(global_w, local_w):
    pass


def server_update(global_w, deltas, sizes, server_lr=1.0):
    pass
''',
"hints": [
    "Delta is `local - global`.",
    "Weighted mean: `sum(n / N * d for n, d in zip(sizes, deltas))`.",
    "Return `global_w + server_lr * mean_delta` (a new array).",
],
"solution": r'''
import numpy as np


def client_delta(global_w, local_w):
    g = np.asarray(global_w, dtype=float)
    l = np.asarray(local_w, dtype=float)
    if g.shape != l.shape:
        raise ValueError("shape mismatch")
    return l - g


def server_update(global_w, deltas, sizes, server_lr=1.0):
    if not deltas or len(deltas) != len(sizes):
        raise ValueError("need one size per delta")
    total = float(sum(sizes))
    if total == 0:
        raise ValueError("total size is zero")
    g = np.asarray(global_w, dtype=float)
    mean = sum((n / total) * np.asarray(d, dtype=float) for n, d in zip(sizes, deltas))
    return g + server_lr * mean
''',
"explanation": r'''
Deltas are local minus global parameters. The server takes their size-weighted mean and steps in
that direction with its own learning rate; with rate 1 the result is algebraically identical to
FedAvg.
''',
"tests": r'''
import numpy as np

class TestDelta(unittest.TestCase):
    def test_delta(self):
        np.testing.assert_allclose(S.client_delta(np.array([1., 2.]), np.array([1.5, 0.])), [0.5, -2.])

    def test_server_lr(self):
        out = S.server_update(np.zeros(2), [np.array([1., 1.]), np.array([3., -1.])], [1, 1], server_lr=0.5)
        np.testing.assert_allclose(out, [1., 0.])

    def test_equals_fedavg(self):
        rng = np.random.default_rng(0)
        g = rng.normal(size=4); locals_ = [rng.normal(size=4) for _ in range(3)]; sizes = [5, 1, 14]
        deltas = [S.client_delta(g, l) for l in locals_]
        fedavg = sum(n * l for n, l in zip(sizes, locals_)) / sum(sizes)
        np.testing.assert_allclose(S.server_update(g, deltas, sizes), fedavg)

    def test_no_mutation(self):
        g = np.zeros(2)
        S.server_update(g, [np.ones(2)], [1])
        np.testing.assert_array_equal(g, [0, 0])

    def test_zero_lr(self):
        np.testing.assert_allclose(S.server_update(np.array([3.]), [np.array([9.])], [2], server_lr=0.0), [3.])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.client_delta(np.ones(2), np.ones(3))
        with self.assertRaises(ValueError):
            S.server_update(np.ones(2), [], [])
''',
"feedback": [
    ("test_delta", "Delta = local − global."),
    ("test_equals_fedavg", "Weight deltas by n_k/N; with server_lr = 1 you must reproduce FedAvg."),
    ("test_no_mutation", "Return a new array; don't use += on global_w."),
    ("test_server_lr", "Multiply the aggregated delta by server_lr."),
],
},
# ---------------------------------------------------------------- label-skew-partition
{
"slug": "label-skew-partition", "title": "Label-Skewed (non-IID) Partition",
"difficulty": "beginner", "prereqs": ["iid-partition"], "packages": ["numpy"],
"objectives": ["Build McMahan-style pathological non-IID shards", "Measure per-client label distributions",
               "Quantify heterogeneity"],
"tags": ["non-iid", "label-skew", "heterogeneity", "partitioning"],
"sources": ["S028", "S032"], "entry": "shard_partition(labels, n_clients, shards_per_client, seed); label_counts(labels, parts, n_classes)",
"article": r'''
# Non-IID Data: Label Skew

## Intuition
A phone keyboard user types mostly in one language; a hospital sees mostly certain conditions. Real
clients have very different data. A standard stress test gives each client only a couple of classes.

## Precise explanation (shard method of McMahan et al.)
1. Sort example indices by label (stable sort).
2. Cut the sorted list into `n_clients * shards_per_client` equal-ish shards (`np.array_split`).
3. Shuffle shard ids with `rng.permutation`, and give client k the shards at positions
   `k*s .. (k+1)*s - 1` of the shuffled list.
With 2 shards per client, most clients see only 1–2 labels. **Label counts** per client form a
`(n_clients, n_classes)` table; a simple heterogeneity summary is the average number of distinct
labels per client.

## Worked example
10 examples, labels 0..4 twice each, 5 clients × 1 shard → each client gets exactly one label.

## Common mistakes
* Unstable sorting (non-reproducible shard contents).
* Shards that cross class boundaries unintentionally (fine — that's realistic — but know it happens).
* Forgetting that skewed partitions slow FedAvg convergence ([[fedavg-training]]).

## Why this matters
Non-IID data is the defining challenge of FL and motivates FedProx ([[fedprox]]).
''',
"statement": r'''
Implement:
* `shard_partition(labels, n_clients, shards_per_client, seed)` → list of sorted index arrays
  following the recipe (stable `np.argsort(labels, kind="stable")`). Raise `ValueError` if there are
  fewer examples than shards.
* `label_counts(labels, parts, n_classes)` → int array `(n_clients, n_classes)`.

**Example**
```python
labels = np.array([0, 1, 2, 3, 4] * 2)
parts = shard_partition(labels, 5, 1, seed=0)
label_counts(labels, parts, 5).max(axis=1)   # [2, 2, 2, 2, 2] — every client holds one class
```
''',
"starter": r'''
import numpy as np


def shard_partition(labels, n_clients, shards_per_client, seed):
    pass


def label_counts(labels, parts, n_classes):
    pass
''',
"hints": [
    "`order = np.argsort(labels, kind='stable')`; `shards = np.array_split(order, n_clients * s)`.",
    "`ids = rng.permutation(len(shards))`; client k gets `ids[k*s:(k+1)*s]`.",
    "Counts: `np.bincount(labels[p], minlength=n_classes)` per part.",
],
"solution": r'''
import numpy as np


def shard_partition(labels, n_clients, shards_per_client, seed):
    labels = np.asarray(labels)
    n_shards = n_clients * shards_per_client
    if n_clients < 1 or shards_per_client < 1 or len(labels) < n_shards:
        raise ValueError("not enough examples for the requested shards")
    order = np.argsort(labels, kind="stable")
    shards = np.array_split(order, n_shards)
    ids = np.random.default_rng(seed).permutation(n_shards)
    s = shards_per_client
    return [np.sort(np.concatenate([shards[i] for i in ids[k * s:(k + 1) * s]])) for k in range(n_clients)]


def label_counts(labels, parts, n_classes):
    labels = np.asarray(labels)
    return np.array([np.bincount(labels[p], minlength=n_classes) for p in parts])
''',
"explanation": r'''
Sorting by label groups each class together, so contiguous shards contain one (or two) classes.
Randomly dealing shards to clients produces pathological label skew; `bincount` per client reveals
the resulting label distribution.
''',
"tests": r'''
import numpy as np

class TestShard(unittest.TestCase):
    def test_one_class_each(self):
        labels = np.array([0, 1, 2, 3, 4] * 2)
        C = S.label_counts(labels, S.shard_partition(labels, 5, 1, 0), 5)
        np.testing.assert_array_equal(C.max(axis=1), 2)
        np.testing.assert_array_equal((C > 0).sum(axis=1), 1)

    def test_cover(self):
        labels = np.random.default_rng(0).integers(0, 10, 300)
        parts = S.shard_partition(labels, 10, 2, 1)
        self.assertEqual(sorted(np.concatenate(parts).tolist()), list(range(300)))

    def test_skewed_vs_iid(self):
        labels = np.repeat(np.arange(10), 30)
        C = S.label_counts(labels, S.shard_partition(labels, 10, 2, 3), 10)
        self.assertLessEqual((C > 0).sum(axis=1).max(), 3)

    def test_recipe(self):
        labels = np.array([2, 0, 1, 0, 2, 1])
        order = np.argsort(labels, kind="stable")
        shards = np.array_split(order, 3)
        ids = np.random.default_rng(5).permutation(3)
        exp = [np.sort(shards[i]) for i in ids]
        for p, e in zip(S.shard_partition(labels, 3, 1, 5), exp):
            np.testing.assert_array_equal(p, e)

    def test_counts_shape(self):
        labels = np.array([0, 1, 1])
        self.assertEqual(S.label_counts(labels, [np.array([0]), np.array([1, 2])], 3).tolist(), [[1, 0, 0], [0, 2, 0]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.shard_partition(np.arange(3), 2, 2, 0)
''',
"feedback": [
    ("test_recipe", "Stable argsort by label, array_split into n_clients*s shards, deal shards by rng.permutation."),
    ("test_one_class_each", "Shards are contiguous slices of the label-sorted indices."),
    ("test_cover", "Every example must belong to exactly one client."),
    ("test_counts_shape", "Use np.bincount with minlength=n_classes per client."),
],
},
# ---------------------------------------------------------------- local-sgd
{
"slug": "local-sgd", "title": "Local SGD on a Client", "optional": True,
"difficulty": "intermediate", "prereqs": ["linreg-gradient-descent", "client-delta"], "packages": ["numpy"],
"objectives": ["Run several epochs of minibatch SGD on local data", "Shuffle reproducibly per epoch",
               "Return the local model without touching the global one"],
"tags": ["local-training", "sgd", "minibatch", "federated-learning"],
"sources": ["S028", "S013"], "entry": "mse_grad(w, X, y); local_sgd(w, X, y, lr, epochs, batch_size, seed)",
"article": r'''
# Local Training on a Client

## Intuition
In FedAvg each client does real work: several passes (epochs) of minibatch SGD on its own data,
starting from the global model. More local work means fewer communication rounds — the central idea
of McMahan et al.

## Precise explanation
For linear regression with loss $L(w) = \frac{1}{|B|}\sum_{i\in B}(x_i\cdot w - y_i)^2$ on a batch B:
$\nabla L = \frac{2}{|B|}X_B^\top(X_Bw - y_B)$ ([[linreg-gradient-descent]]).
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
too much local work causes **client drift** ([[fedprox]]).

## Worked example
With B = n and E = 1, local SGD is one full-batch gradient step: w − lr·∇L(w).

## Common mistakes
* Updating the caller's global array in place.
* Re-seeding inside the epoch loop (same order every epoch).
* Dividing by n instead of the batch size.

## Why this matters
This function is the "client" half of every FL simulation in the remaining problems.
''',
"statement": r'''
Implement:
* `mse_grad(w, X, y)` → gradient of the mean squared error on `(X, y)`.
* `local_sgd(w, X, y, lr, epochs, batch_size, seed)` → new weight array following the recipe exactly.
  Raise `ValueError` if `lr <= 0`, `epochs < 1` or `batch_size < 1`.

**Example**
```python
X = np.array([[1., 0.], [0., 1.]]); y = np.array([1., 2.])
local_sgd(np.zeros(2), X, y, lr=0.5, epochs=1, batch_size=2, seed=0)   # [0.5, 1.0]
```
''',
"starter": r'''
import numpy as np


def mse_grad(w, X, y):
    pass


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    pass
''',
"hints": [
    "`2 / len(y) * X.T @ (X @ w - y)`.",
    "`rng = np.random.default_rng(seed)` once, outside the epoch loop.",
    "`for s in range(0, n, batch_size): b = order[s:s + batch_size]`.",
],
"solution": r'''
import numpy as np


def mse_grad(w, X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    return 2.0 / len(y) * X.T @ (X @ w - y)


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    if lr <= 0 or epochs < 1 or batch_size < 1:
        raise ValueError("invalid lr, epochs or batch_size")
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.array(w, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(y)
    for _ in range(epochs):
        order = rng.permutation(n)
        for s in range(0, n, batch_size):
            b = order[s:s + batch_size]
            w = w - lr * mse_grad(w, X[b], y[b])
    return w
''',
"explanation": r'''
`np.array(w)` copies the global weights so the caller's array is untouched. One generator produces a
fresh permutation per epoch; each minibatch takes one gradient step with its own batch-mean gradient.
''',
"tests": r'''
import numpy as np

class TestLocalSGD(unittest.TestCase):
    def test_full_batch_one_step(self):
        X = np.array([[1., 0.], [0., 1.]]); y = np.array([1., 2.])
        np.testing.assert_allclose(S.local_sgd(np.zeros(2), X, y, 0.5, 1, 2, 0), [0.5, 1.0])

    def test_grad(self):
        X = np.array([[1., 2.], [3., 4.]]); y = np.array([1., 0.]); w = np.array([0.5, -0.5])
        np.testing.assert_allclose(S.mse_grad(w, X, y), 2 / 2 * X.T @ (X @ w - y))

    def test_recipe(self):
        rng0 = np.random.default_rng(1)
        X, y = rng0.normal(size=(7, 3)), rng0.normal(size=7)
        w = np.zeros(3); rng = np.random.default_rng(11)
        for _ in range(2):
            o = rng.permutation(7)
            for s in range(0, 7, 3):
                b = o[s:s + 3]; w = w - 0.05 * 2 / len(b) * X[b].T @ (X[b] @ w - y[b])
        np.testing.assert_allclose(S.local_sgd(np.zeros(3), X, y, 0.05, 2, 3, 11), w)

    def test_converges(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(100, 2)); y = X @ np.array([2., -1.])
        np.testing.assert_allclose(S.local_sgd(np.zeros(2), X, y, 0.05, 50, 10, 0), [2., -1.], atol=1e-6)

    def test_no_mutation(self):
        w = np.zeros(2)
        S.local_sgd(w, np.eye(2), np.ones(2), 0.1, 1, 1, 0)
        np.testing.assert_array_equal(w, [0, 0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.local_sgd(np.zeros(2), np.eye(2), np.ones(2), 0.1, 0, 1, 0)
''',
"feedback": [
    ("test_recipe", "Create the generator once; new permutation each epoch; batch-mean gradient per step."),
    ("test_full_batch_one_step", "Gradient is 2/|B| · Xᵀ(Xw − y)."),
    ("test_no_mutation", "Copy w before updating (np.array(w))."),
    ("test_converges", "The last batch of an epoch may be smaller — include it."),
],
},
# ---------------------------------------------------------------- fedavg-round
{
"slug": "fedavg-round", "title": "One FedAvg Round",
"difficulty": "intermediate", "prereqs": ["weighted-fedavg", "fl-torch-local-training"], "packages": ["numpy"],
"objectives": ["Broadcast the global model, train locally, aggregate", "Use distinct reproducible seeds per client",
               "Relate one-epoch full-batch FedAvg to centralised gradient descent"],
"tags": ["fedavg", "communication-round", "federated-learning"],
"sources": ["S028"], "entry": "fedavg_round(global_w, clients, lr, epochs, batch_size, seed)",
"article": r'''
# One Round of FedAvg

## Intuition
A round is: the server sends the current model to the selected clients; each trains locally; they
send models back; the server averages them weighted by data size.

## Precise explanation
```mermaid
sequenceDiagram
  participant S as Server
  participant C1 as Client 1
  participant C2 as Client 2
  S->>C1: global w
  S->>C2: global w
  C1->>C1: local SGD (E epochs)
  C2->>C2: local SGD (E epochs)
  C1->>S: w1, n1
  C2->>S: w2, n2
  S->>S: w = Σ n_k w_k / N
```
Client k uses seed `seed + k` so runs are reproducible but clients shuffle differently.
**Sanity check:** with E = 1 and full-batch local training (B = n_k), one FedAvg round equals one
step of centralised gradient descent on the pooled data, because the size-weighted average of local
gradients is the global gradient.

## Worked example
Two clients with identical data → identical local models → the average equals either one.

## Common mistakes
* Letting client k start from client k−1's model (must all start from the same global w).
* Using the same seed for every client.
* Unweighted averaging.

## Why this matters
This is FedAvg; [[fedavg-training]] loops it with client sampling.
''',
"statement": r'''
Write `fedavg_round(global_w, clients, lr, epochs, batch_size, seed)` returning
`(new_global, local_models)`. Each client `k` (tuple `(X, y)`) runs `local_sgd` ([[local-sgd]] recipe, include
your own copy) from `global_w` with seed `seed + k`; aggregate with weights `len(y_k)`. `batch_size`
may be `None` meaning full batch (`len(y_k)`). Raise `ValueError` for an empty client list.

**Example**
```python
new_w, locals_ = fedavg_round(np.zeros(2), clients, lr=0.1, epochs=1, batch_size=None, seed=0)
# equals one centralised GD step on all data
```
''',
"starter": r'''
import numpy as np


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    # copy your [[local-sgd]] implementation here
    pass


def fedavg_round(global_w, clients, lr, epochs, batch_size, seed):
    pass
''',
"hints": [
    "Loop `for k, (X, y) in enumerate(clients)`.",
    "`bs = len(y) if batch_size is None else batch_size`.",
    "Aggregate: `sum(n * w for n, w in zip(sizes, locals_)) / sum(sizes)`.",
],
"solution": r'''
import numpy as np


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    if lr <= 0 or epochs < 1 or batch_size < 1:
        raise ValueError("invalid lr, epochs or batch_size")
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


def fedavg_round(global_w, clients, lr, epochs, batch_size, seed):
    if not clients:
        raise ValueError("need at least one client")
    locals_, sizes = [], []
    for k, (X, y) in enumerate(clients):
        bs = len(y) if batch_size is None else batch_size
        locals_.append(local_sgd(global_w, X, y, lr, epochs, bs, seed + k))
        sizes.append(len(y))
    total = float(sum(sizes))
    new_global = sum((n / total) * w for n, w in zip(sizes, locals_))
    return new_global, locals_
''',
"explanation": r'''
Every client starts from the same broadcast weights and trains with its own seed. The server
combines the returned models by data-size-weighted averaging. With one full-batch epoch, the weighted
average of one-step updates equals a single gradient step on the pooled data.
''',
"tests": r'''
import numpy as np

rng0 = np.random.default_rng(0)
CL = [(rng0.normal(size=(n, 2)), rng0.normal(size=n)) for n in (5, 12, 3)]

class TestRound(unittest.TestCase):
    def test_equals_centralised_step(self):
        w0 = np.array([0.3, -0.2])
        new, _ = S.fedavg_round(w0, CL, 0.1, 1, None, 0)
        X = np.vstack([c[0] for c in CL]); y = np.concatenate([c[1] for c in CL])
        np.testing.assert_allclose(new, w0 - 0.1 * 2 / len(y) * X.T @ (X @ w0 - y))

    def test_locals_count(self):
        _, locs = S.fedavg_round(np.zeros(2), CL, 0.05, 2, 2, 1)
        self.assertEqual(len(locs), 3)

    def test_seeds_per_client(self):
        w0 = np.zeros(2)
        _, locs = S.fedavg_round(w0, CL, 0.05, 2, 2, 7)
        for k, (X, y) in enumerate(CL):
            np.testing.assert_allclose(locs[k], S.local_sgd(w0, X, y, 0.05, 2, 2, 7 + k))

    def test_identical_clients(self):
        c = (np.eye(2), np.array([1., 2.]))
        new, locs = S.fedavg_round(np.zeros(2), [c, c], 0.1, 3, 1, 0)
        self.assertEqual(new.shape, (2,))
        np.testing.assert_allclose(new, (locs[0] + locs[1]) / 2)

    def test_weighting(self):
        new, locs = S.fedavg_round(np.zeros(2), CL, 0.05, 1, 2, 3)
        np.testing.assert_allclose(new, (5 * locs[0] + 12 * locs[1] + 3 * locs[2]) / 20)

    def test_global_unchanged(self):
        g = np.zeros(2)
        S.fedavg_round(g, CL, 0.1, 1, None, 0)
        np.testing.assert_array_equal(g, [0, 0])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.fedavg_round(np.zeros(2), [], 0.1, 1, None, 0)
''',
"feedback": [
    ("test_equals_centralised_step", "All clients must start from global_w; aggregate with weights n_k/N."),
    ("test_seeds_per_client", "Client k uses seed + k."),
    ("test_weighting", "Weight each local model by its client's number of samples."),
    ("test_global_unchanged", "Never modify global_w in place."),
],
},
# ---------------------------------------------------------------- client-sampling
{
"slug": "client-sampling", "title": "Seeded Client Sampling",
"difficulty": "intermediate", "prereqs": ["fedavg-round"], "packages": ["numpy"],
"objectives": ["Select a fraction C of clients per round without replacement",
               "Make each round's selection reproducible", "Check participation rates over many rounds"],
"tags": ["client-sampling", "participation", "cross-device"],
"sources": ["S028", "S032"], "entry": "sample_clients(n_clients, fraction, seed, round_idx)",
"article": r'''
# Client Sampling

## Intuition
In cross-device FL (millions of phones) only a small fraction of clients participate in each round —
those that are charging, idle and on Wi-Fi. Simulations model this by sampling a fraction C of
clients per round.

## Precise explanation
* Number per round: $m = \max(1, \operatorname{round}(C\cdot K))$ (McMahan et al. use $\max(\lceil
  CK\rceil, 1)$; we use round — a design choice — and test it).
* Sample without replacement and sort for readability.
* Reproducibility per round: seed the generator with `(seed, round_idx)` —
  `np.random.default_rng([seed, round_idx])` — so round 7 always selects the same clients regardless
  of how many earlier rounds were simulated.
* Over many rounds each client participates with frequency ≈ m/K.
Cross-silo FL (a few hospitals) often uses all clients every round (C = 1).

## Worked example
K = 10, C = 0.3 → 3 clients per round, e.g. [1, 4, 8].

## Common mistakes
* Sampling with replacement (the same client twice).
* m = 0 for tiny fractions.
* One global RNG whose state depends on the simulation history.

## Why this matters
Partial participation is a key source of noise and bias in FL; [[fedavg-training]] uses this sampler.
''',
"statement": r'''
Write `sample_clients(n_clients, fraction, seed, round_idx)` → sorted int array of
`max(1, round(fraction * n_clients))` distinct client ids, chosen with
`np.random.default_rng([seed, round_idx]).choice(n_clients, m, replace=False)`.
Raise `ValueError` unless `0 < fraction <= 1` and `n_clients >= 1`.

**Example**
```python
s = sample_clients(10, 0.3, seed=0, round_idx=0)
len(s), len(set(s.tolist()))     # (3, 3)
sample_clients(10, 1.0, 0, 5)    # array([0, 1, ..., 9])
```
''',
"starter": r'''
import numpy as np


def sample_clients(n_clients, fraction, seed, round_idx):
    pass
''',
"hints": [
    "`m = max(1, round(fraction * n_clients))`.",
    "`rng = np.random.default_rng([seed, round_idx])`.",
    "`np.sort(rng.choice(n_clients, m, replace=False))`.",
],
"solution": r'''
import numpy as np


def sample_clients(n_clients, fraction, seed, round_idx):
    if n_clients < 1 or not 0 < fraction <= 1:
        raise ValueError("need n_clients >= 1 and 0 < fraction <= 1")
    m = max(1, round(fraction * n_clients))
    rng = np.random.default_rng([seed, round_idx])
    return np.sort(rng.choice(n_clients, m, replace=False))
''',
"explanation": r'''
The per-round seed sequence `[seed, round_idx]` gives an independent, reproducible stream for every
round. Sampling without replacement guarantees distinct clients, and the count rule never returns zero.
''',
"tests": r'''
import numpy as np

class TestSampling(unittest.TestCase):
    def test_count_distinct(self):
        s = S.sample_clients(10, 0.3, 0, 0)
        self.assertEqual(len(s), 3)
        self.assertEqual(len(set(s.tolist())), 3)

    def test_full(self):
        np.testing.assert_array_equal(S.sample_clients(10, 1.0, 0, 5), np.arange(10))

    def test_min_one(self):
        self.assertEqual(len(S.sample_clients(100, 0.001, 1, 0)), 1)

    def test_recipe_and_round_independence(self):
        exp = np.sort(np.random.default_rng([3, 7]).choice(20, 5, replace=False))
        np.testing.assert_array_equal(S.sample_clients(20, 0.25, 3, 7), exp)

    def test_sorted_range(self):
        s = S.sample_clients(50, 0.2, 2, 4)
        self.assertTrue((np.diff(s) > 0).all() and s.min() >= 0 and s.max() < 50)

    def test_participation_rate(self):
        counts = np.zeros(10)
        for r in range(3000):
            counts[S.sample_clients(10, 0.3, 0, r)] += 1
        np.testing.assert_allclose(counts / 3000, 0.3, atol=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.sample_clients(10, 0.0, 0, 0)
''',
"feedback": [
    ("test_recipe_and_round_independence", "Seed with default_rng([seed, round_idx]) and use choice(..., replace=False)."),
    ("test_min_one", "Always select at least one client."),
    ("test_count_distinct", "Sample without replacement."),
    ("test_participation_rate", "Each round must be an independent draw."),
],
},
# ---------------------------------------------------------------- update-clipping
{
"slug": "update-clipping", "title": "Clipping Client Updates",
"difficulty": "intermediate", "prereqs": ["client-delta"], "packages": ["numpy"],
"objectives": ["Clip update vectors to a maximum L2 norm", "Preserve direction while bounding magnitude",
               "Report how many clients were clipped"],
"tags": ["clipping", "robustness", "privacy", "norms"],
"sources": ["S031", "S032"], "entry": "clip_update(delta, max_norm); clip_all(deltas, max_norm)",
"article": r'''
# Clipping Client Updates

## Intuition
One faulty or malicious client could send an enormous update and wreck the global model. Clipping
caps every update's length while keeping its direction — and it bounds how much any single client
can influence the aggregate, which differential privacy needs ([[dp-aggregation]]).

## Precise explanation
$$\text{clip}(\Delta, C) = \Delta \cdot \min\!\left(1, \frac{C}{\lVert\Delta\rVert_2}\right).$$
Updates already within the norm are unchanged; larger ones are scaled down to norm exactly C. The
zero vector stays zero. McMahan et al. (2017) clip per-user updates this way for user-level DP.
After clipping, replacing one client's update changes a *sum* of updates by at most $2C$.

## Worked example
Δ = [3, 4] (norm 5), C = 2.5 → [1.5, 2.0] (norm 2.5). Δ = [0.3, 0.4], C = 2.5 → unchanged.

## Common mistakes
* Clipping each coordinate separately (changes direction).
* Division by zero for a zero update.
* Clipping after aggregation (doesn't bound individual influence).

## Why this matters
Clipping is standard in DP-SGD/DP-FedAvg and a simple robustness measure.
''',
"statement": r'''
Implement:
* `clip_update(delta, max_norm)` → clipped new array; raise `ValueError` if `max_norm <= 0`.
* `clip_all(deltas, max_norm)` → `(clipped_list, n_clipped)` where `n_clipped` counts updates whose
  norm exceeded `max_norm`.

**Example**
```python
clip_update(np.array([3., 4.]), 2.5)     # [1.5, 2. ]
clip_all([np.array([3., 4.]), np.array([0.3, 0.4])], 2.5)[1]   # 1
```
''',
"starter": r'''
import numpy as np


def clip_update(delta, max_norm):
    pass


def clip_all(deltas, max_norm):
    pass
''',
"hints": [
    "`n = np.linalg.norm(delta)`.",
    "Scale factor `min(1.0, max_norm / n)` when `n > 0`.",
    "Count with `sum(np.linalg.norm(d) > max_norm for d in deltas)`.",
],
"solution": r'''
import numpy as np


def clip_update(delta, max_norm):
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")
    d = np.asarray(delta, dtype=float)
    n = float(np.linalg.norm(d))
    if n <= max_norm:
        return d.copy()
    return d * (max_norm / n)


def clip_all(deltas, max_norm):
    clipped = [clip_update(d, max_norm) for d in deltas]
    n_clipped = sum(1 for d in deltas if np.linalg.norm(d) > max_norm)
    return clipped, int(n_clipped)
''',
"explanation": r'''
Updates inside the ball are returned unchanged (as copies); larger ones are rescaled to lie exactly
on the sphere of radius max_norm, preserving direction. The zero vector falls in the first branch,
avoiding division by zero.
''',
"tests": r'''
import numpy as np

class TestClip(unittest.TestCase):
    def test_clip(self):
        np.testing.assert_allclose(S.clip_update(np.array([3., 4.]), 2.5), [1.5, 2.0])

    def test_unchanged(self):
        np.testing.assert_allclose(S.clip_update(np.array([0.3, 0.4]), 2.5), [0.3, 0.4])

    def test_zero(self):
        np.testing.assert_array_equal(S.clip_update(np.zeros(3), 1.0), np.zeros(3))

    def test_norm_and_direction(self):
        d = np.random.default_rng(0).normal(size=10) * 10
        c = S.clip_update(d, 1.0)
        self.assertAlmostEqual(np.linalg.norm(c), 1.0)
        self.assertAlmostEqual(c @ d / (np.linalg.norm(c) * np.linalg.norm(d)), 1.0)

    def test_clip_all(self):
        cl, n = S.clip_all([np.array([3., 4.]), np.array([0.3, 0.4]), np.array([0., 10.])], 2.5)
        self.assertEqual(n, 2)
        self.assertTrue(all(np.linalg.norm(c) <= 2.5 + 1e-12 for c in cl))

    def test_sensitivity(self):
        rng = np.random.default_rng(1)
        ds = [rng.normal(size=4) * 5 for _ in range(5)]
        a = sum(S.clip_all(ds, 1.0)[0])
        ds2 = ds[:-1] + [rng.normal(size=4) * 100]
        b = sum(S.clip_all(ds2, 1.0)[0])
        self.assertLessEqual(np.linalg.norm(a - b), 2.0 + 1e-12)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.clip_update(np.ones(2), 0)
''',
"feedback": [
    ("test_clip", "Scale by max_norm / ‖Δ‖ when the norm is too large."),
    ("test_norm_and_direction", "Scale the whole vector; don't clip coordinates independently."),
    ("test_zero", "The zero vector must stay zero without dividing by zero."),
    ("test_clip_all", "Count updates with norm strictly greater than max_norm."),
],
},
# ---------------------------------------------------------------- fedavg-training
{
"slug": "fedavg-training", "title": "Full FedAvg Training Loop",
"difficulty": "advanced", "prereqs": ["fedavg-round", "client-sampling"], "packages": ["numpy"],
"objectives": ["Combine sampling, local training and aggregation over many rounds",
               "Track global loss per round", "Compare IID and non-IID convergence"],
"tags": ["fedavg", "training-loop", "convergence", "non-iid"],
"sources": ["S028", "S032"], "entry": "global_loss(w, clients); train_fedavg(clients, w0, rounds, fraction, lr, epochs, batch_size, seed)",
"article": r'''
# The Full FedAvg Algorithm

## Intuition
Repeat FedAvg rounds with a random subset of clients each time. Watch the global loss fall, using far
fewer communication rounds than one-gradient-step-per-round SGD would need.

## Precise explanation
```text
w = w0
for t in 0..R-1:
    S_t = sample_clients(K, C, seed, t)                 # [[client-sampling]]
    for k in S_t: w_k = local_sgd(w, data_k, lr, E, B, seed*1000 + t*K + k)   # [[local-sgd]]
    w = Σ_{k∈S_t} n_k w_k / Σ_{k∈S_t} n_k               # [[weighted-fedavg]] over participants only
    record global_loss(w)
```
**Global loss** = size-weighted mean of client MSEs = MSE on the pooled data.
On IID data FedAvg converges quickly; on label/feature-skewed data local models drift apart and
progress slows or oscillates (McMahan et al.; FL survey), motivating FedProx ([[fedprox]]).

<svg xmlns="http://www.w3.org/2000/svg" width="270" height="150" viewBox="0 0 270 150" role="img" aria-label="Two decreasing loss curves over rounds; the IID curve drops faster than the non-IID curve">
<title>FedAvg loss curves</title>
<line x1="30" y1="130" x2="260" y2="130" stroke="#999"/><line x1="30" y1="130" x2="30" y2="10" stroke="#999"/>
<path d="M 30 20 C 60 90, 90 115, 250 122" fill="none" stroke="#1f77b4" stroke-width="2"/>
<path d="M 30 20 C 80 50, 130 85, 250 108" fill="none" stroke="#d62728" stroke-width="2" stroke-dasharray="5 3"/>
<text x="180" y="112" font-size="11" fill="#1f77b4">IID</text><text x="180" y="88" font-size="11" fill="#d62728">non-IID</text>
<text x="120" y="146" font-size="11">round</text>
</svg>

*Figure (original, schematic): typical global loss curves.*

## Worked example
3 clients holding noise-free data from y = 2x₀ − x₁ converge to w ≈ [2, −1].

## Common mistakes
* Averaging over all clients instead of the sampled ones.
* Evaluating loss only on participants.
* Reusing one seed for every client and round.

## Why this matters
This is the end-to-end algorithm deployed in production FL systems (with many engineering additions).
''',
"statement": r'''
Implement:
* `global_loss(w, clients)` → MSE over all clients' data combined.
* `train_fedavg(clients, w0, rounds, fraction, lr, epochs, batch_size, seed)` → `(w, history)` following
  the pseudocode exactly (include your own copies of `sample_clients` and `local_sgd`; `batch_size`
  `None` = full batch). `history[t]` is the global loss after round t.

**Example**
```python
w, hist = train_fedavg(clients, np.zeros(2), rounds=30, fraction=1.0, lr=0.1, epochs=2, batch_size=4, seed=0)
hist[-1] < hist[0]     # True
```
''',
"starter": r'''
import numpy as np


def sample_clients(n_clients, fraction, seed, round_idx):
    pass  # from [[client-sampling]]


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    pass  # from [[local-sgd]]


def global_loss(w, clients):
    pass


def train_fedavg(clients, w0, rounds, fraction, lr, epochs, batch_size, seed):
    pass
''',
"hints": [
    "Global loss: total squared error over all clients / total samples.",
    "Client seed: `seed * 1000 + t * K + k`.",
    "Aggregate only over `S_t` with weights `len(y_k)`.",
],
"solution": r'''
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
''',
"explanation": r'''
Each round samples participants, trains each from the current global model with a unique seed,
aggregates only the participants' models by size, and evaluates the loss on all clients' data. The
seed scheme makes every run fully reproducible.
''',
"tests": r'''
import numpy as np

def make_clients(skew=False, seed=0):
    rng = np.random.default_rng(seed)
    cl = []
    for k in range(5):
        if skew:
            X = np.column_stack([rng.normal(k - 2, 0.3, 20), rng.normal(2 - k, 0.3, 20)])
        else:
            X = rng.normal(size=(20, 2))
        cl.append((X, X @ np.array([2., -1.])))
    return cl

class TestFedAvgTrain(unittest.TestCase):
    def test_global_loss(self):
        cl = [(np.eye(2), np.array([1., 0.])), (np.array([[1., 1.]]), np.array([3.]))]
        self.assertAlmostEqual(S.global_loss(np.zeros(2), cl), (1 + 0 + 9) / 3)

    def test_converges_iid(self):
        w, h = S.train_fedavg(make_clients(), np.zeros(2), 40, 1.0, 0.05, 2, 5, 0)
        np.testing.assert_allclose(w, [2, -1], atol=1e-4)
        self.assertLess(h[-1], 1e-6)

    def test_partial_participation(self):
        w, h = S.train_fedavg(make_clients(), np.zeros(2), 80, 0.4, 0.05, 1, 5, 1)
        self.assertEqual(len(h), 80)
        self.assertLess(h[-1], 1e-3 * h[0])

    def test_reproducible(self):
        a = S.train_fedavg(make_clients(), np.zeros(2), 5, 0.6, 0.05, 1, 4, 3)
        b = S.train_fedavg(make_clients(), np.zeros(2), 5, 0.6, 0.05, 1, 4, 3)
        np.testing.assert_array_equal(a[0], b[0])

    def test_first_round_matches_manual(self):
        cl = make_clients()
        w, h = S.train_fedavg(cl, np.zeros(2), 1, 0.4, 0.05, 1, 5, 2)
        chosen = S.sample_clients(5, 0.4, 2, 0)
        locs = [S.local_sgd(np.zeros(2), *cl[k], 0.05, 1, 5, 2 * 1000 + 0 * 5 + int(k)) for k in chosen]
        np.testing.assert_allclose(w, sum(locs) / len(locs))

    def test_noniid_still_learns(self):
        _, h = S.train_fedavg(make_clients(skew=True), np.zeros(2), 60, 1.0, 0.02, 3, 5, 0)
        self.assertLess(h[-1], h[0])
''',
"feedback": [
    ("test_first_round_matches_manual", "Use seed*1000 + t*K + k for client k in round t and average only sampled clients."),
    ("test_global_loss", "Global loss = total squared error / total number of samples."),
    ("test_converges_iid", "Every round must start local training from the current global w."),
    ("test_reproducible", "All randomness must come from seeded generators."),
],
},
# ---------------------------------------------------------------- secure-aggregation
{
"slug": "secure-aggregation", "title": "Secure Aggregation with Pairwise Masks",
"difficulty": "advanced", "prereqs": ["weighted-fedavg"], "packages": ["numpy"],
"objectives": ["Generate cancelling pairwise masks from shared seeds", "Recover the exact sum of updates without seeing any single update",
               "Recover the sum when a client drops out by removing its pairwise masks"],
"tags": ["secure-aggregation", "privacy", "masking", "cryptography-concepts"],
"sources": ["S029", "S032"], "entry": "pair_mask(i, j, dim, base_seed); mask_update(i, update, n_clients, base_seed); aggregate(masked, n_clients, dim, base_seed, dropped=())",
"article": r'''
# Secure Aggregation (simplified)

## Intuition
The server should learn only the *sum* of client updates, never an individual update. Each pair of
clients agrees on a random mask; one adds it, the other subtracts it. Every masked update looks like
noise, but in the sum all masks cancel.

## Precise explanation (core idea of Bonawitz et al., 2017)
For clients $i < j$ with a shared seed $s_{ij}$, mask $m_{ij} = \text{PRG}(s_{ij})$ (a random vector).
Client i sends
$$y_i = x_i + \sum_{j > i} m_{ij} - \sum_{j < i} m_{ji}.$$
Then $\sum_i y_i = \sum_i x_i$ because each $m_{ij}$ appears once with + and once with −.
**Dropouts:** if client d never sends $y_d$, the masks between d and the survivors no longer cancel.
In the real protocol survivors reveal secret shares that let the server reconstruct $s_{dj}$; here we
simulate that by letting the server regenerate those pairwise masks and remove them.
Simplifications in this exercise: seeds are derived deterministically from `(base_seed, i, j)` instead
of Diffie–Hellman key agreement, masks are real-valued Gaussian vectors instead of integers modulo a
large number, and there is no secret sharing — so this is **not secure**, only a faithful model of the
cancellation arithmetic.

## Worked example
x₀ = [1], x₁ = [2], m₀₁ = [5]: y₀ = [6], y₁ = [−3]; sum [3] = x₀ + x₁ ✓.

## Common mistakes
* Both clients adding the mask (no cancellation).
* Seeding masks per client instead of per pair.
* Forgetting the dropped client's pairs, leaving a random error in the sum.

## Why this matters
Secure aggregation lets FL provide privacy against an honest-but-curious server and is often combined
with differential privacy ([[dp-aggregation]]).
''',
"statement": r'''
Implement:
* `pair_mask(i, j, dim, base_seed)` → for `i < j`, `np.random.default_rng([base_seed, i, j]).normal(size=dim)`
  (raise `ValueError` if `i >= j`).
* `mask_update(i, update, n_clients, base_seed)` → masked vector per the formula.
* `aggregate(masked, n_clients, dim, base_seed, dropped=())` → `masked` is a dict client id → masked
  vector for **surviving** clients; `dropped` lists ids that sent nothing. Return the sum of the
  survivors' true updates: sum the masked vectors, then for each dropped d and each survivor s remove
  the unmatched mask (if `s < d` the survivor added `m_sd`; if `s > d` it subtracted `m_ds`).

**Example**
```python
ups = [np.array([1., 2.]), np.array([3., 4.]), np.array([5., 6.])]
masked = {i: mask_update(i, ups[i], 3, base_seed=7) for i in range(3)}
aggregate(masked, 3, 2, 7)                                    # ≈ [9., 12.]
aggregate({0: masked[0], 2: masked[2]}, 3, 2, 7, dropped=[1])  # ≈ [6., 8.]
```
''',
"starter": r'''
import numpy as np


def pair_mask(i, j, dim, base_seed):
    pass


def mask_update(i, update, n_clients, base_seed):
    pass


def aggregate(masked, n_clients, dim, base_seed, dropped=()):
    pass
''',
"hints": [
    "In `mask_update`, loop `j` over all other clients: add `pair_mask(i, j)` if `j > i`, subtract `pair_mask(j, i)` if `j < i`.",
    "Sum the survivors' masked vectors.",
    "For dropped d and survivor s: subtract `pair_mask(s, d)` if `s < d`, add `pair_mask(d, s)` if `s > d`.",
],
"solution": r'''
import numpy as np


def pair_mask(i, j, dim, base_seed):
    if i >= j:
        raise ValueError("pair_mask requires i < j")
    return np.random.default_rng([base_seed, i, j]).normal(size=dim)


def mask_update(i, update, n_clients, base_seed):
    y = np.array(update, dtype=float)
    dim = y.shape[0]
    for j in range(n_clients):
        if j > i:
            y = y + pair_mask(i, j, dim, base_seed)
        elif j < i:
            y = y - pair_mask(j, i, dim, base_seed)
    return y


def aggregate(masked, n_clients, dim, base_seed, dropped=()):
    total = np.zeros(dim)
    for v in masked.values():
        total = total + np.asarray(v, dtype=float)
    for d in dropped:
        for s in masked:
            if s < d:
                total = total - pair_mask(s, d, dim, base_seed)
            elif s > d:
                total = total + pair_mask(d, s, dim, base_seed)
    return total
''',
"explanation": r'''
Each pair's mask enters one client's message with + and the other's with −, so they cancel in the
sum. When a client drops, its partners' masks with it are left uncancelled; regenerating exactly
those pairwise masks and removing them recovers the survivors' true sum.
''',
"tests": r'''
import numpy as np

UPS = [np.array([1., 2.]), np.array([3., 4.]), np.array([5., 6.])]

class TestSecAgg(unittest.TestCase):
    def test_full_sum(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in range(3)}
        np.testing.assert_allclose(S.aggregate(masked, 3, 2, 7), [9., 12.], atol=1e-10)

    def test_individual_hidden(self):
        for i in range(3):
            self.assertGreater(np.linalg.norm(S.mask_update(i, UPS[i], 3, 7) - UPS[i]), 0.1)

    def test_dropout(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in (0, 2)}
        np.testing.assert_allclose(S.aggregate(masked, 3, 2, 7, dropped=[1]), [6., 8.], atol=1e-10)

    def test_dropout_uncorrected_is_wrong(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in (0, 2)}
        self.assertGreater(np.linalg.norm(S.aggregate(masked, 3, 2, 7) - np.array([6., 8.])), 1e-3)

    def test_many_clients_two_drops(self):
        rng = np.random.default_rng(0)
        ups = [rng.normal(size=5) for _ in range(8)]
        alive = [0, 1, 3, 4, 6, 7]
        masked = {i: S.mask_update(i, ups[i], 8, 11) for i in alive}
        np.testing.assert_allclose(S.aggregate(masked, 8, 5, 11, dropped=[2, 5]), sum(ups[i] for i in alive), atol=1e-9)

    def test_pair_mask(self):
        np.testing.assert_allclose(S.pair_mask(1, 4, 3, 9), np.random.default_rng([9, 1, 4]).normal(size=3))
        with self.assertRaises(ValueError):
            S.pair_mask(2, 2, 3, 0)

    def test_single_client_no_mask(self):
        np.testing.assert_allclose(S.mask_update(0, np.array([1., 2.]), 1, 0), [1., 2.])
''',
"feedback": [
    ("test_full_sum", "Client i adds m_ij for j > i and subtracts m_ji for j < i."),
    ("test_dropout", "For each dropped d, remove the masks between d and every survivor with the right sign."),
    ("test_pair_mask", "Seed each pair with default_rng([base_seed, i, j]) for i < j."),
    ("test_individual_hidden", "Masked updates should look nothing like the raw updates."),
],
},
# ---------------------------------------------------------------- dp-aggregation
{
"slug": "dp-aggregation", "title": "Differentially Private Aggregation",
"difficulty": "advanced", "prereqs": ["update-clipping", "weighted-fedavg"], "packages": ["numpy"],
"objectives": ["Clip per-client updates and average them", "Add calibrated Gaussian noise (noise multiplier × clip / m)",
               "Measure the privacy–utility trade-off empirically"],
"tags": ["differential-privacy", "gaussian-mechanism", "clipping", "dp-fedavg"],
"sources": ["S031", "S032"], "entry": "dp_mean(deltas, clip_norm, noise_multiplier, rng)",
"article": r'''
# DP-style Aggregation: Clip, Average, Add Noise

## Intuition
Even aggregated updates can leak information about one client's data. Differential privacy (DP)
limits that leakage: clip each client's influence, then add random noise large enough to hide any
single contribution.

## Precise explanation (Gaussian mechanism as used by DP-FedAvg, McMahan et al., 2017)
For m participating clients with updates $\Delta_k$:
1. Clip: $\tilde\Delta_k = \text{clip}(\Delta_k, C)$ ([[update-clipping]]).
2. Average: $\bar\Delta = \frac1m\sum_k\tilde\Delta_k$. Replacing one client changes this by at most
   $2C/m$ (L2 sensitivity of the *replace-one* neighbour definition; $C/m$ for add/remove).
3. Noise: $\bar\Delta + \mathcal N(0, \sigma^2 I)$ with $\sigma = z\cdot C/m$, where z is the
   **noise multiplier**.
Larger z → stronger privacy, noisier model. Converting z, sampling rate and rounds into a formal
(ε, δ) guarantee requires a privacy accountant (out of scope here; the paper and the FL survey
discuss it). This exercise implements the mechanism, not the accounting.

## Worked example
Updates [3, 4] and [0.3, 0.4], C = 1 → clipped [0.6, 0.8] and [0.3, 0.4] → mean [0.45, 0.6];
with z = 0 that is the result; with z = 1 the noise std is 1·1/2 = 0.5 per coordinate.

## Common mistakes
* Noise scale using the number of all clients instead of participants.
* Adding noise before clipping.
* Claiming an ε without an accountant.

## Why this matters
DP aggregation is how deployed FL systems give formal privacy guarantees.
''',
"statement": r'''
Write `dp_mean(deltas, clip_norm, noise_multiplier, rng)` returning `(noisy_mean, clipped_mean, sigma)`:
clip each delta to `clip_norm` ([[update-clipping]] rule), average, and add `rng.normal(0, sigma, size=dim)` with
`sigma = noise_multiplier * clip_norm / m`. With `noise_multiplier == 0` do **not** draw noise
(return the clipped mean). Raise `ValueError` for empty deltas, `clip_norm <= 0` or
`noise_multiplier < 0`.

**Example**
```python
noisy, clean, sigma = dp_mean([np.array([3., 4.]), np.array([0.3, 0.4])], 1.0, 0.0, np.random.default_rng(0))
clean, sigma    # ([0.45, 0.6], 0.0)
```
''',
"starter": r'''
import numpy as np


def dp_mean(deltas, clip_norm, noise_multiplier, rng):
    pass
''',
"hints": [
    "Clip: `d * min(1, C / ‖d‖)` (guard the zero vector).",
    "`clipped_mean = np.mean(clipped, axis=0)`; `sigma = z * C / len(deltas)`.",
    "Only call `rng.normal` when `sigma > 0`.",
],
"solution": r'''
import numpy as np


def _clip(d, c):
    d = np.asarray(d, dtype=float)
    n = float(np.linalg.norm(d))
    return d if n <= c else d * (c / n)


def dp_mean(deltas, clip_norm, noise_multiplier, rng):
    if not deltas or clip_norm <= 0 or noise_multiplier < 0:
        raise ValueError("invalid arguments")
    clipped = np.array([_clip(d, clip_norm) for d in deltas])
    clean = clipped.mean(axis=0)
    sigma = noise_multiplier * clip_norm / len(deltas)
    if sigma == 0:
        return clean.copy(), clean, 0.0
    return clean + rng.normal(0.0, sigma, size=clean.shape), clean, float(sigma)
''',
"explanation": r'''
Clipping bounds each client's contribution; averaging over m clients divides the sensitivity by m;
Gaussian noise with standard deviation z·C/m is then added to the mean. Skipping the draw when σ = 0
keeps the noiseless path exact and leaves the generator untouched.
''',
"tests": r'''
import numpy as np

class TestDP(unittest.TestCase):
    def test_no_noise(self):
        noisy, clean, s = S.dp_mean([np.array([3., 4.]), np.array([0.3, 0.4])], 1.0, 0.0, np.random.default_rng(0))
        np.testing.assert_allclose(clean, [0.45, 0.6])
        np.testing.assert_allclose(noisy, clean)
        self.assertEqual(s, 0.0)

    def test_sigma(self):
        _, _, s = S.dp_mean([np.ones(3)] * 4, 2.0, 1.5, np.random.default_rng(0))
        self.assertAlmostEqual(s, 1.5 * 2.0 / 4)

    def test_noise_recipe(self):
        ds = [np.array([1., 0.]), np.array([0., 1.])]
        noisy, clean, s = S.dp_mean(ds, 5.0, 1.0, np.random.default_rng(3))
        np.testing.assert_allclose(noisy, clean + np.random.default_rng(3).normal(0, s, size=2))

    def test_noise_statistics(self):
        rng = np.random.default_rng(1)
        ds = [np.zeros(20000)] * 10
        noisy, _, s = S.dp_mean(ds, 1.0, 2.0, rng)
        self.assertAlmostEqual(noisy.std(), s, delta=0.01 * s * 5)
        self.assertAlmostEqual(noisy.mean(), 0.0, delta=0.01)

    def test_sensitivity_bound(self):
        rng = np.random.default_rng(2)
        ds = [rng.normal(size=5) * 3 for _ in range(6)]
        _, a, _ = S.dp_mean(ds, 1.0, 0.0, rng)
        _, b, _ = S.dp_mean(ds[:-1] + [rng.normal(size=5) * 50], 1.0, 0.0, rng)
        self.assertLessEqual(np.linalg.norm(a - b), 2 * 1.0 / 6 + 1e-12)

    def test_more_noise_more_error(self):
        ds = [np.array([0.5, 0.5])] * 5
        errs = []
        for z in (0.1, 1.0, 10.0):
            e = [np.linalg.norm(S.dp_mean(ds, 1.0, z, np.random.default_rng(r))[0] - 0.5) for r in range(200)]
            errs.append(np.mean(e))
        self.assertTrue(errs[0] < errs[1] < errs[2])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.dp_mean([], 1.0, 1.0, np.random.default_rng(0))
''',
"feedback": [
    ("test_sigma", "sigma = noise_multiplier × clip_norm / m (number of participating clients)."),
    ("test_noise_recipe", "Add rng.normal(0, sigma, size=dim) to the clipped mean (one draw)."),
    ("test_sensitivity_bound", "Clip each update before averaging."),
    ("test_no_noise", "With noise_multiplier = 0 return the clipped mean exactly."),
],
},
# ---------------------------------------------------------------- fedprox
{
"slug": "fedprox", "title": "FedProx Local Objective",
"difficulty": "advanced", "prereqs": ["fl-torch-local-training", "fedavg-training"], "packages": ["numpy"],
"objectives": ["Add a proximal term to the local objective", "Derive and implement its gradient",
               "Show that μ limits client drift on heterogeneous data"],
"tags": ["fedprox", "non-iid", "client-drift", "regularisation"],
"sources": ["S030", "S032"], "entry": "prox_grad(w, w_global, X, y, mu); local_prox_gd(w_global, X, y, mu, lr, steps)",
"article": r'''
# FedProx: Limiting Client Drift

## Intuition
On non-IID data, a client that trains for many local steps runs off towards *its own* optimum, and
averaging such drifted models works poorly. FedProx adds a spring that pulls each local model back
towards the global model.

## Precise explanation (Li et al., 2018)
Local objective for client k:
$$h_k(w) = L_k(w) + \frac{\mu}{2}\lVert w - w^{t}\rVert^2,$$
where $w^t$ is the current global model and $L_k$ the local loss (here MSE). Gradient:
$$\nabla h_k(w) = \nabla L_k(w) + \mu\,(w - w^t).$$
* μ = 0 recovers FedAvg's local training.
* Large μ keeps $w$ near $w^t$ (less drift, slower local progress).
For linear regression the minimiser of $h_k$ interpolates between the local least-squares solution
(μ → 0) and the global model (μ → ∞).

## Worked example
One feature, X = [[1]], y = [4], w^t = 0. Minimiser of $(w - 4)^2 + \frac{\mu}{2}w^2$ is
$w^* = 8/(2 + \mu)$: μ = 0 → 4, μ = 2 → 2, μ = 1000 → ≈ 0.008.

## Common mistakes
* Wrong sign of the proximal gradient.
* Using the *initial* local model instead of the global model as the anchor (they are equal at step 0
  but the anchor must stay fixed).
* Applying the proximal term on the server.

## Why this matters
FedProx is a standard baseline for heterogeneous federated settings.
''',
"statement": r'''
Implement full-batch local training for linear regression:
* `prox_grad(w, w_global, X, y, mu)` → `2/n · Xᵀ(Xw − y) + mu·(w − w_global)`.
* `local_prox_gd(w_global, X, y, mu, lr, steps)` → weights after `steps` gradient steps starting from
  `w_global` (copied). Raise `ValueError` if `mu < 0`, `lr <= 0` or `steps < 1`.

**Example**
```python
local_prox_gd(np.zeros(1), np.array([[1.]]), np.array([4.]), mu=2.0, lr=0.1, steps=500)   # ≈ [2.]
```
''',
"starter": r'''
import numpy as np


def prox_grad(w, w_global, X, y, mu):
    pass


def local_prox_gd(w_global, X, y, mu, lr, steps):
    pass
''',
"hints": [
    "MSE gradient from [[local-sgd]] plus `mu * (w - w_global)`.",
    "Keep `w_global` fixed as the anchor during all steps.",
    "Start from `w = np.array(w_global, dtype=float)`.",
],
"solution": r'''
import numpy as np


def prox_grad(w, w_global, X, y, mu):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    return 2.0 / len(y) * X.T @ (X @ w - y) + mu * (w - np.asarray(w_global, dtype=float))


def local_prox_gd(w_global, X, y, mu, lr, steps):
    if mu < 0 or lr <= 0 or steps < 1:
        raise ValueError("invalid mu, lr or steps")
    anchor = np.array(w_global, dtype=float)
    w = anchor.copy()
    for _ in range(steps):
        w = w - lr * prox_grad(w, anchor, X, y, mu)
    return w
''',
"explanation": r'''
The proximal gradient adds a linear pull towards the fixed global anchor. Running gradient descent on
the augmented objective yields a local model that balances fitting local data against staying close
to the global model, controlled by μ.
''',
"tests": r'''
import numpy as np

X1, Y1 = np.array([[1.]]), np.array([4.])

class TestFedProx(unittest.TestCase):
    def test_closed_form(self):
        for mu, exp in [(0.0, 4.0), (2.0, 2.0), (6.0, 1.0)]:
            np.testing.assert_allclose(S.local_prox_gd(np.zeros(1), X1, Y1, mu, 0.1, 2000), [exp], atol=1e-6)

    def test_grad_formula(self):
        g = S.prox_grad(np.array([1.0]), np.array([3.0]), X1, Y1, 0.5)
        np.testing.assert_allclose(g, [2 * (1 - 4) + 0.5 * (1 - 3)])

    def test_mu0_plain(self):
        rng = np.random.default_rng(0)
        X, y = rng.normal(size=(10, 2)), rng.normal(size=10)
        w = np.zeros(2)
        for _ in range(5):
            w = w - 0.05 * 2 / 10 * X.T @ (X @ w - y)
        np.testing.assert_allclose(S.local_prox_gd(np.zeros(2), X, y, 0.0, 0.05, 5), w)

    def test_drift_decreases_with_mu(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(30, 2)); y = X @ np.array([5., 5.])
        g = np.zeros(2)
        drifts = [np.linalg.norm(S.local_prox_gd(g, X, y, mu, 0.02, 300) - g) for mu in (0.0, 1.0, 10.0)]
        self.assertTrue(drifts[0] > drifts[1] > drifts[2])

    def test_anchor_fixed(self):
        g = np.array([1.0])
        S.local_prox_gd(g, X1, Y1, 1.0, 0.1, 10)
        np.testing.assert_array_equal(g, [1.0])

    def test_large_mu_stays(self):
        w = S.local_prox_gd(np.array([0.5]), X1, Y1, 1000.0, 0.001, 2000)
        self.assertAlmostEqual(w[0], (8 + 1000 * 0.5) / 1002, places=4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.local_prox_gd(np.zeros(1), X1, Y1, -1.0, 0.1, 5)
''',
"feedback": [
    ("test_grad_formula", "Proximal gradient adds mu·(w − w_global)."),
    ("test_closed_form", "Keep the anchor w_global fixed; minimiser is 8/(2 + mu) for the 1-D example."),
    ("test_mu0_plain", "With mu = 0, FedProx equals plain gradient descent."),
    ("test_anchor_fixed", "Copy w_global; don't modify it."),
],
},
]
