"""NumPy steps added in the 2026-10 revision: vectorised arithmetic and matrix products, each
compared with the plain-Python loops from the Mathematics topic."""

PROBLEMS = [
# ---------------------------------------------------------------- vectorized-math
{
"slug": "vectorized-math", "title": "Vectorised Arithmetic and ufuncs",
"difficulty": "beginner", "prereqs": ["array-info", "sigmoid-function"], "packages": ["numpy"],
"objectives": ["Replace element-by-element loops with array expressions",
               "Use universal functions (np.exp, np.sqrt, np.abs, np.where)",
               "Check a vectorised result against a loop with np.allclose",
               "Write a sigmoid that never overflows on arrays"],
"tags": ["vectorisation", "ufuncs", "elementwise", "allclose"],
"sources": ["S007", "S081"], "entry": "dot_loop(a, b); dot_vectorized(a, b); fahrenheit(celsius); rms(x); sigmoid(x)",
"article": r'''
# Vectorised Arithmetic and ufuncs

## Intuition
In [[dot-product]] you wrote a loop that multiplies matching elements and adds them up. NumPy
lets you write the *whole* operation at once: `a * b` multiplies every pair of elements, and
`.sum()` adds them. The loop still happens, but inside fast compiled code, typically tens to
hundreds of times faster than a Python loop on large arrays.

## Precise explanation
* Arithmetic operators on arrays of the same shape work **element-wise**:
  `a + b`, `a * b`, `a ** 2`, `a / 2`, `-a`. Mixing an array and a number applies the number to
  every element: `c * 9 / 5 + 32`.
* **Universal functions (ufuncs)** are element-wise functions: `np.exp`, `np.log`, `np.sqrt`,
  `np.abs`, `np.maximum(a, b)`. `math.exp` only accepts single numbers; `np.exp` accepts arrays.
* Reductions collapse an array: `a.sum()`, `a.mean()`, `a.max()`.
* `np.where(cond, x, y)` picks from `x` where `cond` is true and from `y` elsewhere. Both `x` and
  `y` are computed for every element, so they must not overflow.
* Comparing floats: use `np.allclose(a, b)` (tolerance) instead of `==`.

**Stable vectorised sigmoid.** [[sigmoid-function]] branched on the sign of one number. For
arrays, compute `e = np.exp(-np.abs(x))` (never larger than 1), then
`np.where(x >= 0, 1 / (1 + e), e / (1 + e))`.

## Worked example
```python
import numpy as np
a = np.array([1.0, 2.0, 3.0]); b = np.array([4.0, 5.0, 6.0])
a * b            # array([ 4., 10., 18.])
(a * b).sum()    # 32.0 — the dot product
np.sqrt(np.mean(a ** 2))   # root-mean-square ≈ 2.160
```

## Common mistakes
* Using `math.exp(array)` → `TypeError`; use `np.exp`.
* Python lists do not vectorise: `[1, 2] * 2` is `[1, 2, 1, 2]`. Convert with `np.asarray`.
* Integer arrays: `np.array([1, 2]) / 2` is float, but in-place `a /= 2` on an int array fails;
  create float arrays with `dtype=float`.
* Shape mismatches such as `(3,) * (4,)` raise `ValueError` — check shapes first.

## Why this matters
Every later topic expresses its maths as array expressions; checking them against a slow,
obviously-correct loop is the standard way to test numerical code.
''',
"statement": r'''
Implement (inputs may be lists or arrays; convert with `np.asarray(x, dtype=float)`):

1. `dot_loop(a, b)` — the dot product with a Python loop (raise `ValueError` if lengths differ).
2. `dot_vectorized(a, b)` — the same with `*` and `.sum()` (same `ValueError`); return a `float`.
3. `fahrenheit(celsius)` — `celsius * 9 / 5 + 32` as an array.
4. `rms(x)` — root-mean-square $\sqrt{\frac1n\sum x_i^2}$ as a `float`.
5. `sigmoid(x)` — stable element-wise sigmoid returning an array of the same shape; must not
   produce warnings or `nan` for inputs like `[-1000, 0, 1000]`.

**Examples**
```python
dot_vectorized([1, 2, 3], [4, 5, 6])   # 32.0
fahrenheit([0, 100])                    # array([ 32., 212.])
sigmoid([-1000, 0, 1000])               # array([0. , 0.5, 1. ])
```
''',
"starter": r'''
import numpy as np


def dot_loop(a, b):
    if len(a) != len(b):
        raise ValueError("length mismatch")
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def dot_vectorized(a, b):
    # TODO: element-wise multiply, then sum
    return 0.0


def fahrenheit(celsius):
    # TODO
    return np.asarray(celsius, dtype=float)


def rms(x):
    # TODO
    return 0.0


def sigmoid(x):
    x = np.asarray(x, dtype=float)
    # TODO: stable version with np.exp(-np.abs(x)) and np.where
    return 1 / (1 + np.exp(-x))
''',
"hints": [
    "`a = np.asarray(a, dtype=float)`; compare `a.shape != b.shape` before multiplying; `float((a * b).sum())`.",
    "`float(np.sqrt(np.mean(x ** 2)))` for RMS.",
    "`e = np.exp(-np.abs(x)); return np.where(x >= 0, 1 / (1 + e), e / (1 + e))`.",
],
"solution": r'''
import numpy as np


def dot_loop(a, b):
    if len(a) != len(b):
        raise ValueError("length mismatch")
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def dot_vectorized(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("shape mismatch")
    return float((a * b).sum())


def fahrenheit(celsius):
    return np.asarray(celsius, dtype=float) * 9 / 5 + 32


def rms(x):
    x = np.asarray(x, dtype=float)
    return float(np.sqrt(np.mean(x ** 2)))


def sigmoid(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(-np.abs(x))
    return np.where(x >= 0, 1 / (1 + e), e / (1 + e))
''',
"explanation": r'''
Converting inputs to float arrays makes every operator element-wise. The dot product becomes one
multiplication and one reduction; RMS chains a power, a mean and a square root. The sigmoid only
exponentiates non-positive numbers, so both branches given to `np.where` are finite everywhere.
''',
"tests": r'''
import random
import warnings

import numpy as np


class TestVectorized(unittest.TestCase):
    def test_dot_matches_loop(self):
        rng = random.Random(0)
        a = [rng.random() - 0.5 for _ in range(200)]
        b = [rng.random() - 0.5 for _ in range(200)]
        self.assertAlmostEqual(S.dot_vectorized(a, b), S.dot_loop(a, b), places=10)
        self.assertEqual(S.dot_vectorized([1, 2, 3], [4, 5, 6]), 32.0)
        self.assertIsInstance(S.dot_vectorized([1], [2]), float)

    def test_dot_mismatch(self):
        with self.assertRaises(ValueError):
            S.dot_vectorized([1, 2], [1, 2, 3])

    def test_fahrenheit(self):
        out = S.fahrenheit([0, 100, -40])
        self.assertIsInstance(out, np.ndarray)
        np.testing.assert_allclose(out, [32, 212, -40])

    def test_rms(self):
        self.assertAlmostEqual(S.rms([3, 4]), math.sqrt(12.5))
        self.assertAlmostEqual(S.rms(np.full(10, -2.0)), 2.0)

    def test_sigmoid_values(self):
        x = np.linspace(-6, 6, 13)
        expected = [1 / (1 + math.exp(-v)) for v in x]
        np.testing.assert_allclose(S.sigmoid(x), expected, rtol=1e-12)

    def test_sigmoid_stable(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            out = S.sigmoid([-1000.0, 0.0, 1000.0])
        np.testing.assert_allclose(out, [0.0, 0.5, 1.0])

    def test_sigmoid_shape(self):
        self.assertEqual(S.sigmoid(np.zeros((2, 3))).shape, (2, 3))
''',
"feedback": [
    ("test_dot_matches_loop", "Multiply the arrays element-wise and call `.sum()`; return a Python float."),
    ("test_dot_mismatch", "Compare the shapes and raise ValueError before multiplying."),
    ("test_rms", "Square, average, then take the square root."),
    ("test_sigmoid_stable", "Avoid `np.exp(-x)` for very negative x; use `np.exp(-np.abs(x))` with `np.where`."),
    ("test_sigmoid_shape", "Keep the input shape: operate on the whole array without flattening."),
],
"library": {
"text": r'''
NumPy also has a dedicated function for this step: `np.dot(a, b)` (or `a @ b`, introduced in
[[matmul-dot]]) computes the dot product directly, and is what you would normally write.
The element-wise form `(a * b).sum()` shows what `np.dot` does. `scipy.special.expit` is a
library sigmoid for arrays. The tests compare your functions with these.
''',
"optional": ["scipy"],
"tests": r'''
try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    def test_dot_matches_np_dot(self):
        a, b = np.arange(5.0), np.linspace(-1, 1, 5)
        self.assertAlmostEqual(S.dot_vectorized(a, b), float(np.dot(a, b)), places=12)

    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_sigmoid_matches_expit(self):
        x = np.linspace(-40, 40, 81)
        np.testing.assert_allclose(S.sigmoid(x), _special.expit(x), rtol=1e-12)
''',
},
},
# ---------------------------------------------------------------- matmul-dot
{
"slug": "matmul-dot", "title": "Matrix Products with @",
"difficulty": "intermediate", "prereqs": ["axis-aggregations", "matrix-multiply"], "packages": ["numpy"],
"objectives": ["Multiply matrices and matrix–vector pairs with the @ operator",
               "Predict result shapes and catch mismatches before multiplying",
               "Score a whole batch of examples with one product",
               "Verify @ against the triple loop from Mathematics"],
"tags": ["matmul", "matrix-multiplication", "shapes", "linear-algebra"],
"sources": ["S082", "S007", "S009"], "entry": "matmul_loops(A, B); matmul(A, B); batch_scores(X, w, b); gram(X)",
"article": r'''
# Matrix Products with @

## Intuition
[[matrix-multiply]] computed each entry of $AB$ as a dot product of a row of $A$ with a column of
$B$ using three nested loops. NumPy's `@` operator does the same in one expression and is the
most important operation in machine learning: a linear model scores a whole batch of examples
with a single `X @ w`.

## Precise explanation
For $A$ of shape $(m, n)$ and $B$ of shape $(n, p)$, $C = AB$ has shape $(m, p)$ and
$C_{ij} = \sum_{k} A_{ik} B_{kj}$. The inner dimensions must match.

| Expression | Shapes | Result |
|---|---|---|
| `A @ B` | (m, n) @ (n, p) | (m, p) |
| `A @ v` | (m, n) @ (n,) | (m,) — each row dotted with v |
| `v @ w` | (n,) @ (n,) | scalar — the dot product |
| `X @ X.T` | (m, n) @ (n, m) | (m, m) — all pairwise dot products (the Gram matrix) |

* `A * B` is **element-wise**, not matrix multiplication.
* `np.dot` gives the same results for 1-D and 2-D arrays; `@` is the modern, clearer spelling.
* `.T` transposes a 2-D array.
* **Linear model on a batch**: rows of `X` are examples, `w` holds one weight per feature, and
  `X @ w + b` gives one score per example.

## Worked example
```python
A = np.array([[1, 2], [3, 4]]); B = np.array([[5, 6], [7, 8]])
A @ B        # [[19, 22], [43, 50]]
A * B        # [[ 5, 12], [21, 32]]  — different!
X = np.array([[1., 2.], [3., 4.], [5., 6.]]); w = np.array([0.5, -1.0])
X @ w + 0.1  # [-1.4, -2.4, -3.4]
```

## Common mistakes
* Using `*` when you meant `@`.
* Multiplying `(3, 2) @ (3, 2)`; you probably needed a transpose.
* Confusing a 1-D vector `(n,)` with a column `(n, 1)`; `X @ w` with `w` of shape `(n, 1)` returns
  shape `(m, 1)`, not `(m,)`.

## Why this matters
Dense layers ([[dense-forward]]), attention ([[scaled-dot-attention]]) and least squares are all
matrix products.
''',
"statement": r'''
Implement:

1. `matmul_loops(A, B)` — nested-list product with three loops (as in [[matrix-multiply]]);
   raise `ValueError` if inner dimensions differ. Return a list of lists.
2. `matmul(A, B)` — `np.asarray` both and return `A @ B`; raise `ValueError` with a message
   containing both shapes if the inner dimensions differ (check before multiplying; both
   inputs are 2-D).
3. `batch_scores(X, w, b)` — scores `X @ w + b` for a 2-D `X`, 1-D `w` and a number `b`.
4. `gram(X)` — `X @ X.T`.

**Examples**
```python
matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])   # array([[19, 22], [43, 50]])
batch_scores([[1, 2], [3, 4], [5, 6]], [0.5, -1.0], 0.1)   # array([-1.4, -2.4, -3.4])
```
''',
"starter": r'''
import numpy as np


def matmul_loops(A, B):
    # TODO: three nested loops
    return []


def matmul(A, B):
    A = np.asarray(A)
    B = np.asarray(B)
    # TODO: check shapes, then use @
    return A * B


def batch_scores(X, w, b):
    # TODO
    return np.zeros(len(X))


def gram(X):
    # TODO
    return np.asarray(X)
''',
"hints": [
    "Loops: for each i (rows of A) and j (columns of B), sum `A[i][k] * B[k][j]` over k.",
    "`if A.shape[1] != B.shape[0]: raise ValueError(f\"cannot multiply {A.shape} by {B.shape}\")`.",
    "`np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b`; `X @ X.T` for the Gram matrix.",
],
"solution": r'''
import numpy as np


def matmul_loops(A, B):
    n = len(B)
    if any(len(row) != n for row in A):
        raise ValueError("inner dimensions differ")
    p = len(B[0]) if B else 0
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(len(A))]


def matmul(A, B):
    A = np.asarray(A)
    B = np.asarray(B)
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"cannot multiply {A.shape} by {B.shape}")
    return A @ B


def batch_scores(X, w, b):
    return np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b


def gram(X):
    X = np.asarray(X, dtype=float)
    return X @ X.T
''',
"explanation": r'''
The loop version spells out $C_{ij} = \sum_k A_{ik}B_{kj}$; `@` performs the same computation in
compiled code. Checking `A.shape[1] == B.shape[0]` first produces a clear message. Scoring a batch
is one matrix–vector product plus a broadcast scalar, and the Gram matrix collects every pairwise
dot product of the rows.
''',
"tests": r'''
import numpy as np


class TestMatmul(unittest.TestCase):
    def test_small(self):
        out = S.matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        np.testing.assert_array_equal(out, [[19, 22], [43, 50]])
        self.assertIsInstance(out, np.ndarray)

    def test_loops_match_numpy(self):
        rng = np.random.default_rng(0)
        A = rng.integers(-5, 5, size=(4, 3)).tolist()
        B = rng.integers(-5, 5, size=(3, 6)).tolist()
        self.assertEqual(S.matmul_loops(A, B), S.matmul(A, B).tolist())

    def test_not_elementwise(self):
        A = np.array([[1, 2], [3, 4]])
        self.assertFalse(np.array_equal(S.matmul(A, A), A * A))

    def test_shape_error(self):
        with self.assertRaises(ValueError) as ctx:
            S.matmul(np.ones((3, 2)), np.ones((3, 2)))
        self.assertIn("(3, 2)", str(ctx.exception))
        with self.assertRaises(ValueError):
            S.matmul_loops([[1, 2]], [[1, 2]])

    def test_rectangular_shape(self):
        self.assertEqual(S.matmul(np.ones((2, 5)), np.ones((5, 3))).shape, (2, 3))

    def test_batch_scores(self):
        np.testing.assert_allclose(S.batch_scores([[1, 2], [3, 4], [5, 6]], [0.5, -1.0], 0.1), [-1.4, -2.4, -3.4])
        self.assertEqual(S.batch_scores(np.ones((7, 3)), np.ones(3), 0).shape, (7,))

    def test_gram(self):
        X = np.array([[1.0, 2.0], [3.0, 4.0], [0.0, 1.0]])
        G = S.gram(X)
        self.assertEqual(G.shape, (3, 3))
        np.testing.assert_allclose(G, G.T)
        self.assertAlmostEqual(G[0, 1], 1 * 3 + 2 * 4)
''',
"feedback": [
    ("test_loops_match_numpy", "Entry (i, j) is the sum over k of A[i][k] * B[k][j]."),
    ("test_not_elementwise", "Use `@` (matrix product), not `*` (element-wise)."),
    ("test_shape_error", "Check `A.shape[1] != B.shape[0]` and include both shapes in the message."),
    ("test_batch_scores", "Compute `X @ w + b` with float arrays."),
    ("test_gram", "The Gram matrix is `X @ X.T`, shape (rows, rows)."),
],
"library": {
"text": r'''
`@` calls `np.matmul`; `np.dot` and `np.einsum("ik,kj->ij", A, B)` are equivalent spellings for
2-D arrays. NumPy hands large products to an optimised BLAS library, which is why `@` is far
faster than the triple loop. The tests check all three spellings agree with your function.
''',
"tests": r'''
class TestAgainstLibrary(unittest.TestCase):
    def test_equivalent_spellings(self):
        A = np.arange(6.0).reshape(2, 3)
        B = np.arange(12.0).reshape(3, 4)
        out = S.matmul(A, B)
        np.testing.assert_allclose(out, np.dot(A, B))
        np.testing.assert_allclose(out, np.einsum("ik,kj->ij", A, B))
''',
},
},
]
