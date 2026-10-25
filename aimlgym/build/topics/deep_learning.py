"""Problem definitions for the deep learning topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- activations
{
"slug": "activations", "title": "Activation Functions",
"difficulty": "beginner", "prereqs": ["logistic-regression"], "packages": ["numpy"],
"objectives": ["Implement ReLU, leaky ReLU and tanh", "Implement their derivatives",
               "Explain why non-linear activations are necessary"],
"tags": ["activations", "relu", "tanh", "derivatives"],
"sources": ["S013", "S016"], "entry": "relu, relu_grad, leaky_relu, leaky_relu_grad, tanh, tanh_grad",
"article": r'''
# Activation Functions

## Intuition
Stacking linear layers gives… another linear layer: $W_2(W_1x) = (W_2W_1)x$. Non-linear
**activations** between layers let networks bend and fold space, so they can model curves,
XOR and images.

## Precise explanation
| name | $f(z)$ | $f'(z)$ |
|---|---|---|
| ReLU | $\max(0, z)$ | 1 if $z>0$ else 0 |
| Leaky ReLU | $z$ if $z>0$ else $\alpha z$ | 1 if $z>0$ else $\alpha$ |
| tanh | $\tanh z$ | $1-\tanh^2 z$ |
| sigmoid | $\sigma(z)$ ([[logistic-regression]]) | $\sigma(z)(1-\sigma(z))$ |

ReLU is not differentiable at 0; frameworks use the convention $f'(0) = 0$, and so do we.
Leaky ReLU keeps a small slope for negatives, avoiding "dead" units that never activate.
tanh is zero-centred with range (−1, 1); its gradient vanishes for large $|z|$.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="160" viewBox="0 0 300 160" role="img" aria-label="Plots of ReLU (a hinge at zero) and tanh (an S-curve between minus one and one)">
<title>ReLU and tanh</title>
<line x1="10" y1="80" x2="290" y2="80" stroke="#bbb"/><line x1="150" y1="10" x2="150" y2="150" stroke="#bbb"/>
<polyline points="20,80 150,80 220,10" fill="none" stroke="#1f77b4" stroke-width="2.5"/>
<path d="M 20 125 C 110 125, 120 80, 150 80 S 190 35, 280 35" fill="none" stroke="#d62728" stroke-width="2.5"/>
<text x="225" y="22" font-size="12" fill="#1f77b4">ReLU</text><text x="240" y="52" font-size="12" fill="#d62728">tanh</text>
</svg>

*Figure (original): ReLU (blue) is a hinge; tanh (red) saturates at ±1 (vertical scale differs).*

## Worked example
z = [−2, 0, 3]: ReLU [0, 0, 3]; ReLU′ [0, 0, 1]; leaky (α = 0.1) [−0.2, 0, 3]; tanh′(0) = 1.

## Common mistakes
* `np.maximum(z, 0)` is right; `max(z, 0)` (Python) fails on arrays.
* Computing tanh′ as `1 - z**2` instead of `1 - tanh(z)**2`.
* In-place modification of the input array.

## Why this matters
Activations and their derivatives are the per-layer ingredients of backpropagation ([[neuron-backprop]], [[train-xor-mlp]]).
''',
"statement": r'''
Implement element-wise functions on NumPy arrays (return new float arrays; inputs unchanged):
`relu(z)`, `relu_grad(z)` (0 at z = 0), `leaky_relu(z, alpha=0.01)`,
`leaky_relu_grad(z, alpha=0.01)` (alpha at z = 0), `tanh(z)`, `tanh_grad(z)`.

**Examples**
```python
relu(np.array([-2., 0., 3.]))              # [0., 0., 3.]
leaky_relu(np.array([-2., 3.]), alpha=0.1) # [-0.2, 3.]
tanh_grad(np.array([0.]))                  # [1.]
```
''',
"starter": r'''
import numpy as np


def relu(z):
    pass


def relu_grad(z):
    pass


def leaky_relu(z, alpha=0.01):
    pass


def leaky_relu_grad(z, alpha=0.01):
    pass


def tanh(z):
    pass


def tanh_grad(z):
    pass
''',
"hints": [
    "`np.maximum(z, 0.0)` for ReLU; `(z > 0).astype(float)` for its gradient.",
    "`np.where(z > 0, z, alpha * z)` and `np.where(z > 0, 1.0, alpha)`.",
    "`t = np.tanh(z); 1 - t ** 2`.",
],
"solution": r'''
import numpy as np


def relu(z):
    return np.maximum(np.asarray(z, dtype=float), 0.0)


def relu_grad(z):
    return (np.asarray(z) > 0).astype(float)


def leaky_relu(z, alpha=0.01):
    z = np.asarray(z, dtype=float)
    return np.where(z > 0, z, alpha * z)


def leaky_relu_grad(z, alpha=0.01):
    return np.where(np.asarray(z) > 0, 1.0, alpha)


def tanh(z):
    return np.tanh(np.asarray(z, dtype=float))


def tanh_grad(z):
    t = np.tanh(np.asarray(z, dtype=float))
    return 1.0 - t ** 2
''',
"explanation": r'''
Each function is one vectorised expression. Gradients use strict `z > 0`, giving the framework
convention at zero. All functions build new arrays, so inputs are never modified.
''',
"tests": r'''
import numpy as np

Z = np.array([-2., 0., 3.])

def num_grad(f, z, h=1e-6):
    return (f(z + h) - f(z - h)) / (2 * h)

class TestAct(unittest.TestCase):
    def test_relu(self):
        np.testing.assert_allclose(S.relu(Z), [0, 0, 3])
        np.testing.assert_allclose(S.relu_grad(Z), [0, 0, 1])

    def test_leaky(self):
        np.testing.assert_allclose(S.leaky_relu(np.array([-2., 3.]), alpha=0.1), [-0.2, 3])
        np.testing.assert_allclose(S.leaky_relu_grad(Z, alpha=0.1), [0.1, 0.1, 1])

    def test_tanh(self):
        np.testing.assert_allclose(S.tanh(Z), np.tanh(Z))
        self.assertAlmostEqual(S.tanh_grad(np.array([0.]))[0], 1.0)

    def test_numeric_grads(self):
        z = np.array([-1.3, -0.2, 0.4, 2.1])
        np.testing.assert_allclose(S.tanh_grad(z), num_grad(S.tanh, z), atol=1e-8)
        np.testing.assert_allclose(S.relu_grad(z), num_grad(S.relu, z), atol=1e-6)
        np.testing.assert_allclose(S.leaky_relu_grad(z, 0.2), num_grad(lambda v: S.leaky_relu(v, 0.2), z), atol=1e-6)

    def test_no_mutation(self):
        z = Z.copy()
        S.relu(z); S.leaky_relu(z); S.tanh_grad(z)
        np.testing.assert_array_equal(z, Z)

    def test_2d_shape(self):
        self.assertEqual(S.relu_grad(np.zeros((3, 4))).shape, (3, 4))

    def test_saturation(self):
        self.assertLess(S.tanh_grad(np.array([10.]))[0], 1e-7)
''',
"feedback": [
    ("test_relu", "relu_grad(0) must be 0 — use z > 0, not z >= 0."),
    ("test_leaky", "Leaky gradient is alpha for z <= 0."),
    ("test_numeric_grads", "tanh′(z) = 1 − tanh(z)², not 1 − z²."),
    ("test_no_mutation", "Return new arrays; don't assign into z."),
],
},
# ---------------------------------------------------------------- stable-softmax
{
"slug": "stable-softmax", "title": "Numerically Stable Softmax",
"difficulty": "beginner", "prereqs": ["activations", "exp-log"], "packages": ["numpy"],
"objectives": ["Compute softmax along an axis", "Use the max-subtraction trick to avoid overflow",
               "Compute log-softmax stably"],
"tags": ["softmax", "numerical-stability", "log-sum-exp"],
"sources": ["S013"], "entry": "softmax(z, axis=-1); log_softmax(z, axis=-1)",
"article": r'''
# Softmax

## Intuition
Softmax turns a vector of arbitrary scores (logits) into probabilities: exponentiate (all
positive), divide by the total (sum to 1). Bigger scores get exponentially more probability.

## Precise explanation
$$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}.$$
**Shift invariance:** adding a constant $c$ to every $z_i$ doesn't change the result. Choose
$c = -\max_j z_j$ so the largest exponent is $e^0 = 1$ — no overflow, and at least one term in
the denominator is 1 (no division by zero).
**Log-softmax:** $\log\text{softmax}(z)_i = z_i - \text{logsumexp}(z)$ with
$\text{logsumexp}(z) = m + \log\sum_j e^{z_j - m}$, $m = \max z$. Computing `log(softmax(z))`
directly can give `log(0) = -inf` for very negative logits.

For a batch `(n, K)`, apply along `axis=-1` (each row separately) and use `keepdims=True`.

## Worked example
z = [1, 2, 3] → shifted [−2, −1, 0] → e = [0.135, 0.368, 1] → sum 1.503 → [0.090, 0.245, 0.665].
z = [1000, 1001] gives the same as [0, 1]: [0.269, 0.731].

## Common mistakes
* `np.exp(1000)` → inf → NaN probabilities.
* Normalising over the wrong axis (columns instead of rows).
* Forgetting `keepdims`, causing a broadcasting error.

## Why this matters
Softmax is the output layer of every classifier and the attention weights of transformers
([[scaled-dot-attention]]).
''',
"statement": r'''
Implement `softmax(z, axis=-1)` and `log_softmax(z, axis=-1)` for arrays of any shape, stable
for logits as large as 1e4 in magnitude (no overflow warnings, no NaN).

**Examples**
```python
softmax(np.array([1., 2., 3.]))          # [0.09003057, 0.24472847, 0.66524096]
softmax(np.array([1000., 1001.]))        # [0.26894142, 0.73105858]
log_softmax(np.array([0., -1e4]))        # [0., -10000.]
```
''',
"starter": r'''
import numpy as np


def softmax(z, axis=-1):
    # TODO
    pass


def log_softmax(z, axis=-1):
    # TODO
    pass
''',
"hints": [
    "`m = z.max(axis=axis, keepdims=True)`; work with `z - m`.",
    "`e = np.exp(z - m); e / e.sum(axis=axis, keepdims=True)`.",
    "`(z - m) - np.log(np.exp(z - m).sum(axis=axis, keepdims=True))`.",
],
"solution": r'''
import numpy as np


def softmax(z, axis=-1):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)


def log_softmax(z, axis=-1):
    z = np.asarray(z, dtype=float)
    s = z - z.max(axis=axis, keepdims=True)
    return s - np.log(np.exp(s).sum(axis=axis, keepdims=True))
''',
"explanation": r'''
Subtracting the maximum along the chosen axis keeps every exponent ≤ 0, so `exp` cannot overflow
and the denominator is at least 1. Log-softmax uses the same shift and the log-sum-exp identity
to avoid `log(0)`.
''',
"tests": r'''
import warnings
import numpy as np

class TestSoftmax(unittest.TestCase):
    def test_basic(self):
        np.testing.assert_allclose(S.softmax(np.array([1., 2., 3.])), [0.09003057, 0.24472847, 0.66524096], rtol=1e-7)

    def test_large(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.softmax(np.array([1000., 1001.])), [0.26894142, 0.73105858], rtol=1e-7)

    def test_shift_invariance(self):
        z = np.array([0.3, -1.2, 2.5])
        np.testing.assert_allclose(S.softmax(z), S.softmax(z + 123.0), atol=1e-12)

    def test_rows(self):
        Z = np.array([[1., 2., 3.], [0., 0., 0.]])
        P = S.softmax(Z)
        np.testing.assert_allclose(P.sum(axis=1), [1, 1])
        np.testing.assert_allclose(P[1], [1 / 3] * 3)

    def test_axis0(self):
        Z = np.array([[1., 5.], [1., 5.]])
        np.testing.assert_allclose(S.softmax(Z, axis=0), [[0.5, 0.5], [0.5, 0.5]])

    def test_log_softmax(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.log_softmax(np.array([0., -1e4])), [0., -1e4], atol=1e-9)

    def test_log_consistency(self):
        z = np.array([[0.2, 1.7, -0.4], [3.0, 3.0, 1.0]])
        np.testing.assert_allclose(np.exp(S.log_softmax(z)), S.softmax(z), rtol=1e-12)
''',
"feedback": [
    ("test_large", "Subtract the max before exponentiating."),
    ("test_axis0", "Use keepdims=True with the given axis for max and sum."),
    ("test_log_softmax", "Don't compute log(softmax(z)); use shifted logits minus log-sum-exp."),
    ("test_rows", "Each row must sum to 1 when axis=-1."),
],
},
# ---------------------------------------------------------------- cross-entropy
{
"slug": "cross-entropy", "title": "Cross-Entropy Loss",
"difficulty": "beginner", "prereqs": ["stable-softmax"], "packages": ["numpy"],
"objectives": ["Compute softmax cross-entropy from logits and integer labels",
               "Derive its gradient softmax − one_hot", "Verify gradients numerically"],
"tags": ["cross-entropy", "loss-functions", "softmax", "gradients"],
"sources": ["S013", "S016"], "entry": "cross_entropy(logits, labels); cross_entropy_grad(logits, labels)",
"article": r'''
# Cross-Entropy Loss

## Intuition
If the true class is "cat", the loss should be small when the model gives "cat" high probability
and huge when it confidently says "dog". Cross-entropy is the negative log of the probability
assigned to the correct class.

## Precise explanation
For logits $z \in \mathbb{R}^{n\times K}$ and labels $y_i$:
$$L = -\frac1n\sum_i \log \text{softmax}(z_i)_{y_i}.$$
Compute it with log-softmax ([[stable-softmax]]) and pick the correct entries with fancy indexing ([[fancy-indexing]]):
`-log_softmax(z)[np.arange(n), y].mean()`.
**Gradient** (the reason softmax + cross-entropy are paired):
$$\frac{\partial L}{\partial z} = \frac{1}{n}\big(\text{softmax}(z) - \text{one\_hot}(y)\big).$$
Binary log-loss ([[logistic-regression]]) is the K = 2 special case.

## Worked example
One sample, z = [2, 0, −1], y = 0: softmax ≈ [0.844, 0.114, 0.042]; L = −log 0.844 = 0.170;
gradient = [−0.156, 0.114, 0.042].

## Common mistakes
* Taking the log of probabilities that underflowed to 0.
* Using `P[:, y]` instead of `P[np.arange(n), y]`.
* Forgetting to average over the batch (gradient off by a factor n).

## Why this matters
Cross-entropy is the training loss of classifiers and of language models ([[perplexity]] perplexity is
its exponential).
''',
"statement": r'''
Implement:
* `cross_entropy(logits, labels)` → float mean loss for `logits` `(n, K)` and integer `labels`
  `(n,)`; stable for large logits.
* `cross_entropy_grad(logits, labels)` → `(n, K)` gradient of the mean loss.

Raise `ValueError` if shapes disagree or a label is outside `0..K-1`.

**Examples**
```python
cross_entropy(np.array([[2., 0., -1.]]), np.array([0]))        # 0.16984...
cross_entropy(np.array([[0., 0.], [0., 0.]]), np.array([0, 1]))# 0.693147... (= log 2)
```
''',
"starter": r'''
import numpy as np


def cross_entropy(logits, labels):
    # TODO
    pass


def cross_entropy_grad(logits, labels):
    # TODO
    pass
''',
"hints": [
    "Write `_log_softmax` with max subtraction ([[stable-softmax]]).",
    "Loss: `-lsm[np.arange(n), labels].mean()`.",
    "Gradient: `P = np.exp(lsm); P[np.arange(n), labels] -= 1; P / n`.",
],
"solution": r'''
import numpy as np


def _check(logits, labels):
    z = np.asarray(logits, dtype=float)
    y = np.asarray(labels, dtype=int)
    if z.ndim != 2 or y.shape != (z.shape[0],):
        raise ValueError("logits must be (n, K) and labels (n,)")
    if y.size and (y.min() < 0 or y.max() >= z.shape[1]):
        raise ValueError("label out of range")
    s = z - z.max(axis=1, keepdims=True)
    lsm = s - np.log(np.exp(s).sum(axis=1, keepdims=True))
    return lsm, y


def cross_entropy(logits, labels):
    lsm, y = _check(logits, labels)
    return float(-lsm[np.arange(len(y)), y].mean())


def cross_entropy_grad(logits, labels):
    lsm, y = _check(logits, labels)
    n = len(y)
    g = np.exp(lsm)
    g[np.arange(n), y] -= 1.0
    return g / n
''',
"explanation": r'''
A stable log-softmax gives log-probabilities directly, and paired indexing selects each row's
correct-class entry. The gradient is softmax minus one-hot, divided by the batch size because the
loss is a mean.
''',
"tests": r'''
import numpy as np

class TestCE(unittest.TestCase):
    def test_single(self):
        z = np.array([[2., 0., -1.]])
        p = np.exp(z) / np.exp(z).sum()
        self.assertAlmostEqual(S.cross_entropy(z, np.array([0])), -np.log(p[0, 0]))

    def test_uniform(self):
        self.assertAlmostEqual(S.cross_entropy(np.zeros((2, 2)), np.array([0, 1])), np.log(2))

    def test_large_logits(self):
        self.assertAlmostEqual(S.cross_entropy(np.array([[1000., 0.]]), np.array([1])), 1000.0)

    def test_grad_formula(self):
        z = np.array([[2., 0., -1.]])
        p = np.exp(z) / np.exp(z).sum()
        np.testing.assert_allclose(S.cross_entropy_grad(z, np.array([0])), p - [[1, 0, 0]])

    def test_grad_numeric(self):
        rng = np.random.default_rng(0)
        z, y = rng.normal(size=(4, 3)), np.array([0, 2, 1, 2])
        g = S.cross_entropy_grad(z, y)
        h = 1e-6
        for i in range(4):
            for j in range(3):
                e = np.zeros_like(z); e[i, j] = h
                num = (S.cross_entropy(z + e, y) - S.cross_entropy(z - e, y)) / (2 * h)
                self.assertAlmostEqual(g[i, j], num, places=6)

    def test_grad_rows_sum_zero(self):
        g = S.cross_entropy_grad(np.random.default_rng(1).normal(size=(5, 4)), np.array([0, 1, 2, 3, 0]))
        np.testing.assert_allclose(g.sum(axis=1), 0, atol=1e-12)

    def test_bad_label(self):
        with self.assertRaises(ValueError):
            S.cross_entropy(np.zeros((1, 3)), np.array([3]))
''',
"feedback": [
    ("test_large_logits", "Use a stable log-softmax; log(softmax) underflows."),
    ("test_grad_numeric", "Gradient of the *mean* loss: divide (softmax − one_hot) by n."),
    ("test_single", "Pick log-probabilities with [np.arange(n), labels]."),
    ("test_bad_label", "Validate labels are in 0..K−1."),
],
},
# ---------------------------------------------------------------- dense-forward
{
"slug": "dense-forward", "title": "Dense Layer Forward Pass",
"difficulty": "beginner", "prereqs": ["activations", "matmul-dot"], "packages": ["numpy"],
"objectives": ["Compute XW + b for a batch", "Check layer shapes", "Count parameters and initialise weights"],
"tags": ["dense-layer", "fully-connected", "initialisation", "shapes"],
"sources": ["S013", "S014"], "entry": "dense(X, W, b); n_params(layer_sizes); he_init(fan_in, fan_out, rng)",
"article": r'''
# The Dense (Fully Connected) Layer

## Intuition
A dense layer is many linear models side by side: each output unit is a weighted sum of all
inputs plus a bias. For a batch of inputs this is one matrix product.

## Precise explanation
Input $X$ `(n, d_in)`, weights $W$ `(d_in, d_out)`, bias $b$ `(d_out,)`:
$$Y = XW + b \quad\text{shape } (n, d_\text{out}),$$
with $b$ broadcast over rows ([[broadcast-center]]). Parameters: $d_\text{in} d_\text{out} + d_\text{out}$.
For layer sizes $[d_0, d_1, \dots, d_L]$ the total is $\sum_l (d_{l-1}+1)d_l$.

**Initialisation:** all-zero weights make every unit identical forever (symmetry). **He
initialisation** for ReLU networks draws $W \sim \mathcal N(0, 2/d_\text{in})$ so activations keep
roughly constant variance across layers; biases start at 0.

## Worked example
X = [[1, 2]], W = [[1, 0, −1], [2, 1, 0]], b = [0.5, 0, 0] → Y = [[5.5, 2, −1]].
Layers [784, 128, 10]: (784+1)·128 + (128+1)·10 = 100 480 + 1 290 = 101 770 parameters.

## Common mistakes
* `W @ X` instead of `X @ W` (row-vector convention used here).
* Bias with shape `(n,)` instead of `(d_out,)`.
* Initialising all weights to the same constant.

## Why this matters
Dense layers make up MLPs ([[mlp-forward]]), transformer feed-forward blocks and classifier heads.
''',
"statement": r'''
Implement:
* `dense(X, W, b)` → `X @ W + b`; raise `ValueError` on any shape mismatch
  (`X` must be 2-D, `W.shape[0] == X.shape[1]`, `b.shape == (W.shape[1],)`).
* `n_params(layer_sizes)` → total weights + biases for consecutive dense layers (int); raise
  `ValueError` for fewer than 2 sizes or non-positive sizes.
* `he_init(fan_in, fan_out, rng)` → `(W, b)` with `W = rng.normal(0, sqrt(2/fan_in), (fan_in, fan_out))`
  and `b = zeros(fan_out)`.

**Examples**
```python
dense(np.array([[1., 2.]]), np.array([[1., 0., -1.], [2., 1., 0.]]), np.array([0.5, 0., 0.]))
# [[5.5, 2., -1.]]
n_params([784, 128, 10])   # 101770
```
''',
"starter": r'''
import numpy as np


def dense(X, W, b):
    pass


def n_params(layer_sizes):
    pass


def he_init(fan_in, fan_out, rng):
    pass
''',
"hints": [
    "Validate all three shapes, then `X @ W + b`.",
    "`sum((a + 1) * c for a, c in zip(sizes[:-1], sizes[1:]))`.",
    "`rng.normal(0.0, np.sqrt(2.0 / fan_in), size=(fan_in, fan_out))`.",
],
"solution": r'''
import numpy as np


def dense(X, W, b):
    X, W, b = (np.asarray(a, dtype=float) for a in (X, W, b))
    if X.ndim != 2 or W.ndim != 2 or X.shape[1] != W.shape[0] or b.shape != (W.shape[1],):
        raise ValueError("shape mismatch")
    return X @ W + b


def n_params(layer_sizes):
    if len(layer_sizes) < 2 or any(s < 1 for s in layer_sizes):
        raise ValueError("need at least two positive layer sizes")
    return int(sum((a + 1) * c for a, c in zip(layer_sizes[:-1], layer_sizes[1:])))


def he_init(fan_in, fan_out, rng):
    W = rng.normal(0.0, np.sqrt(2.0 / fan_in), size=(fan_in, fan_out))
    return W, np.zeros(fan_out)
''',
"explanation": r'''
The forward pass is one matrix product plus a broadcast bias, guarded by shape checks. Each
layer has (inputs + 1) × outputs parameters. He initialisation scales the weight spread by the
fan-in to keep signal variance stable through ReLU layers.
''',
"tests": r'''
import numpy as np

class TestDense(unittest.TestCase):
    def test_forward(self):
        Y = S.dense(np.array([[1., 2.]]), np.array([[1., 0., -1.], [2., 1., 0.]]), np.array([0.5, 0., 0.]))
        np.testing.assert_allclose(Y, [[5.5, 2., -1.]])

    def test_batch_shape(self):
        self.assertEqual(S.dense(np.ones((7, 4)), np.ones((4, 3)), np.zeros(3)).shape, (7, 3))

    def test_shape_errors(self):
        with self.assertRaises(ValueError):
            S.dense(np.ones((2, 3)), np.ones((4, 2)), np.zeros(2))
        with self.assertRaises(ValueError):
            S.dense(np.ones((2, 3)), np.ones((3, 2)), np.zeros(3))

    def test_n_params(self):
        self.assertEqual(S.n_params([784, 128, 10]), 101770)
        self.assertEqual(S.n_params([2, 1]), 3)

    def test_n_params_bad(self):
        with self.assertRaises(ValueError):
            S.n_params([5])

    def test_he_stats(self):
        W, b = S.he_init(500, 400, np.random.default_rng(0))
        self.assertEqual(W.shape, (500, 400))
        np.testing.assert_array_equal(b, np.zeros(400))
        self.assertAlmostEqual(W.std(), np.sqrt(2 / 500), delta=0.002)
        self.assertAlmostEqual(W.mean(), 0.0, delta=0.002)

    def test_he_reproducible(self):
        a, _ = S.he_init(3, 2, np.random.default_rng(5))
        b, _ = S.he_init(3, 2, np.random.default_rng(5))
        np.testing.assert_array_equal(a, b)
''',
"feedback": [
    ("test_forward", "Compute X @ W + b (row-vector convention)."),
    ("test_shape_errors", "Check W rows == X columns and b length == W columns."),
    ("test_n_params", "Each layer has (fan_in + 1) * fan_out parameters."),
    ("test_he_stats", "Standard deviation is sqrt(2 / fan_in)."),
],
},
# ---------------------------------------------------------------- mlp-forward
{
"slug": "mlp-forward", "title": "MLP Forward Pass", "optional": True,
"difficulty": "beginner", "prereqs": ["dense-forward"], "packages": ["numpy"],
"objectives": ["Chain dense layers and activations", "Cache intermediate values for backprop",
               "Produce class predictions with softmax"],
"tags": ["mlp", "forward-pass", "cache", "neural-networks"],
"sources": ["S013", "S014"], "entry": "mlp_forward(X, params); predict_classes(X, params)",
"article": r'''
# Multilayer Perceptron: Forward Pass

## Intuition
An MLP passes data through layers like an assembly line: each station applies a dense layer and
then an activation, handing the result to the next station. The last station outputs raw scores
(logits).

## Precise explanation
With parameters `[(W1, b1), …, (WL, bL)]`:
$$a_0 = X,\quad z_l = a_{l-1}W_l + b_l,\quad a_l = \text{ReLU}(z_l)\ (l < L),\quad \text{logits} = z_L.$$
No activation on the output layer — softmax/cross-entropy ([[stable-softmax]]/03) handle it.
**Cache:** backpropagation needs every $a_{l-1}$ and $z_l$, so store them during the forward pass.
Predicted class = `argmax(logits, axis=1)` (softmax is monotone, so it isn't needed for argmax).

```mermaid
flowchart LR
  X[a0 = X] --> D1["z1 = a0 W1 + b1"] --> R1["a1 = ReLU(z1)"] --> D2["z2 = a1 W2 + b2"] --> O[logits]
```

## Worked example
X = [[1, −1]], W1 = I, b1 = 0 → z1 = [1, −1] → a1 = [1, 0]; W2 = [[2], [3]], b2 = [0.5] →
logits = [[2.5]].

## Common mistakes
* Applying ReLU to the output logits.
* Losing the cache (overwriting variables) and being unable to backprop.
* Shape drift — check `(n, d_l)` after each layer.

## Why this matters
This is the inference path of every feed-forward network; [[train-xor-mlp]] adds the backward pass.
''',
"statement": r'''
Implement:
* `mlp_forward(X, params)` → `(logits, cache)` where `params` is a non-empty list of `(W, b)`;
  ReLU after every layer except the last; `cache` is a list with one dict per layer
  `{"a_prev": ..., "z": ...}`.
* `predict_classes(X, params)` → integer array of argmax over logits.

**Example**
```python
params = [(np.eye(2), np.zeros(2)), (np.array([[2.], [3.]]), np.array([0.5]))]
logits, cache = mlp_forward(np.array([[1., -1.]]), params)
logits        # [[2.5]]
cache[1]["a_prev"]   # [[1., 0.]]
```
''',
"starter": r'''
import numpy as np


def mlp_forward(X, params):
    # TODO
    pass


def predict_classes(X, params):
    # TODO
    pass
''',
"hints": [
    "Loop `for l, (W, b) in enumerate(params)` with `a = X` initially.",
    "`z = a @ W + b`; store `{'a_prev': a, 'z': z}`; apply ReLU unless it's the last layer.",
    "`mlp_forward(X, params)[0].argmax(axis=1)`.",
],
"solution": r'''
import numpy as np


def mlp_forward(X, params):
    if not params:
        raise ValueError("params must contain at least one layer")
    a = np.asarray(X, dtype=float)
    cache = []
    last = len(params) - 1
    for l, (W, b) in enumerate(params):
        z = a @ W + b
        cache.append({"a_prev": a, "z": z})
        a = z if l == last else np.maximum(z, 0.0)
    return a, cache


def predict_classes(X, params):
    return mlp_forward(X, params)[0].argmax(axis=1)
''',
"explanation": r'''
Each iteration applies one dense layer, records its input and pre-activation for later
backpropagation, and applies ReLU except at the output. Class predictions use argmax on the
logits.
''',
"tests": r'''
import numpy as np

P = [(np.eye(2), np.zeros(2)), (np.array([[2.], [3.]]), np.array([0.5]))]

class TestMLP(unittest.TestCase):
    def test_example(self):
        logits, cache = S.mlp_forward(np.array([[1., -1.]]), P)
        np.testing.assert_allclose(logits, [[2.5]])
        np.testing.assert_allclose(cache[1]["a_prev"], [[1., 0.]])
        np.testing.assert_allclose(cache[0]["z"], [[1., -1.]])

    def test_no_relu_on_output(self):
        logits, _ = S.mlp_forward(np.array([[1., 1.]]), [(np.array([[-1.], [-1.]]), np.array([0.]))])
        np.testing.assert_allclose(logits, [[-2.]])

    def test_cache_length(self):
        rng = np.random.default_rng(0)
        params = [(rng.normal(size=(3, 5)), np.zeros(5)), (rng.normal(size=(5, 4)), np.zeros(4)),
                  (rng.normal(size=(4, 2)), np.zeros(2))]
        logits, cache = S.mlp_forward(rng.normal(size=(6, 3)), params)
        self.assertEqual(len(cache), 3)
        self.assertEqual(logits.shape, (6, 2))
        self.assertTrue((cache[2]["a_prev"] >= 0).all())

    def test_matches_manual(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(4, 3)); W1, b1 = rng.normal(size=(3, 2)), rng.normal(size=2)
        W2, b2 = rng.normal(size=(2, 3)), rng.normal(size=3)
        exp = np.maximum(X @ W1 + b1, 0) @ W2 + b2
        np.testing.assert_allclose(S.mlp_forward(X, [(W1, b1), (W2, b2)])[0], exp)

    def test_predict(self):
        params = [(np.array([[1., -1.]]), np.array([0., 0.]))]
        np.testing.assert_array_equal(S.predict_classes(np.array([[2.], [-3.]]), params), [0, 1])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.mlp_forward(np.ones((1, 2)), [])
''',
"feedback": [
    ("test_no_relu_on_output", "Don't apply ReLU to the last layer."),
    ("test_example", "Cache the layer input a_prev and pre-activation z for every layer."),
    ("test_matches_manual", "Apply ReLU between layers: a = max(z, 0)."),
    ("test_predict", "Predictions are argmax over axis 1 of the logits."),
],
},
# ---------------------------------------------------------------- neuron-backprop
{
"slug": "neuron-backprop", "title": "Backprop Through One Neuron",
"difficulty": "intermediate", "prereqs": ["scalar-autograd"], "packages": ["numpy"],
"objectives": ["Apply the chain rule through a computational graph", "Compute gradients of a sigmoid neuron with BCE",
               "Confirm the simplification dL/dz = p − y"],
"tags": ["backpropagation", "chain-rule", "computational-graph"],
"sources": ["S016", "S014"], "entry": "neuron_forward_backward(x, y, w, b)",
"article": r'''
# Backpropagation in One Neuron

## Intuition
Backpropagation is the chain rule applied systematically: to know how the loss changes with a
weight, multiply how the loss changes with the output, how the output changes with the
pre-activation, and how the pre-activation changes with the weight.

## Precise explanation
Graph for one example: $z = w\cdot x + b$ → $p = \sigma(z)$ → $L = -[y\log p + (1-y)\log(1-p)]$.
Local derivatives:
* $\partial L/\partial p = -\frac{y}{p} + \frac{1-y}{1-p}$
* $\partial p/\partial z = p(1-p)$
* $\partial z/\partial w = x$, $\partial z/\partial b = 1$
Chain: $\frac{\partial L}{\partial z} = \frac{\partial L}{\partial p}\frac{\partial p}{\partial z} = p - y$,
so $\nabla_w L = (p-y)x$ and $\partial L/\partial b = p-y$.

```mermaid
flowchart LR
  x & w --> z["z = w·x + b"] --> p["p = σ(z)"] --> L["L = BCE(p, y)"]
  L -. "∂L/∂p" .-> p -. "·p(1−p)" .-> z -. "·x" .-> w
```

## Worked example
x = [1, 2], w = [0.5, −0.25], b = 0, y = 1: z = 0, p = 0.5, L = log 2 = 0.693;
∂L/∂p = −2, ∂p/∂z = 0.25, ∂L/∂z = −0.5; ∇w = [−0.5, −1], ∂b = −0.5.

## Common mistakes
* Multiplying by $\sigma'(x)$ instead of $\sigma'(z)$.
* Sign errors (gradient points uphill).
* Not reusing forward values (p) in the backward pass.

## Why this matters
Every deep-learning framework does exactly this, layer by layer ([[train-xor-mlp]]).
''',
"statement": r'''
Write `neuron_forward_backward(x, y, w, b)` for one example (`x`, `w` 1-D arrays, `y` in {0, 1})
returning a dict with keys `z, p, loss, dL_dp, dp_dz, dL_dz, grad_w, grad_b` (floats, `grad_w`
an array). Clip `p` to `[1e-12, 1 - 1e-12]` only when computing `loss` and `dL_dp`.

**Example**
```python
r = neuron_forward_backward(np.array([1., 2.]), 1, np.array([0.5, -0.25]), 0.0)
r["loss"], r["dL_dz"], r["grad_w"]    # (0.6931..., -0.5, array([-0.5, -1. ]))
```
''',
"starter": r'''
import numpy as np


def neuron_forward_backward(x, y, w, b):
    # TODO: forward z, p, loss; backward dL_dp, dp_dz, dL_dz, grad_w, grad_b
    pass
''',
"hints": [
    "`z = float(w @ x + b)`; `p = 1 / (1 + np.exp(-z))`.",
    "`dL_dp = -y / pc + (1 - y) / (1 - pc)` with clipped `pc`; `dp_dz = p * (1 - p)`.",
    "`dL_dz = dL_dp * dp_dz`; `grad_w = dL_dz * x`; `grad_b = dL_dz`.",
],
"solution": r'''
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
''',
"explanation": r'''
The forward pass computes and stores z and p. The backward pass multiplies local derivatives
from the loss back to the parameters, exactly following the graph. The product dL/dp · dp/dz
simplifies to p − y, which the tests check.
''',
"tests": r'''
import numpy as np

X, W = np.array([1., 2.]), np.array([0.5, -0.25])

def loss_at(w, b, x, y):
    p = 1 / (1 + np.exp(-(w @ x + b)))
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))

class TestNeuron(unittest.TestCase):
    def test_example(self):
        r = S.neuron_forward_backward(X, 1, W, 0.0)
        self.assertAlmostEqual(r["z"], 0.0)
        self.assertAlmostEqual(r["loss"], np.log(2))
        self.assertAlmostEqual(r["dL_dp"], -2.0)
        self.assertAlmostEqual(r["dp_dz"], 0.25)
        np.testing.assert_allclose(r["grad_w"], [-0.5, -1.0])

    def test_p_minus_y(self):
        for y in (0, 1):
            r = S.neuron_forward_backward(np.array([0.3, -1.1]), y, np.array([1.2, 0.4]), -0.2)
            self.assertAlmostEqual(r["dL_dz"], r["p"] - y, places=10)

    def test_numeric_w(self):
        x, w, b, y = np.array([0.7, -0.3, 1.5]), np.array([0.2, 0.9, -0.4]), 0.1, 0
        r = S.neuron_forward_backward(x, y, w, b)
        h = 1e-6
        for j in range(3):
            e = np.zeros(3); e[j] = h
            num = (loss_at(w + e, b, x, y) - loss_at(w - e, b, x, y)) / (2 * h)
            self.assertAlmostEqual(r["grad_w"][j], num, places=6)

    def test_numeric_b(self):
        x, w, b, y = np.array([0.7, -0.3]), np.array([0.2, 0.9]), 0.1, 1
        r = S.neuron_forward_backward(x, y, w, b)
        num = (loss_at(w, b + 1e-6, x, y) - loss_at(w, b - 1e-6, x, y)) / 2e-6
        self.assertAlmostEqual(r["grad_b"], num, places=6)

    def test_large_z_stable(self):
        r = S.neuron_forward_backward(np.array([100.]), 1, np.array([10.]), 0.0)
        self.assertTrue(np.isfinite(r["loss"]))
        self.assertAlmostEqual(r["dL_dz"], 0.0, places=6)

    def test_keys(self):
        r = S.neuron_forward_backward(X, 0, W, 0.0)
        self.assertEqual(set(r), {"z", "p", "loss", "dL_dp", "dp_dz", "dL_dz", "grad_w", "grad_b"})
''',
"feedback": [
    ("test_example", "dL/dp = −y/p + (1−y)/(1−p); dp/dz = p(1−p)."),
    ("test_p_minus_y", "Multiply the two local derivatives; the product should equal p − y."),
    ("test_numeric_w", "grad_w = dL/dz · x."),
    ("test_large_z_stable", "Use a stable sigmoid and clip p for the log."),
],
},
# ---------------------------------------------------------------- sgd-momentum
{
"slug": "sgd-momentum", "title": "SGD with Momentum",
"difficulty": "intermediate", "prereqs": ["dense-backward", "gradient-descent-1d"], "packages": ["numpy"],
"objectives": ["Implement the momentum update", "Keep optimiser state per parameter",
               "Compare convergence on an ill-conditioned quadratic"],
"tags": ["optimisers", "momentum", "sgd"],
"sources": ["S013"], "entry": "class Momentum(lr, beta): step(params, grads)",
"article": r'''
# Momentum

## Intuition
Plain gradient descent zig-zags across narrow valleys. Momentum treats the parameters like a
heavy ball: it accumulates velocity in consistent directions and damps oscillations.

## Precise explanation
For each parameter $\theta$ with gradient $g$:
$$v \leftarrow \beta v + g,\qquad \theta \leftarrow \theta - \eta v,$$
with $v$ initialised to zeros of the same shape and $\beta \in [0, 1)$ (typically 0.9).
$\beta = 0$ is plain SGD. Velocity is optimiser **state**, kept per parameter between steps.
(Some libraries write $v \leftarrow \beta v + (1-\beta) g$; that only rescales the learning rate.)

## Worked example
$\eta = 0.1$, $\beta = 0.9$, constant gradient 1: v = 1, 1.9, 2.71 … so the steps grow
0.1, 0.19, 0.271 — acceleration along a consistent slope.

## Common mistakes
* Re-initialising velocity every step (then it is plain SGD).
* Sharing one velocity array between parameters.
* Mutating the caller's gradient arrays.

## Why this matters
Momentum (and its descendants such as Adam) is how practically every network is trained; FedAvg
servers can also apply momentum to aggregated updates.
''',
"statement": r'''
Implement `class Momentum(lr=0.01, beta=0.9)`:
* `step(params, grads)` — `params` and `grads` are dicts name → NumPy array (same keys/shapes).
  Update velocities (created lazily as zeros on first use) and return a **new** dict of updated
  params; inputs must not be modified.
* Raise `ValueError` if keys differ, shapes differ, `lr <= 0`, or `beta` not in `[0, 1)`.

**Example**
```python
opt = Momentum(lr=0.1, beta=0.9)
p = {"w": np.array([0.0])}
for _ in range(3):
    p = opt.step(p, {"w": np.array([1.0])})
p["w"]    # [-0.561]  (= -(0.1 + 0.19 + 0.271))
```
''',
"starter": r'''
import numpy as np


class Momentum:
    def __init__(self, lr=0.01, beta=0.9):
        # TODO validate and store state
        pass

    def step(self, params, grads):
        # TODO
        return params
''',
"hints": [
    "Store `self.v = {}` and create `np.zeros_like(param)` the first time a key appears.",
    "`self.v[k] = self.beta * self.v[k] + grads[k]`.",
    "Build `new[k] = params[k] - self.lr * self.v[k]` (a new array).",
],
"solution": r'''
import numpy as np


class Momentum:
    def __init__(self, lr=0.01, beta=0.9):
        if lr <= 0 or not 0 <= beta < 1:
            raise ValueError("lr must be > 0 and 0 <= beta < 1")
        self.lr = lr
        self.beta = beta
        self.v = {}

    def step(self, params, grads):
        if set(params) != set(grads):
            raise ValueError("params and grads must have the same keys")
        new = {}
        for k, p in params.items():
            g = np.asarray(grads[k], dtype=float)
            p = np.asarray(p, dtype=float)
            if g.shape != p.shape:
                raise ValueError(f"shape mismatch for {k}")
            if k not in self.v:
                self.v[k] = np.zeros_like(p)
            self.v[k] = self.beta * self.v[k] + g
            new[k] = p - self.lr * self.v[k]
        return new
''',
"explanation": r'''
Velocity arrays persist inside the optimiser, one per parameter name. Each step blends the old
velocity with the new gradient and moves the parameter against the velocity, returning fresh
arrays so caller data is never mutated.
''',
"tests": r'''
import numpy as np

class TestMomentum(unittest.TestCase):
    def test_example(self):
        opt = S.Momentum(lr=0.1, beta=0.9)
        p = {"w": np.array([0.0])}
        for _ in range(3):
            p = opt.step(p, {"w": np.array([1.0])})
        np.testing.assert_allclose(p["w"], [-0.561])

    def test_beta0_is_sgd(self):
        opt = S.Momentum(lr=0.5, beta=0.0)
        p = opt.step({"a": np.array([1.0, 2.0])}, {"a": np.array([2.0, -2.0])})
        np.testing.assert_allclose(p["a"], [0.0, 3.0])

    def test_no_mutation(self):
        p0, g0 = {"w": np.array([1.0])}, {"w": np.array([0.5])}
        S.Momentum(lr=0.1).step(p0, g0)
        np.testing.assert_array_equal(p0["w"], [1.0])
        np.testing.assert_array_equal(g0["w"], [0.5])

    def test_separate_state(self):
        opt = S.Momentum(lr=1.0, beta=0.5)
        p = {"a": np.zeros(1), "b": np.zeros(1)}
        p = opt.step(p, {"a": np.ones(1), "b": np.zeros(1)})
        p = opt.step(p, {"a": np.zeros(1), "b": np.zeros(1)})
        np.testing.assert_allclose(p["a"], [-1.5])
        np.testing.assert_allclose(p["b"], [0.0])

    def test_faster_on_ravine(self):
        H = np.array([1.0, 50.0])
        def run(beta, lr, steps=60):
            opt = S.Momentum(lr=lr, beta=beta); p = {"x": np.array([1.0, 1.0])}
            for _ in range(steps):
                p = opt.step(p, {"x": H * p["x"]})
            return float(0.5 * (H * p["x"] ** 2).sum())
        self.assertLess(run(0.9, 0.01), run(0.0, 0.01))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.Momentum(beta=1.0)
        with self.assertRaises(ValueError):
            S.Momentum().step({"a": np.zeros(2)}, {"a": np.zeros(3)})
''',
"feedback": [
    ("test_example", "v ← βv + g; θ ← θ − lr·v, with v persisting between calls."),
    ("test_separate_state", "Keep one velocity array per parameter name."),
    ("test_no_mutation", "Return new arrays; don't use -= on the inputs."),
    ("test_errors", "Validate beta in [0, 1) and matching shapes."),
],
},
# ---------------------------------------------------------------- conv1d
{
"slug": "conv1d", "title": "1D Convolution by Hand (valid, stride)", "optional": True,
"difficulty": "advanced", "prereqs": ["dense-forward", "moving-average"], "packages": ["numpy"],
"objectives": ["Implement deep-learning style convolution (cross-correlation)",
               "Apply padding and stride", "Compute the output length formula"],
"tags": ["convolution", "cnn", "stride", "padding"],
"sources": ["S015", "S013"], "entry": "conv1d(x, kernel, stride=1, padding=0, bias=0.0); conv_output_length(n, k, stride, padding)",
"article": r'''
# 1-D Convolution

## Intuition
Slide a small window (the **kernel**) along a signal; at each position, take the dot product of
the kernel with the part of the signal under it. A kernel [−1, 1] detects increases; [1/3]×3
smooths.

## Precise explanation
Deep-learning libraries implement **cross-correlation** (no kernel flip) and still call it
convolution:
$$y_i = b + \sum_{j=0}^{k-1} x_{is + j}\, w_j,$$
after zero-padding $p$ values on both ends. Output length (CS231n formula):
$$n_\text{out} = \left\lfloor \frac{n + 2p - k}{s} \right\rfloor + 1.$$
NumPy's `np.convolve` flips the kernel (mathematical convolution); `np.correlate(x, w, "valid")`
matches the DL definition for stride 1, no padding.

## Worked example
x = [1, 2, 3, 4, 5], w = [1, 0, −1], stride 1: [1−3, 2−4, 3−5] = [−2, −2, −2]; length
(5 − 3)/1 + 1 = 3. With stride 2: positions 0 and 2 → [−2, −2]. With padding 1: x becomes
[0,1,2,3,4,5,0] → length 5: [−2, −2, −2, −2, 4].

## Common mistakes
* Flipping the kernel (using `np.convolve`).
* Off-by-one in the number of windows.
* Padding only one side.

## Why this matters
Convolutions power audio models and text CNNs, and their 2-D version is the core of computer
vision ([[conv2d-filter]]).
''',
"statement": r'''
Implement:
* `conv_output_length(n, k, stride, padding)` → int using the formula; raise `ValueError` if the
  result would be < 1, `k < 1` or `stride < 1` or `padding < 0`.
* `conv1d(x, kernel, stride=1, padding=0, bias=0.0)` → float array (cross-correlation with zero
  padding).

**Examples**
```python
conv1d([1, 2, 3, 4, 5], [1, 0, -1])              # [-2., -2., -2.]
conv1d([1, 2, 3, 4, 5], [1, 0, -1], stride=2)    # [-2., -2.]
conv1d([1, 2, 3, 4, 5], [1, 0, -1], padding=1)   # [-2., -2., -2., -2., 4.]
```
''',
"starter": r'''
import numpy as np


def conv_output_length(n, k, stride, padding):
    pass


def conv1d(x, kernel, stride=1, padding=0, bias=0.0):
    pass
''',
"hints": [
    "`(n + 2 * padding - k) // stride + 1`.",
    "Pad with `np.pad(x, padding)`.",
    "Window i starts at `i * stride`: `xp[i*stride : i*stride + k] @ kernel + bias`.",
],
"solution": r'''
import numpy as np


def conv_output_length(n, k, stride, padding):
    if k < 1 or stride < 1 or padding < 0:
        raise ValueError("invalid k, stride or padding")
    out = (n + 2 * padding - k) // stride + 1
    if out < 1:
        raise ValueError("kernel larger than padded input")
    return int(out)


def conv1d(x, kernel, stride=1, padding=0, bias=0.0):
    x = np.asarray(x, dtype=float)
    w = np.asarray(kernel, dtype=float)
    k = len(w)
    m = conv_output_length(len(x), k, stride, padding)
    xp = np.pad(x, padding)
    return np.array([xp[i * stride:i * stride + k] @ w for i in range(m)]) + bias
''',
"explanation": r'''
The output length comes from the formula, which also validates the configuration. After zero
padding, each output is the dot product of the kernel with the window starting at i·stride — the
cross-correlation used by deep-learning libraries.
''',
"tests": r'''
import numpy as np

X = [1, 2, 3, 4, 5]

class TestConv1d(unittest.TestCase):
    def test_valid(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1]), [-2, -2, -2])

    def test_stride(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1], stride=2), [-2, -2])

    def test_padding(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1], padding=1), [-2, -2, -2, -2, 4])

    def test_no_flip(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 2]), np.correlate(X, [1, 2], mode="valid"))

    def test_bias(self):
        np.testing.assert_allclose(S.conv1d([1, 1, 1], [1, 1], bias=0.5), [2.5, 2.5])

    def test_output_length(self):
        self.assertEqual(S.conv_output_length(32, 5, 1, 2), 32)
        self.assertEqual(S.conv_output_length(7, 3, 2, 0), 3)
        for n, k, s, p in [(10, 3, 1, 0), (10, 4, 3, 1), (9, 2, 2, 2)]:
            self.assertEqual(len(S.conv1d(np.ones(n), np.ones(k), s, p)), S.conv_output_length(n, k, s, p))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.conv1d([1, 2], [1, 2, 3])
        with self.assertRaises(ValueError):
            S.conv_output_length(5, 2, 0, 0)
''',
"feedback": [
    ("test_no_flip", "Don't flip the kernel; DL 'convolution' is cross-correlation."),
    ("test_padding", "Pad both ends with zeros using np.pad(x, padding)."),
    ("test_stride", "Window i starts at i * stride."),
    ("test_output_length", "n_out = floor((n + 2p − k)/s) + 1."),
],
},
# ---------------------------------------------------------------- train-xor-mlp
{
"slug": "train-xor-mlp", "title": "Train an MLP on XOR", "optional": True,
"difficulty": "advanced", "prereqs": ["dense-backward", "sgd-momentum"], "packages": ["numpy"],
"objectives": ["Implement full backpropagation for a 2-layer network", "Train with gradient descent until XOR is solved",
               "Explain why a linear model cannot solve XOR"],
"tags": ["backpropagation", "training-loop", "xor", "mlp"],
"sources": ["S014", "S016", "S013"], "entry": "init_params(n_hidden, seed); forward_backward(X, y, params); train_xor(n_hidden=8, lr=1.0, epochs=3000, seed=0)",
"article": r'''
# Learning XOR with Backpropagation

## Intuition
XOR outputs 1 when exactly one input is 1. No straight line separates {(0,1), (1,0)} from
{(0,0), (1,1)}, so logistic regression fails. A hidden layer can bend the space so a line
works — and backpropagation finds the weights automatically.

## Precise explanation
Network 2 → H → 1: $h = \tanh(XW_1 + b_1)$, $p = \sigma(hW_2 + b_2)$, loss = mean BCE.
Backward pass (n examples, from [[cross-entropy]]/06):
* $\delta_2 = (p - y)/n$  (shape `(n, 1)`)
* $\nabla W_2 = h^\top \delta_2$, $\nabla b_2 = \sum \delta_2$
* $\delta_1 = (\delta_2 W_2^\top) \odot (1 - h^2)$
* $\nabla W_1 = X^\top \delta_1$, $\nabla b_1 = \sum \delta_1$
Then $\theta \leftarrow \theta - \eta\nabla\theta$. Random (not zero) initial weights break
symmetry between hidden units.

```mermaid
flowchart LR
  X --> H["h = tanh(XW1+b1)"] --> P["p = σ(hW2+b2)"] --> L[BCE]
  L -. "δ2 = (p−y)/n" .-> P
  P -. "δ1 = δ2 W2ᵀ ⊙ (1−h²)" .-> H
```

## Worked example
After training (seed 0, H = 8, lr = 1, 3000 epochs) the reference network reaches a loss below
0.001 and outputs probabilities close to [0, 1, 1, 0] for inputs (0,0), (0,1), (1,0), (1,1).

**Local minima are real.** In this build, H = 4 with seed 0 gets stuck at a loss of about 0.35
(seeds 1–7 succeed); with H = 8 all of seeds 0–7 succeed. Wider layers and different seeds are the
usual remedies.

## Common mistakes
* Forgetting the $(1-h^2)$ factor.
* Using $W_2$ after updating it to compute $\delta_1$ (compute all gradients first).
* Zero initialisation (hidden units stay identical).

## Why this matters
This is a complete deep-learning training loop; frameworks automate the backward pass, but the
structure — forward, loss, backward, update — is identical.
''',
"statement": r'''
Implement:
* `init_params(n_hidden, seed)` → dict with `W1 (2, H)`, `b1 (H,)`, `W2 (H, 1)`, `b2 (1,)`,
  using `rng = np.random.default_rng(seed)`; `W1 = rng.normal(0, 1, (2, H))` then
  `W2 = rng.normal(0, 1, (H, 1))`; biases zero.
* `forward_backward(X, y, params)` → `(loss, grads)` where `y` has shape `(n,)` and grads has the
  same keys/shapes as params, following the formulas above (BCE with p clipped to [1e-12, 1−1e-12]
  for the loss value).
* `train_xor(n_hidden=8, lr=1.0, epochs=3000, seed=0)` → `(params, history)` trained by full-batch
  gradient descent on the 4 XOR points (`X = [[0,0],[0,1],[1,0],[1,1]]`, `y = [0,1,1,0]`), history =
  loss before each update.

**Example**
```python
params, hist = train_xor()
hist[-1] < 0.05        # True
```
''',
"starter": r'''
import numpy as np

X_XOR = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
Y_XOR = np.array([0., 1., 1., 0.])


def init_params(n_hidden, seed):
    pass


def forward_backward(X, y, params):
    pass


def train_xor(n_hidden=8, lr=1.0, epochs=3000, seed=0):
    pass
''',
"hints": [
    "Forward: `h = np.tanh(X @ W1 + b1)`, `p = sigmoid(h @ W2 + b2)[:, 0]`.",
    "`d2 = ((p - y) / n)[:, None]`; `d1 = (d2 @ W2.T) * (1 - h ** 2)`.",
    "Grads: `W2: h.T @ d2`, `b2: d2.sum(0)`, `W1: X.T @ d1`, `b1: d1.sum(0)`.",
],
"solution": r'''
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
''',
"explanation": r'''
The forward pass stores h and p, the backward pass propagates δ from the output to the hidden
layer using the tanh derivative, and all gradients are computed before any update. Full-batch
gradient descent then drives the loss toward zero; the hidden layer makes XOR linearly separable.
''',
"tests": r'''
import numpy as np

class TestXOR(unittest.TestCase):
    def test_init_shapes(self):
        p = S.init_params(5, 0)
        self.assertEqual({k: v.shape for k, v in p.items()}, {"W1": (2, 5), "b1": (5,), "W2": (5, 1), "b2": (1,)})

    def test_init_recipe(self):
        rng = np.random.default_rng(3)
        W1 = rng.normal(0, 1, (2, 4)); W2 = rng.normal(0, 1, (4, 1))
        p = S.init_params(4, 3)
        np.testing.assert_allclose(p["W1"], W1); np.testing.assert_allclose(p["W2"], W2)

    def test_gradients_numeric(self):
        params = S.init_params(3, 1)
        X, y = S.X_XOR, S.Y_XOR
        _, g = S.forward_backward(X, y, params)
        h = 1e-6
        for k in params:
            it = np.nditer(params[k], flags=["multi_index"])
            for _ in it:
                idx = it.multi_index
                pp = {kk: vv.copy() for kk, vv in params.items()}; pm = {kk: vv.copy() for kk, vv in params.items()}
                pp[k][idx] += h; pm[k][idx] -= h
                num = (S.forward_backward(X, y, pp)[0] - S.forward_backward(X, y, pm)[0]) / (2 * h)
                self.assertAlmostEqual(g[k][idx], num, places=6, msg=f"{k}{idx}")

    def test_trains(self):
        params, hist = S.train_xor()
        self.assertEqual(len(hist), 3000)
        self.assertLess(hist[-1], 0.05)

    def test_predictions(self):
        params, _ = S.train_xor()
        h = np.tanh(S.X_XOR @ params["W1"] + params["b1"])
        p = 1 / (1 + np.exp(-(h @ params["W2"] + params["b2"])))[:, 0]
        np.testing.assert_array_equal((p > 0.5).astype(int), [0, 1, 1, 0])

    def test_loss_decreases_overall(self):
        _, hist = S.train_xor(epochs=500)
        self.assertLess(hist[-1], hist[0])

    def test_initial_loss_value(self):
        loss, _ = S.forward_backward(S.X_XOR, S.Y_XOR,
                                     {"W1": np.zeros((2, 2)), "b1": np.zeros(2), "W2": np.zeros((2, 1)), "b2": np.zeros(1)})
        self.assertAlmostEqual(loss, np.log(2))
''',
"feedback": [
    ("test_gradients_numeric", "Check δ1 = (δ2 W2ᵀ) ⊙ (1 − h²) and that δ2 is divided by n."),
    ("test_init_recipe", "Draw W1 then W2 from one default_rng(seed); biases are zeros."),
    ("test_trains", "Compute all gradients first, then update every parameter with lr."),
    ("test_initial_loss_value", "With zero weights p = 0.5 everywhere, so the loss is log 2."),
],
},
# ---------------------------------------------------------------- inverted-dropout
{
"slug": "inverted-dropout", "title": "Inverted Dropout", "optional": True,
"difficulty": "advanced", "prereqs": ["train-xor-mlp", "seeded-generator"], "packages": ["numpy"],
"objectives": ["Implement inverted dropout for training and evaluation modes",
               "Keep expected activations unchanged by rescaling", "Backpropagate through the dropout mask"],
"tags": ["dropout", "regularisation", "train-eval-mode"],
"sources": ["S013"], "entry": "dropout_forward(x, p, rng, training=True); dropout_backward(grad_out, mask, p)",
"article": r'''
# Inverted Dropout

## Intuition
During training, randomly switch off a fraction of units so the network cannot rely on any single
one — like a team practising with random members absent. At test time everyone plays.

## Precise explanation
With drop probability $p$:
* **Training:** mask $m_i \sim \text{Bernoulli}(1-p)$ (1 = keep); output $y = x \odot m / (1-p)$.
  Dividing by $1-p$ ("inverted" dropout) keeps $\mathbb E[y] = x$, so nothing needs rescaling at
  test time.
* **Evaluation:** $y = x$ (no randomness).
* **Backward:** $\partial L/\partial x = \partial L/\partial y \odot m / (1-p)$.
* $p = 0$ → identity; $p = 1$ is invalid (division by zero).
Mask recipe used here: `keep = rng.random(x.shape) >= p`.

## Worked example
x = [2, 2, 2, 2], p = 0.5, mask [1, 0, 1, 1] → y = [4, 0, 4, 4]; mean of y ≈ 2 on average.

## Common mistakes
* Applying dropout at evaluation time.
* Scaling at test time *and* using inverted dropout (double scaling).
* Generating a new mask in the backward pass.

## Why this matters
Dropout is a standard regulariser in MLPs and transformers; train/eval mode switches are a
classic source of bugs.
''',
"statement": r'''
Implement:
* `dropout_forward(x, p, rng, training=True)` → `(y, mask)`. In training, `mask = rng.random(x.shape) >= p`
  (boolean) and `y = x * mask / (1 - p)`; in evaluation return `(x.copy(), None)`.
  Raise `ValueError` unless `0 <= p < 1`.
* `dropout_backward(grad_out, mask, p)` → gradient w.r.t. `x`.

**Example**
```python
y, m = dropout_forward(np.ones(8), 0.5, np.random.default_rng(0))
set(np.unique(y)) <= {0.0, 2.0}    # True
dropout_forward(np.ones(3), 0.5, None, training=False)[0]   # [1., 1., 1.]
```
''',
"starter": r'''
import numpy as np


def dropout_forward(x, p, rng, training=True):
    pass


def dropout_backward(grad_out, mask, p):
    pass
''',
"hints": [
    "Validate `0 <= p < 1` first.",
    "`mask = rng.random(x.shape) >= p`; `y = x * mask / (1 - p)`.",
    "Backward uses the same mask: `grad_out * mask / (1 - p)`.",
],
"solution": r'''
import numpy as np


def dropout_forward(x, p, rng, training=True):
    if not 0 <= p < 1:
        raise ValueError("p must be in [0, 1)")
    x = np.asarray(x, dtype=float)
    if not training:
        return x.copy(), None
    mask = rng.random(x.shape) >= p
    return x * mask / (1.0 - p), mask


def dropout_backward(grad_out, mask, p):
    return np.asarray(grad_out, dtype=float) * mask / (1.0 - p)
''',
"explanation": r'''
Training mode samples a keep-mask with probability 1 − p and rescales the survivors, so the
expected output equals the input. Evaluation mode is the identity. The backward pass reuses the
forward mask because the operation is element-wise multiplication by a constant.
''',
"tests": r'''
import numpy as np

class TestDropout(unittest.TestCase):
    def test_values(self):
        y, m = S.dropout_forward(np.ones(8), 0.5, np.random.default_rng(0))
        self.assertTrue(set(np.unique(y)).issubset({0.0, 2.0}))
        np.testing.assert_allclose(y, m * 2.0)

    def test_recipe(self):
        rng_a, rng_b = np.random.default_rng(7), np.random.default_rng(7)
        x = np.arange(10.0)
        y, m = S.dropout_forward(x, 0.3, rng_a)
        exp_mask = rng_b.random(x.shape) >= 0.3
        np.testing.assert_array_equal(m, exp_mask)
        np.testing.assert_allclose(y, x * exp_mask / 0.7)

    def test_eval_identity(self):
        y, m = S.dropout_forward(np.array([1., 2., 3.]), 0.5, None, training=False)
        np.testing.assert_array_equal(y, [1, 2, 3])
        self.assertIsNone(m)

    def test_expectation(self):
        y, _ = S.dropout_forward(np.full(200000, 3.0), 0.4, np.random.default_rng(1))
        self.assertAlmostEqual(y.mean(), 3.0, delta=0.02)

    def test_p0_identity(self):
        y, _ = S.dropout_forward(np.array([5., -1.]), 0.0, np.random.default_rng(2))
        np.testing.assert_array_equal(y, [5., -1.])

    def test_backward(self):
        x = np.array([1., 2., 3., 4.])
        y, m = S.dropout_forward(x, 0.5, np.random.default_rng(3))
        g = S.dropout_backward(np.ones(4), m, 0.5)
        np.testing.assert_allclose(g, m * 2.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.dropout_forward(np.ones(2), 1.0, np.random.default_rng(0))
''',
"feedback": [
    ("test_recipe", "Mask = rng.random(x.shape) >= p; scale kept values by 1/(1 − p)."),
    ("test_eval_identity", "In evaluation mode return x unchanged and mask None."),
    ("test_backward", "Reuse the forward mask and the same 1/(1 − p) scale."),
    ("test_bad_p", "p must satisfy 0 <= p < 1."),
],
},
# ---------------------------------------------------------------- batchnorm-forward
{
"slug": "batchnorm-forward", "title": "Batch Normalization by Hand (train/eval)", "optional": True,
"difficulty": "advanced", "prereqs": ["inverted-dropout"], "packages": ["numpy"],
"objectives": ["Normalise activations with batch statistics", "Maintain running averages for evaluation",
               "Apply learnable scale and shift"],
"tags": ["batch-normalization", "normalisation", "running-statistics"],
"sources": ["S013"], "entry": "class BatchNorm1d(n_features, momentum=0.1, eps=1e-5): forward(x, training=True)",
"article": r'''
# Batch Normalization

## Intuition
Layer inputs drift as earlier layers learn. Batch normalisation standardises each feature using
the current mini-batch's mean and variance, then lets the network re-scale and re-shift with
learned parameters — making training faster and less sensitive to initialisation.

## Precise explanation
For a batch $x$ `(n, d)`, per feature:
$$\mu_B = \text{mean}(x),\ \sigma_B^2 = \text{var}(x)\ (\text{population}),\quad
\hat x = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}},\quad y = \gamma \hat x + \beta.$$
Running statistics for evaluation (PyTorch-style momentum, D2L describes the same idea):
$$\mu_\text{run} \leftarrow (1-m)\mu_\text{run} + m\,\mu_B,\qquad
\sigma^2_\text{run} \leftarrow (1-m)\sigma^2_\text{run} + m\,\sigma^2_{B,\text{unbiased}},$$
where the running variance uses the unbiased $n/(n-1)$ batch variance (as PyTorch does).
Evaluation uses the running statistics, so a single example gives a deterministic output.
Initial values: $\gamma = 1$, $\beta = 0$, $\mu_\text{run} = 0$, $\sigma^2_\text{run} = 1$.

## Worked example
x = [[1], [3]]: μ = 2, σ² = 1 → x̂ ≈ [−1, 1] (ε small). Running mean after one step with
m = 0.1: 0.2; running var: 0.9·1 + 0.1·2 = 1.1 (unbiased var = 2).

## Common mistakes
* Using batch statistics at evaluation time.
* Normalising across features instead of across the batch (that is layer norm).
* Updating running statistics during evaluation.

## Why this matters
Batch norm is common in CNNs; its train/eval distinction appears again in dropout and in
federated settings where client batch statistics differ.
''',
"statement": r'''
Implement `class BatchNorm1d(n_features, momentum=0.1, eps=1e-5)` with attributes `gamma`,
`beta` (ones/zeros), `running_mean` (zeros), `running_var` (ones) and
`forward(x, training=True)`:
* training: normalise with batch mean / population variance, update running stats as above
  (unbiased variance; requires batch size ≥ 2, else `ValueError`), return `gamma * x_hat + beta`;
* evaluation: use running stats, no updates.
Raise `ValueError` if `x.shape[1] != n_features`.

**Example**
```python
bn = BatchNorm1d(1)
bn.forward(np.array([[1.], [3.]]))   # ≈ [[-1.], [1.]]
bn.running_mean, bn.running_var      # (array([0.2]), array([1.1]))
```
''',
"starter": r'''
import numpy as np


class BatchNorm1d:
    def __init__(self, n_features, momentum=0.1, eps=1e-5):
        # TODO
        pass

    def forward(self, x, training=True):
        # TODO
        pass
''',
"hints": [
    "`mu = x.mean(0)`, `var = x.var(0)` (population) for normalisation.",
    "Unbiased: `var * n / (n - 1)` for the running variance update.",
    "Eval: `(x - running_mean) / sqrt(running_var + eps)` then scale/shift.",
],
"solution": r'''
import numpy as np


class BatchNorm1d:
    def __init__(self, n_features, momentum=0.1, eps=1e-5):
        self.n_features = n_features
        self.momentum = momentum
        self.eps = eps
        self.gamma = np.ones(n_features)
        self.beta = np.zeros(n_features)
        self.running_mean = np.zeros(n_features)
        self.running_var = np.ones(n_features)

    def forward(self, x, training=True):
        x = np.asarray(x, dtype=float)
        if x.ndim != 2 or x.shape[1] != self.n_features:
            raise ValueError("x must have shape (n, n_features)")
        if training:
            n = x.shape[0]
            if n < 2:
                raise ValueError("batch size must be >= 2 in training mode")
            mu = x.mean(axis=0)
            var = x.var(axis=0)
            m = self.momentum
            self.running_mean = (1 - m) * self.running_mean + m * mu
            self.running_var = (1 - m) * self.running_var + m * var * n / (n - 1)
        else:
            mu, var = self.running_mean, self.running_var
        x_hat = (x - mu) / np.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta
''',
"explanation": r'''
Training mode normalises with the batch's own statistics and updates exponential running
averages (unbiased variance). Evaluation mode normalises with the stored averages and leaves
state untouched, so outputs no longer depend on the other examples in the batch.
''',
"tests": r'''
import numpy as np

class TestBN(unittest.TestCase):
    def test_train_output(self):
        bn = S.BatchNorm1d(1)
        np.testing.assert_allclose(bn.forward(np.array([[1.], [3.]])), [[-1.], [1.]], atol=1e-5)

    def test_running_stats(self):
        bn = S.BatchNorm1d(1)
        bn.forward(np.array([[1.], [3.]]))
        np.testing.assert_allclose(bn.running_mean, [0.2])
        np.testing.assert_allclose(bn.running_var, [1.1])

    def test_normalised_stats(self):
        x = np.random.default_rng(0).normal(5, 3, size=(64, 4))
        y = S.BatchNorm1d(4).forward(x)
        np.testing.assert_allclose(y.mean(0), 0, atol=1e-10)
        np.testing.assert_allclose(y.std(0), 1, atol=1e-3)

    def test_gamma_beta(self):
        bn = S.BatchNorm1d(2); bn.gamma = np.array([2., 3.]); bn.beta = np.array([1., -1.])
        y = bn.forward(np.array([[0., 0.], [2., 4.]]))
        np.testing.assert_allclose(y, [[-1., -4.], [3., 2.]], atol=1e-4)

    def test_eval_uses_running(self):
        bn = S.BatchNorm1d(1)
        bn.running_mean = np.array([10.]); bn.running_var = np.array([4.])
        y = bn.forward(np.array([[12.]]), training=False)
        np.testing.assert_allclose(y, [[1.0]], atol=1e-5)
        np.testing.assert_allclose(bn.running_mean, [10.])

    def test_converges_to_population(self):
        bn = S.BatchNorm1d(1, momentum=0.1)
        rng = np.random.default_rng(1)
        for _ in range(300):
            bn.forward(rng.normal(2.0, 0.5, size=(32, 1)))
        self.assertAlmostEqual(bn.running_mean[0], 2.0, delta=0.05)
        self.assertAlmostEqual(bn.running_var[0], 0.25, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.BatchNorm1d(2).forward(np.ones((3, 3)))
        with self.assertRaises(ValueError):
            S.BatchNorm1d(1).forward(np.ones((1, 1)))
''',
"feedback": [
    ("test_running_stats", "Running var uses the unbiased batch variance (× n/(n−1)) with momentum 0.1."),
    ("test_eval_uses_running", "In eval mode use running statistics and do not update them."),
    ("test_normalised_stats", "Normalise per feature over axis 0 (the batch)."),
    ("test_gamma_beta", "Output is gamma * x_hat + beta."),
],
},
# ---------------------------------------------------------------- gradient-check
{
"slug": "gradient-check", "title": "Gradient Checking by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["dense-backward", "numerical-gradient"], "packages": ["numpy"],
"objectives": ["Compare analytic and numerical gradients", "Use relative error with a safe denominator",
               "Locate the parameter with the worst mismatch"],
"tags": ["gradient-checking", "debugging", "finite-differences"],
"sources": ["S016", "S013"], "entry": "relative_error(a, b); grad_check(f, grad, x, h=1e-5)",
"article": r'''
# Gradient Checking

## Intuition
Backpropagation code can be subtly wrong and still "train" a bit. A gradient check compares your
analytic gradient with a slow but reliable numerical estimate ([[numerical-gradient]]). If they disagree, there is
a bug.

## Precise explanation
For each coordinate $i$: $g^\text{num}_i = \frac{f(x + h e_i) - f(x - h e_i)}{2h}$.
Compare with the **relative error**
$$\text{rel}(a, b) = \frac{|a - b|}{\max(|a| + |b|,\ \text{tiny})},$$
which is scale-free; the `tiny` floor (1e−12 here) avoids 0/0 when both are zero. Rough guide for
float64 and smooth functions: < 1e−7 excellent, 1e−7…1e−4 suspicious, > 1e−4 almost certainly a
bug. Kinks (ReLU at 0) can cause false alarms.

## Worked example
f(x) = Σ x², grad 2x. At x = [1, −2], numerical [2, −4] → relative errors ~1e−11. A buggy grad
returning x gives rel = |2 − 1|/3 = 0.33.

## Common mistakes
* Using absolute error only (meaningless for very large or small gradients).
* h too small (round-off) or too large (truncation).
* Forgetting to restore x after perturbing.

## Why this matters
Every from-scratch implementation in this course was tested this way; it is the standard sanity
check before training any custom layer.
''',
"statement": r'''
Implement:
* `relative_error(a, b)` → element-wise array (or float for scalars) using the formula with
  floor `1e-12`.
* `grad_check(f, grad, x, h=1e-5)` → dict `{"max_rel_error": float, "worst_index": tuple,
  "numerical": array}` where `f(x)` returns a float, `grad(x)` an array shaped like `x`, and `x` is a
  float array of any shape (must not be modified).

**Example**
```python
r = grad_check(lambda v: float((v**2).sum()), lambda v: 2*v, np.array([1., -2.]))
r["max_rel_error"] < 1e-8      # True
r = grad_check(lambda v: float((v**2).sum()), lambda v: v, np.array([1., -2.]))
round(r["max_rel_error"], 3)   # 0.333
```
''',
"starter": r'''
import numpy as np


def relative_error(a, b):
    pass


def grad_check(f, grad, x, h=1e-5):
    pass
''',
"hints": [
    "`np.abs(a - b) / np.maximum(np.abs(a) + np.abs(b), 1e-12)`.",
    "Iterate with `np.ndindex(x.shape)`; perturb a copy of x at that index.",
    "`worst = np.unravel_index(np.argmax(rel), x.shape)`.",
],
"solution": r'''
import numpy as np


def relative_error(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    r = np.abs(a - b) / np.maximum(np.abs(a) + np.abs(b), 1e-12)
    return r if r.ndim else float(r)


def grad_check(f, grad, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    analytic = np.asarray(grad(x.copy()), dtype=float)
    num = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        xp = x.copy(); xm = x.copy()
        xp[idx] += h
        xm[idx] -= h
        num[idx] = (f(xp) - f(xm)) / (2 * h)
    rel = np.asarray(relative_error(analytic, num))
    worst = tuple(int(i) for i in np.unravel_index(int(np.argmax(rel)), x.shape))
    return {"max_rel_error": float(rel.max()), "worst_index": worst, "numerical": num}
''',
"explanation": r'''
Every coordinate is perturbed on fresh copies, giving a central-difference gradient of any shape.
The relative error compares it with the analytic gradient in a scale-free way, and the worst
coordinate is reported to help locate bugs.
''',
"tests": r'''
import numpy as np

sq = lambda v: float((v ** 2).sum())

class TestGradCheck(unittest.TestCase):
    def test_rel_error(self):
        self.assertAlmostEqual(S.relative_error(2.0, 1.0), 1 / 3)
        self.assertEqual(S.relative_error(0.0, 0.0), 0.0)

    def test_correct(self):
        self.assertLess(S.grad_check(sq, lambda v: 2 * v, np.array([1., -2.]))["max_rel_error"], 1e-8)

    def test_buggy(self):
        r = S.grad_check(sq, lambda v: v, np.array([1., -2.]))
        self.assertAlmostEqual(r["max_rel_error"], 1 / 3, places=6)

    def test_worst_index_2d(self):
        def bad(v):
            g = 2 * v; g[1, 0] += 5; return g
        r = S.grad_check(sq, bad, np.ones((2, 3)))
        self.assertEqual(r["worst_index"], (1, 0))

    def test_no_mutation(self):
        x = np.array([0.5, 1.5])
        S.grad_check(sq, lambda v: 2 * v, x)
        np.testing.assert_array_equal(x, [0.5, 1.5])

    def test_numerical_returned(self):
        r = S.grad_check(lambda v: float(np.sin(v).sum()), np.cos, np.array([0.3, 1.2]))
        np.testing.assert_allclose(r["numerical"], np.cos([0.3, 1.2]), atol=1e-9)

    def test_softmax_ce(self):
        y = 2
        def f(z):
            s = z - z.max(); return float(-(s[y] - np.log(np.exp(s).sum())))
        def g(z):
            p = np.exp(z - z.max()); p /= p.sum(); p[y] -= 1; return p
        self.assertLess(S.grad_check(f, g, np.array([0.1, -0.4, 0.9, 2.0]))["max_rel_error"], 1e-7)
''',
"feedback": [
    ("test_rel_error", "Floor the denominator at 1e-12 so 0 vs 0 gives 0."),
    ("test_worst_index_2d", "Support any shape with np.ndindex and report a tuple index."),
    ("test_no_mutation", "Perturb copies of x, never x itself."),
    ("test_buggy", "Relative error = |a − b| / (|a| + |b|)."),
],
},
]
