"""Problem definitions for the mathematics topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- dot-product
{
"slug": "dot-product", "title": "Dot Product",
"difficulty": "beginner", "prereqs": ["summation"], "packages": [],
"objectives": ["Compute a dot product", "Validate equal lengths",
               "Interpret the sign of a dot product geometrically"],
"tags": ["vectors", "dot-product", "linear-algebra"],
"sources": ["S009"], "entry": "dot(u, v)",
"article": r'''
# The Dot Product

## Intuition
The dot product measures how much two vectors point in the same direction. Large and positive:
they agree; zero: perpendicular; negative: they point away from each other. A linear model's
prediction $w \cdot x$ is exactly "how well does the input agree with the weights".

## Precise explanation
For $u, v \in \mathbb{R}^n$:
$$u \cdot v = \sum_{i=1}^{n} u_i v_i.$$
Geometrically $u \cdot v = \lVert u\rVert\,\lVert v\rVert \cos\theta$, where $\theta$ is the
angle between them. It is only defined when both vectors have the same length $n$.

Properties: symmetric ($u\cdot v = v\cdot u$), linear in each argument, and
$u \cdot u = \lVert u\rVert^2 \ge 0$.

```python
total = 0
for a, b in zip(u, v):
    total += a * b
```

## Worked example
$u = (1, 2, 3)$, $v = (4, -5, 6)$: $1\cdot4 + 2\cdot(-5) + 3\cdot6 = 4 - 10 + 18 = 12$.
$(1, 0)\cdot(0, 1) = 0$ — perpendicular axes.

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="170" viewBox="0 0 260 170" role="img" aria-label="Two arrows from a common origin with the angle theta between them">
<title>Dot product and angle</title>
<line x1="30" y1="140" x2="230" y2="140" stroke="#999"/><line x1="30" y1="140" x2="30" y2="10" stroke="#999"/>
<line x1="30" y1="140" x2="210" y2="110" stroke="#1f77b4" stroke-width="3"/><text x="200" y="102" font-size="14" fill="#1f77b4">u</text>
<line x1="30" y1="140" x2="110" y2="30" stroke="#d62728" stroke-width="3"/><text x="112" y="28" font-size="14" fill="#d62728">v</text>
<path d="M 80 132 A 50 50 0 0 0 60 100" fill="none" stroke="#333"/><text x="70" y="118" font-size="13">θ</text>
</svg>

*Figure (original): u·v = ‖u‖‖v‖cos θ — positive here because θ < 90°.*

## Common mistakes
* Using `zip` without checking lengths: `zip` silently truncates to the shorter vector.
* Confusing the dot product (a number) with element-wise multiplication (a vector).
* Starting the accumulator from `u[0]*v[0]` and then looping over all elements again.

## Why this matters
Dot products are the core operation of linear regression, neural network layers, cosine
similarity in NLP retrieval and attention scores in transformers.
''',
"statement": r'''
Write `dot(u, v)` returning the dot product of two equal-length lists of numbers.

* Raise `ValueError` if the lengths differ.
* The dot product of two empty vectors is `0`.
* Do not use NumPy.

**Examples**
```python
dot([1, 2, 3], [4, -5, 6])   # 12
dot([1, 0], [0, 1])          # 0   — perpendicular
dot([1, 2], [1, 2, 3])       # raises ValueError
```
''',
"starter": r'''
def dot(u, v):
    """Return the dot product of equal-length vectors u and v."""
    # TODO
    pass
''',
"hints": [
    "Compare `len(u)` and `len(v)` first.",
    "`zip(u, v)` pairs up corresponding elements.",
    "Accumulate `total += a * b` starting from 0.",
],
"solution": r'''
def dot(u, v):
    if len(u) != len(v):
        raise ValueError("vectors must have the same length")
    total = 0
    for a, b in zip(u, v):
        total += a * b
    return total
''',
"explanation": r'''
Length validation protects against `zip` silently truncating. The accumulator starts at 0 (the
additive identity), so empty vectors correctly give 0, and each pair contributes its product.
''',
"tests": r'''
class TestDot(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.dot([1, 2, 3], [4, -5, 6]), 12)

    def test_perpendicular(self):
        self.assertEqual(S.dot([1, 0], [0, 1]), 0)

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.dot([1, 2], [1, 2, 3])

    def test_empty(self):
        self.assertEqual(S.dot([], []), 0)

    def test_symmetric(self):
        u, v = [0.5, -1.25, 3.0], [2.0, 4.0, -1.0]
        self.assertAlmostEqual(S.dot(u, v), S.dot(v, u), places=12)

    def test_self_is_squared_norm(self):
        self.assertAlmostEqual(S.dot([3, 4], [3, 4]), 25)

    def test_floats(self):
        self.assertAlmostEqual(S.dot([0.1, 0.2], [0.3, 0.4]), 0.11, places=12)
''',
"feedback": [
    ("test_mismatch", "zip stops at the shorter list — check lengths explicitly."),
    ("test_empty", "Start the accumulator at 0, not at u[0]*v[0]."),
    ("test_floats", "Floats are compared with tolerance 1e-12; return a number."),
    ("test_example", "Multiply corresponding elements and add them up."),
],
},
# ---------------------------------------------------------------- vector-norm-unit
{
"slug": "vector-norm-unit", "title": "Vector Norm and Unit Vector",
"difficulty": "beginner", "prereqs": ["dot-product"], "packages": [],
"objectives": ["Compute L1, L2 and L∞ norms", "Normalise a vector to unit length",
               "Handle the zero vector"],
"tags": ["vectors", "norms", "normalisation"],
"sources": ["S009"], "entry": "norm(v, p=2); unit(v)",
"article": r'''
# Norms: How Long is a Vector?

## Intuition
A norm assigns a length to a vector. Different norms measure length differently, like walking
distance in a city grid (L1) versus as-the-crow-flies distance (L2).

## Precise explanation
For $v \in \mathbb{R}^n$:
* L1 (Manhattan): $\lVert v\rVert_1 = \sum_i |v_i|$
* L2 (Euclidean): $\lVert v\rVert_2 = \sqrt{\sum_i v_i^2} = \sqrt{v\cdot v}$
* L∞ (max): $\lVert v\rVert_\infty = \max_i |v_i|$

Every norm satisfies $\lVert v\rVert \ge 0$, with equality only for the zero vector, and
$\lVert c v\rVert = |c|\,\lVert v\rVert$.

A **unit vector** has L2 norm 1: $\hat v = v / \lVert v\rVert_2$. It keeps the direction and
discards the magnitude. The zero vector has no direction, so it cannot be normalised.

In Python, `float("inf")` represents ∞ and `math.sqrt` / `math.hypot` compute square roots.

## Worked example
$v = (3, -4)$: L1 = 7, L2 = 5, L∞ = 4; unit vector = (0.6, −0.8).

## Common mistakes
* Forgetting absolute values in L1 and L∞ (negative entries).
* Normalising by the L1 norm when "unit vector" means L2.
* Dividing by zero for the zero vector instead of raising an error.

## Why this matters
L2 norms measure errors and distances (k-NN, k-means); L1 and L2 penalties regularise models
(ridge regression, [[ridge-regression]]); gradient clipping in DL and federated learning ([[update-clipping]]) rescales by the
norm.
''',
"statement": r'''
Implement:
* `norm(v, p=2)` for `p` in `{1, 2, float("inf")}`; raise `ValueError` for any other `p`.
  The norm of an empty vector is `0.0`.
* `unit(v)` returning a new list `v / ‖v‖₂`; raise `ValueError` for a zero (or empty) vector.

**Examples**
```python
norm([3, -4])               # 5.0
norm([3, -4], p=1)          # 7.0
norm([3, -4], p=float("inf"))  # 4.0
unit([3, -4])               # [0.6, -0.8]
unit([0, 0])                # raises ValueError
```
''',
"starter": r'''
import math


def norm(v, p=2):
    """Return the L1, L2 or L-infinity norm of v."""
    # TODO
    pass


def unit(v):
    """Return v scaled to unit L2 length."""
    # TODO
    pass
''',
"hints": [
    "L1: `sum(abs(x) for x in v)`; L∞: `max(abs(x) for x in v)` (watch the empty case).",
    "L2: `math.sqrt(sum(x * x for x in v))`.",
    "In `unit`, compute `n = norm(v)` once and raise if `n == 0`.",
],
"solution": r'''
import math


def norm(v, p=2):
    if not v:
        if p in (1, 2, math.inf):
            return 0.0
    if p == 1:
        return float(sum(abs(x) for x in v))
    if p == 2:
        return math.sqrt(sum(x * x for x in v))
    if p == math.inf:
        return float(max(abs(x) for x in v))
    raise ValueError("p must be 1, 2 or inf")


def unit(v):
    n = norm(v)
    if n == 0:
        raise ValueError("cannot normalise the zero vector")
    return [x / n for x in v]
''',
"explanation": r'''
Each norm is a direct translation of its formula. The empty-vector branch returns 0.0 for
valid `p` (avoiding `max()` of an empty sequence) and falls through to the final `raise` for an
invalid `p`. `unit` reuses the L2 norm and refuses to divide by zero.
''',
"tests": r'''
class TestNorms(unittest.TestCase):
    def test_l2(self):
        self.assertAlmostEqual(S.norm([3, -4]), 5.0)

    def test_l1(self):
        self.assertAlmostEqual(S.norm([3, -4], p=1), 7.0)

    def test_linf(self):
        self.assertAlmostEqual(S.norm([3, -4, 1], p=float("inf")), 4.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.norm([1, 2], p=3)

    def test_empty(self):
        self.assertEqual(S.norm([]), 0.0)

    def test_unit(self):
        u = S.unit([3, -4])
        self.assertAlmostEqual(u[0], 0.6)
        self.assertAlmostEqual(u[1], -0.8)

    def test_unit_has_length_one(self):
        u = S.unit([1, 2, 2, 4])
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in u)), 1.0, places=12)

    def test_unit_zero(self):
        with self.assertRaises(ValueError):
            S.unit([0, 0])
''',
"feedback": [
    ("test_linf", "Take the maximum of absolute values, not of raw values."),
    ("test_l1", "Use abs() on each element."),
    ("test_unit_zero", "Raise ValueError before dividing by a zero norm."),
    ("test_empty", "Return 0.0 for an empty vector (max() of an empty list raises)."),
],
},
# ---------------------------------------------------------------- matrix-multiply
{
"slug": "matrix-multiply", "title": "Matrix Multiplication",
"difficulty": "beginner", "prereqs": ["dot-product", "matrix-transpose"], "packages": [],
"objectives": ["Multiply matrices with the row-by-column rule", "Check shape compatibility",
               "Recognise that AB ≠ BA in general"],
"tags": ["matrices", "matrix-multiplication", "shapes"],
"sources": ["S009"], "entry": "matmul(A, B)",
"article": r'''
# Matrix Multiplication

## Intuition
Each entry of a product $AB$ is a dot product: row $i$ of $A$ with column $j$ of $B$. A matrix
can be seen as a machine that transforms vectors; multiplying matrices composes the machines.

## Precise explanation
If $A$ is $m\times n$ and $B$ is $n\times p$, then $C = AB$ is $m\times p$ with
$$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}.$$
The inner dimensions must match ($n$). The shapes "cancel" like dominoes:
$(m\times \mathbf{n})(\mathbf{n}\times p) = m\times p$.

Properties: associative, $(AB)C = A(BC)$; distributive; **not** commutative — $AB$ and $BA$
usually differ, and one may not even be defined. The identity matrix $I$ satisfies $AI = IA = A$.

```mermaid
flowchart LR
  A["A (m×n)"] --> C["C = AB (m×p)"]
  B["B (n×p)"] --> C
  C --> e["C[i][j] = row i of A · column j of B"]
```

## Worked example
$$\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}5&6\\7&8\end{pmatrix}
=\begin{pmatrix}1\cdot5+2\cdot7 & 1\cdot6+2\cdot8\\ 3\cdot5+4\cdot7 & 3\cdot6+4\cdot8\end{pmatrix}
=\begin{pmatrix}19&22\\43&50\end{pmatrix}.$$
Reversing the order gives $\begin{pmatrix}23&34\\31&46\end{pmatrix}$ — different.

## Common mistakes
* Multiplying element-wise (the Hadamard product) instead.
* Checking `len(A) == len(B)` instead of columns of A vs rows of B.
* Pre-allocating with `[[0]*p]*m` (aliased rows — see [[matrix-transpose]]).

## Why this matters
A dense neural-network layer is $XW$; a batch of predictions from linear regression is $Xw$;
attention is $\text{softmax}(QK^\top)V$. Shape reasoning is the most useful debugging skill in ML.
''',
"statement": r'''
Write `matmul(A, B)` multiplying two matrices given as lists of rows (pure Python).

* Raise `ValueError` if `A` or `B` is empty/ragged, or if `len(A[0]) != len(B)`.
* Return a new list of lists of shape `len(A) × len(B[0])`.

**Examples**
```python
matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])   # [[19, 22], [43, 50]]
matmul([[1, 2, 3]], [[1], [0], [-1]])        # [[-2]]   — (1×3)(3×1) = 1×1
matmul([[1, 2]], [[1, 2]])                   # raises ValueError — (1×2)(1×2)
```
''',
"starter": r'''
def matmul(A, B):
    """Return the matrix product A @ B for lists of rows."""
    # TODO: validate shapes, then compute C[i][j] = sum_k A[i][k] * B[k][j]
    pass
''',
"hints": [
    "Write a helper that checks a matrix is non-empty and rectangular.",
    "Compatibility: number of columns of A (`len(A[0])`) must equal rows of B (`len(B)`).",
    "Triple loop over i, j, k, or a comprehension using `zip(*B)` to get B's columns.",
],
"solution": r'''
def _shape(M):
    if not M or not M[0]:
        raise ValueError("matrix must be non-empty")
    n = len(M[0])
    if any(len(row) != n for row in M):
        raise ValueError("ragged matrix")
    return len(M), n


def matmul(A, B):
    m, n = _shape(A)
    n2, p = _shape(B)
    if n != n2:
        raise ValueError(f"incompatible shapes ({m}x{n}) and ({n2}x{p})")
    cols = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in cols] for row in A]
''',
"explanation": r'''
`_shape` validates each matrix and returns its dimensions. After checking the inner dimensions,
`zip(*B)` gives B's columns (safe now that B is rectangular), and each output entry is the dot
product of a row of A with a column of B — the definition, written once.
''',
"tests": r'''
class TestMatmul(unittest.TestCase):
    def test_2x2(self):
        self.assertEqual(S.matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_not_commutative(self):
        self.assertEqual(S.matmul([[5, 6], [7, 8]], [[1, 2], [3, 4]]), [[23, 34], [31, 46]])

    def test_row_times_column(self):
        self.assertEqual(S.matmul([[1, 2, 3]], [[1], [0], [-1]]), [[-2]])

    def test_column_times_row(self):
        self.assertEqual(S.matmul([[1], [2]], [[3, 4]]), [[3, 4], [6, 8]])

    def test_incompatible(self):
        with self.assertRaises(ValueError):
            S.matmul([[1, 2]], [[1, 2]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.matmul([[1, 2], [3]], [[1], [2]])

    def test_identity(self):
        A = [[2, -1, 0], [4, 3, 5]]
        I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(S.matmul(A, I), A)

    def test_shape(self):
        C = S.matmul([[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]])
        self.assertEqual((len(C), len(C[0])), (2, 2))
        self.assertEqual(C, [[4, 5], [10, 11]])
''',
"feedback": [
    ("test_incompatible", "Compare columns of A with rows of B: len(A[0]) vs len(B)."),
    ("test_2x2", "Entry (i, j) is row i of A dotted with column j of B — not element-wise."),
    ("test_column_times_row", "Output shape is len(A) × len(B[0])."),
    ("test_ragged", "Validate every row length."),
],
},
# ---------------------------------------------------------------- binomial-coefficient
{
"slug": "binomial-coefficient", "title": "Binomial Coefficient",
"difficulty": "intermediate", "prereqs": ["summation", "factorial-validated"], "packages": [],
"objectives": ["Count combinations", "Use the multiplicative formula to avoid huge factorials",
               "Exploit symmetry C(n,k) = C(n,n-k)"],
"tags": ["combinatorics", "counting", "integers"],
"sources": ["S009"], "entry": "comb(n, k)",
"article": r'''
# Counting Combinations

## Intuition
"How many different 3-person teams can be chosen from 5 students?" Order does not matter, so
{Ann, Bob, Cy} is the same team as {Cy, Ann, Bob}. The answer is the **binomial coefficient**
$\binom{5}{3} = 10$.

## Precise explanation
$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}\quad (0\le k\le n),\qquad \binom{n}{k}=0 \text{ if } k>n.$$
Computing three factorials is wasteful. The **multiplicative formula** builds the result step by
step and stays an integer at every step:
$$\binom{n}{k} = \prod_{i=1}^{k} \frac{n-k+i}{i}.$$
```python
r = 1
for i in range(1, k + 1):
    r = r * (n - k + i) // i      # exact: r*(n-k+i) is always divisible by i
```
Because $\binom{n}{k} = \binom{n}{n-k}$, use `k = min(k, n - k)` to do fewer steps.

Pascal's rule $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ gives Pascal's triangle.

## Worked example
$\binom{5}{2}$: r = 1 → 1·4//1 = 4 → 4·5//2 = 10.

## Common mistakes
* Using `/` (float division) → large values lose precision (e.g. `comb(60, 30)`).
* Writing `r = r // i * (n-k+i)` — dividing first may not be exact.
* Forgetting $\binom{n}{0} = 1$ and $\binom{n}{k} = 0$ for $k > n$.

## Why this matters
Binomial coefficients give the binomial distribution ([[binomial-pmf]]), count subsets for exact Shapley
values ([[exact-shapley]]), and count n-gram / feature combinations.
''',
"statement": r'''
Write `comb(n, k)` returning $\binom{n}{k}$ as an exact `int` without using `math.comb` or
`math.factorial`.

* Return `0` if `k > n`.
* Raise `ValueError` if `n < 0` or `k < 0`.

**Constraints:** 0 ≤ n ≤ 2000.

**Examples**
```python
comb(5, 2)    # 10
comb(5, 0)    # 1
comb(3, 5)    # 0  — cannot choose 5 from 3
comb(60, 30)  # 118264581564861424  — exact integer
```
''',
"starter": r'''
def comb(n, k):
    """Return the binomial coefficient C(n, k) as an exact int."""
    # TODO
    pass
''',
"hints": [
    "Handle negatives (raise) and `k > n` (return 0) first.",
    "Replace `k` by `min(k, n - k)`.",
    "Loop `for i in range(1, k + 1): r = r * (n - k + i) // i`.",
],
"solution": r'''
def comb(n, k):
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    if k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r
''',
"explanation": r'''
After the edge cases, symmetry halves the work. Multiplying before the integer division keeps
the intermediate value an exact product of consecutive binomial coefficients, so `//` never
truncates. Python's arbitrary-precision ints keep large results exact.
''',
"tests": r'''
class TestComb(unittest.TestCase):
    def test_small(self):
        self.assertEqual(S.comb(5, 2), 10)

    def test_edges(self):
        self.assertEqual(S.comb(5, 0), 1)
        self.assertEqual(S.comb(5, 5), 1)
        self.assertEqual(S.comb(0, 0), 1)

    def test_k_greater(self):
        self.assertEqual(S.comb(3, 5), 0)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.comb(-1, 0)

    def test_large_exact(self):
        self.assertEqual(S.comb(60, 30), 118264581564861424)
        self.assertIsInstance(S.comb(60, 30), int)

    def test_symmetry(self):
        for n in range(15):
            for k in range(n + 1):
                self.assertEqual(S.comb(n, k), S.comb(n, n - k))

    def test_pascal_rule(self):
        for n in range(1, 20):
            for k in range(1, n):
                self.assertEqual(S.comb(n, k), S.comb(n - 1, k - 1) + S.comb(n - 1, k))

    def test_row_sum(self):
        self.assertEqual(sum(S.comb(10, k) for k in range(11)), 2 ** 10)
''',
"feedback": [
    ("test_large_exact", "Use integer `//` after multiplying, never `/`."),
    ("test_k_greater", "Return 0 when k > n."),
    ("test_edges", "C(n, 0) = C(n, n) = 1; check your loop for k = 0."),
    ("test_pascal_rule", "If small values are right but some are off by rounding, divide after multiplying."),
],
},
# ---------------------------------------------------------------- solve-2x2-cramer
{
"slug": "solve-2x2-cramer", "title": "Solve a 2x2 System (Cramer's Rule)",
"difficulty": "intermediate", "prereqs": ["matrix-multiply"], "packages": [],
"objectives": ["Compute a 2×2 determinant", "Solve a linear system with Cramer's rule",
               "Detect singular systems with a tolerance"],
"tags": ["linear-systems", "determinant", "cramers-rule", "floating-point"],
"sources": ["S009"], "entry": "solve_2x2(A, b, tol=1e-12)",
"article": r'''
# Solving Two Equations in Two Unknowns

## Intuition
Two linear equations are two lines in the plane; the solution is where they cross. If the lines
are parallel they never cross (no solution) or coincide (infinitely many). The **determinant**
tells you which case you are in.

## Precise explanation
System $A x = b$ with
$A = \begin{pmatrix}a&b\\c&d\end{pmatrix}$, $b = (e, f)$:
$$\det A = ad - bc.$$
If $\det A \ne 0$, **Cramer's rule** gives
$$x = \frac{e d - b f}{\det A},\qquad y = \frac{a f - e c}{\det A}.$$
Each numerator is the determinant of $A$ with one column replaced by the right-hand side.

**Floating-point care:** with real-world numbers, "zero" is rarely exactly 0.0. Treat the
matrix as singular when $|\det A| < \text{tol}$.

## Worked example
$2x + y = 5$, $x - y = 1$: $\det = 2(-1) - 1\cdot1 = -3$;
$x = (5\cdot(-1) - 1\cdot1)/(-3) = 2$; $y = (2\cdot1 - 5\cdot1)/(-3) = 1$. Check: $2·2+1=5$ ✓.

## Common mistakes
* Swapping $b$ and $c$ in the determinant.
* Testing `det == 0` exactly with floats.
* Forgetting to verify: substitute back and check the residual.

## Why this matters
Linear systems are solved inside least squares ([[least-squares-line]]), ridge regression ([[ridge-regression]]) and Newton's
method. Recognising near-singular systems explains why ML adds regularisation.
''',
"statement": r'''
Write `solve_2x2(A, b, tol=1e-12)` where `A = [[a, b], [c, d]]` and `b = [e, f]`.

* Return the solution `(x, y)` as floats.
* Raise `ValueError("singular")` if `abs(det) < tol`.
* Raise `ValueError` if `A` is not 2×2 or `b` does not have length 2.

**Examples**
```python
solve_2x2([[2, 1], [1, -1]], [5, 1])   # (2.0, 1.0)
solve_2x2([[1, 2], [2, 4]], [3, 6])    # raises ValueError — parallel lines (det = 0)
```
''',
"starter": r'''
def solve_2x2(A, b, tol=1e-12):
    """Solve A @ [x, y] = b for a 2x2 matrix A using Cramer's rule."""
    # TODO
    pass
''',
"hints": [
    "Unpack: `(a, b_), (c, d) = A` and `e, f = b` after checking shapes.",
    "`det = a * d - b_ * c`; raise if `abs(det) < tol`.",
    "`x = (e * d - b_ * f) / det`, `y = (a * f - e * c) / det`.",
],
"solution": r'''
def solve_2x2(A, b, tol=1e-12):
    if len(A) != 2 or any(len(r) != 2 for r in A) or len(b) != 2:
        raise ValueError("A must be 2x2 and b length 2")
    (a, b12), (c, d) = A
    e, f = b
    det = a * d - b12 * c
    if abs(det) < tol:
        raise ValueError("singular")
    x = (e * d - b12 * f) / det
    y = (a * f - e * c) / det
    return float(x), float(y)
''',
"explanation": r'''
The function validates shapes, computes the determinant, and treats tiny determinants as
singular using a tolerance. Cramer's rule then gives each unknown as a ratio of determinants.
The variable is named `b12` to avoid clashing with the right-hand-side vector `b`.
''',
"tests": r'''
class TestSolve(unittest.TestCase):
    def test_example(self):
        x, y = S.solve_2x2([[2, 1], [1, -1]], [5, 1])
        self.assertAlmostEqual(x, 2.0)
        self.assertAlmostEqual(y, 1.0)

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 2], [2, 4]], [3, 6])

    def test_near_singular_tolerance(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 1], [1, 1 + 1e-15]], [1, 2])

    def test_identity(self):
        self.assertEqual(S.solve_2x2([[1, 0], [0, 1]], [3.5, -2]), (3.5, -2.0))

    def test_residual(self):
        A, b = [[0.3, -1.7], [2.2, 0.9]], [1.1, -0.4]
        x, y = S.solve_2x2(A, b)
        self.assertAlmostEqual(A[0][0] * x + A[0][1] * y, b[0], places=10)
        self.assertAlmostEqual(A[1][0] * x + A[1][1] * y, b[1], places=10)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 2, 3], [4, 5, 6]], [1, 2])

    def test_returns_floats(self):
        x, y = S.solve_2x2([[2, 0], [0, 4]], [2, 2])
        self.assertIsInstance(x, float)
        self.assertEqual((x, y), (1.0, 0.5))
''',
"feedback": [
    ("test_example", "Check the determinant ad − bc and which numerator belongs to x vs y."),
    ("test_near_singular_tolerance", "Compare abs(det) < tol, not det == 0."),
    ("test_residual", "Substitute your answer back into both equations to debug."),
    ("test_bad_shape", "Validate that A is 2×2 and b has two entries."),
],
},
# ---------------------------------------------------------------- inverse-2x2
{
"slug": "inverse-2x2", "title": "Inverse of a 2x2 Matrix",
"difficulty": "intermediate", "prereqs": ["solve-2x2-cramer"], "packages": [],
"objectives": ["Compute the inverse via the adjugate formula", "Verify A·A⁻¹ = I numerically",
               "Explain when a matrix has no inverse"],
"tags": ["matrix-inverse", "determinant", "identity"],
"sources": ["S009"], "entry": "inverse_2x2(A, tol=1e-12)",
"article": r'''
# The Inverse of a 2×2 Matrix

## Intuition
If a matrix is a transformation (stretch, rotate, shear), its inverse is the transformation that
undoes it. A matrix that squashes the plane onto a line destroys information and cannot be
undone — it has no inverse.

## Precise explanation
For $A = \begin{pmatrix}a&b\\c&d\end{pmatrix}$ with $\det A = ad-bc \ne 0$:
$$A^{-1} = \frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}.$$
Recipe: swap the diagonal, negate the off-diagonal, divide by the determinant.
Check: $A A^{-1} = A^{-1} A = I$.

$|\det A|$ is the factor by which $A$ scales areas; $\det A = 0$ means area collapses to zero.

Numerically, solving $Ax=b$ directly ([[solve-2x2-cramer]]) is usually preferred over forming $A^{-1}$, but the
inverse is a useful concept and appears in closed-form formulas such as
$w = (X^\top X)^{-1}X^\top y$.

## Worked example
$A = \begin{pmatrix}4&7\\2&6\end{pmatrix}$, $\det = 24 - 14 = 10$,
$A^{-1} = \frac{1}{10}\begin{pmatrix}6&-7\\-2&4\end{pmatrix} = \begin{pmatrix}0.6&-0.7\\-0.2&0.4\end{pmatrix}$.

## Common mistakes
* Negating the diagonal instead of the off-diagonal.
* Forgetting to divide by the determinant.
* Comparing $AA^{-1}$ to $I$ with `==` — use a tolerance.

## Why this matters
Inverses appear in the normal equations, Gaussian covariance matrices and change-of-basis
arguments throughout ML theory.
''',
"statement": r'''
Write `inverse_2x2(A, tol=1e-12)` returning the inverse of a 2×2 matrix as a list of rows of
floats. Raise `ValueError` if `|det A| < tol` or if `A` is not 2×2.

**Examples**
```python
inverse_2x2([[4, 7], [2, 6]])   # [[0.6, -0.7], [-0.2, 0.4]]
inverse_2x2([[2, 4], [1, 2]])   # raises ValueError — det = 0
```
''',
"starter": r'''
def inverse_2x2(A, tol=1e-12):
    """Return the inverse of 2x2 matrix A."""
    # TODO
    pass
''',
"hints": [
    "Unpack `(a, b), (c, d) = A` and compute `det = a*d - b*c`.",
    "Raise ValueError if `abs(det) < tol`.",
    "Return `[[d/det, -b/det], [-c/det, a/det]]`.",
],
"solution": r'''
def inverse_2x2(A, tol=1e-12):
    if len(A) != 2 or any(len(r) != 2 for r in A):
        raise ValueError("A must be 2x2")
    (a, b), (c, d) = A
    det = a * d - b * c
    if abs(det) < tol:
        raise ValueError("matrix is singular")
    return [[d / det, -b / det], [-c / det, a / det]]
''',
"explanation": r'''
The adjugate formula is applied directly after shape and singularity checks. Dividing each entry
by the determinant produces floats.
''',
"tests": r'''
def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


class TestInverse(unittest.TestCase):
    def assertMatAlmost(self, X, Y, places=10):
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(X[i][j], Y[i][j], places=places)

    def test_example(self):
        self.assertMatAlmost(S.inverse_2x2([[4, 7], [2, 6]]), [[0.6, -0.7], [-0.2, 0.4]])

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.inverse_2x2([[2, 4], [1, 2]])

    def test_identity(self):
        self.assertMatAlmost(S.inverse_2x2([[1, 0], [0, 1]]), [[1, 0], [0, 1]])

    def test_product_is_identity(self):
        A = [[0.5, -1.25], [3.0, 2.0]]
        self.assertMatAlmost(_mm(A, S.inverse_2x2(A)), [[1, 0], [0, 1]])
        self.assertMatAlmost(_mm(S.inverse_2x2(A), A), [[1, 0], [0, 1]])

    def test_inverse_of_inverse(self):
        A = [[3, 1], [-2, 5]]
        self.assertMatAlmost(S.inverse_2x2(S.inverse_2x2(A)), A)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.inverse_2x2([[1, 2]])

    def test_diagonal(self):
        self.assertMatAlmost(S.inverse_2x2([[2, 0], [0, -4]]), [[0.5, 0], [0, -0.25]])
''',
"feedback": [
    ("test_example", "Swap the diagonal entries and negate the off-diagonal ones."),
    ("test_product_is_identity", "Divide every entry by the determinant."),
    ("test_singular", "Raise ValueError when |det| < tol."),
    ("test_bad_shape", "Check A has exactly two rows of length two."),
],
},
# ---------------------------------------------------------------- central-difference
{
"slug": "central-difference", "title": "Numerical Derivative (Central Difference)",
"difficulty": "intermediate", "prereqs": ["exp-log"], "packages": [],
"objectives": ["Approximate derivatives with finite differences", "Compare forward and central differences",
               "Understand the role of the step size h"],
"tags": ["calculus", "derivatives", "finite-differences", "numerical-methods"],
"sources": ["S009", "S013"], "entry": "forward_diff(f, x, h=1e-6); central_diff(f, x, h=1e-5)",
"article": r'''
# Numerical Derivatives

## Intuition
The derivative $f'(x)$ is the slope of the tangent line at $x$. We cannot draw a tangent with a
computer, but we can draw a **secant** through two nearby points and use its slope. The closer
the points, the better the approximation — up to the limits of floating-point arithmetic.

## Precise explanation
Definition: $f'(x) = \lim_{h\to 0} \frac{f(x+h) - f(x)}{h}$.
* **Forward difference:** $\frac{f(x+h)-f(x)}{h}$, error proportional to $h$ (first order).
* **Central difference:** $\frac{f(x+h)-f(x-h)}{2h}$, error proportional to $h^2$
  (second order), because the $f''$ terms in the Taylor expansions cancel.

Too-small $h$ causes **cancellation error**: $f(x+h)$ and $f(x-h)$ agree in most digits, so
their difference keeps few significant digits. With 64-bit floats, $h \approx 10^{-5}$ is a good
default for central differences.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="190" viewBox="0 0 300 190" role="img" aria-label="Curve with a tangent line at x and a secant line through x minus h and x plus h">
<title>Secant vs tangent</title>
<path d="M 20 170 Q 150 -40 280 120" fill="none" stroke="#333" stroke-width="2"/>
<line x1="60" y1="125" x2="250" y2="45" stroke="#2ca02c" stroke-width="2" stroke-dasharray="6 4"/>
<line x1="40" y1="128" x2="260" y2="52" stroke="#d62728" stroke-width="2"/>
<circle cx="110" cy="85" r="4" fill="#1f77b4"/><circle cx="205" cy="60" r="4" fill="#1f77b4"/>
<text x="95" y="105" font-size="12">x−h</text><text x="200" y="80" font-size="12">x+h</text>
<text x="220" y="40" font-size="12" fill="#2ca02c">secant</text><text x="235" y="70" font-size="12" fill="#d62728">tangent</text>
</svg>

*Figure (original): the central-difference secant through x−h and x+h is nearly parallel to the
tangent at x.*

## Worked example
$f(x) = x^3$ at $x=2$ (exact $f'(2)=12$), $h = 0.1$:
forward: $(2.1^3 - 8)/0.1 = 12.61$; central: $(2.1^3 - 1.9^3)/0.2 = 12.01$.

## Common mistakes
* Using $h = 10^{-15}$ "for accuracy" — rounding error dominates.
* Dividing the central difference by $h$ instead of $2h$.
* Expecting an exact match with the analytic derivative; always compare with a tolerance.

## Why this matters
Finite differences check that hand-written gradients are correct ([[gradient-check]]) and power the numerical
gradient ([[numerical-gradient]]) and integrated-gradients approximations ([[integrated-gradients]]).
''',
"statement": r'''
Implement:
* `forward_diff(f, x, h=1e-6)` → $(f(x+h)-f(x))/h$
* `central_diff(f, x, h=1e-5)` → $(f(x+h)-f(x-h))/(2h)$

Both raise `ValueError` if `h <= 0`. `f` is any Python function of one float.

**Examples**
```python
central_diff(lambda x: x**3, 2.0)        # ≈ 12.0  (within 1e-6)
forward_diff(lambda x: x**3, 2.0, h=0.1) # 12.61   (first-order error)
central_diff(lambda x: x**3, 2.0, h=0.1) # 12.01   (second-order error)
```
''',
"starter": r'''
def forward_diff(f, x, h=1e-6):
    """Forward-difference estimate of f'(x)."""
    # TODO
    pass


def central_diff(f, x, h=1e-5):
    """Central-difference estimate of f'(x)."""
    # TODO
    pass
''',
"hints": [
    "Validate `h > 0` first.",
    "Forward: one extra evaluation at `x + h`.",
    "Central: evaluate at `x + h` and `x - h` and divide by `2 * h`.",
],
"solution": r'''
def forward_diff(f, x, h=1e-6):
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x)) / h


def central_diff(f, x, h=1e-5):
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x - h)) / (2 * h)
''',
"explanation": r'''
Both functions translate their formulas directly. The central version evaluates symmetrically
around x, so the leading error term cancels and the estimate is far more accurate for the same h.
''',
"tests": r'''
class TestDiff(unittest.TestCase):
    def test_central_cubic(self):
        self.assertAlmostEqual(S.central_diff(lambda x: x ** 3, 2.0), 12.0, delta=1e-6)

    def test_forward_h01(self):
        self.assertAlmostEqual(S.forward_diff(lambda x: x ** 3, 2.0, h=0.1), 12.61, places=9)

    def test_central_h01(self):
        self.assertAlmostEqual(S.central_diff(lambda x: x ** 3, 2.0, h=0.1), 12.01, places=9)

    def test_sin(self):
        self.assertAlmostEqual(S.central_diff(math.sin, 0.7), math.cos(0.7), delta=1e-8)

    def test_exp(self):
        self.assertAlmostEqual(S.central_diff(math.exp, 1.0), math.e, delta=1e-7)

    def test_bad_h(self):
        with self.assertRaises(ValueError):
            S.central_diff(math.sin, 0.0, h=0)
        with self.assertRaises(ValueError):
            S.forward_diff(math.sin, 0.0, h=-1e-3)

    def test_central_more_accurate(self):
        f, x, h = math.exp, 0.5, 1e-3
        ef = abs(S.forward_diff(f, x, h) - math.exp(x))
        ec = abs(S.central_diff(f, x, h) - math.exp(x))
        self.assertLess(ec, ef / 100)
''',
"feedback": [
    ("test_central_h01", "Divide by 2*h in the central difference."),
    ("test_forward_h01", "Forward difference uses f(x+h) − f(x) over h."),
    ("test_bad_h", "Raise ValueError when h <= 0."),
    ("test_central_more_accurate", "Make sure central_diff evaluates at x−h, not at x."),
],
},
# ---------------------------------------------------------------- trapezoid-rule
{
"slug": "trapezoid-rule", "title": "Trapezoidal Integration",
"difficulty": "intermediate", "prereqs": ["central-difference"], "packages": [],
"objectives": ["Approximate a definite integral", "Implement the composite trapezoidal rule",
               "Observe error shrinking as n grows"],
"tags": ["calculus", "integration", "numerical-methods"],
"sources": ["S009", "S013"], "entry": "trapezoid(f, a, b, n)",
"article": r'''
# Area Under a Curve with Trapezoids

## Intuition
To estimate the area under a curve, slice it into thin vertical strips and approximate each
strip by a trapezoid (straight top). More strips → better fit.

## Precise explanation
Split $[a, b]$ into $n$ equal pieces of width $h = (b-a)/n$ with points $x_i = a + ih$.
$$\int_a^b f(x)\,dx \approx h\left[\tfrac12 f(x_0) + f(x_1) + \dots + f(x_{n-1}) + \tfrac12 f(x_n)\right].$$
The ends get weight ½ because each interior point is shared by two trapezoids.
The error shrinks roughly like $h^2$: doubling $n$ cuts the error by about 4.
The rule is exact for straight lines. If $a > b$, the formula naturally gives a negative value,
matching $\int_a^b = -\int_b^a$.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="170" viewBox="0 0 300 170" role="img" aria-label="A curve over four trapezoids whose tops are straight chords of the curve">
<title>Composite trapezoidal rule with n = 4</title>
<line x1="20" y1="150" x2="290" y2="150" stroke="#999"/>
<polygon points="40,150 40,110 100,70 100,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="100,150 100,70 160,50 160,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="160,150 160,50 220,60 220,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="220,150 220,60 280,100 280,150" fill="#aec7e8" stroke="#1f77b4"/>
<path d="M 40 110 C 80 60, 140 35, 180 48 S 260 75, 280 100" fill="none" stroke="#d62728" stroke-width="2"/>
<text x="35" y="165" font-size="12">a</text><text x="276" y="165" font-size="12">b</text>
</svg>

*Figure (original): four trapezoids approximating the area under the red curve.*

## Worked example
$\int_0^1 x^2 dx = 1/3$. With $n=2$, $h=0.5$: $0.5[\tfrac12\cdot0 + 0.25 + \tfrac12\cdot1] = 0.375$.
With $n = 4$: $0.34375$. Errors 0.0417 → 0.0104 (≈4× smaller).

## Common mistakes
* Giving the endpoints weight 1.
* Using `range(n)` and missing $x_n = b$.
* Computing $x_i$ by repeated addition (`x += h`) — rounding drift; use `a + i*h`.

## Why this matters
Numerical integration computes probabilities from densities, areas under ROC curves, and the path
integral in integrated gradients ([[integrated-gradients]]).
''',
"statement": r'''
Write `trapezoid(f, a, b, n)` implementing the composite trapezoidal rule with `n` equal
sub-intervals. Raise `ValueError` if `n` is not a positive int. Allow `a > b` (negative area) and
`a == b` (returns 0.0).

**Examples**
```python
trapezoid(lambda x: x**2, 0, 1, 2)   # 0.375
trapezoid(lambda x: 3*x + 1, 0, 2, 1)  # 8.0  — exact for straight lines
trapezoid(lambda x: x**2, 1, 0, 2)   # -0.375 — reversed limits
```
''',
"starter": r'''
def trapezoid(f, a, b, n):
    """Composite trapezoidal approximation of the integral of f from a to b."""
    # TODO
    pass
''',
"hints": [
    "`h = (b - a) / n`; the points are `a + i * h` for i = 0..n.",
    "Start with `0.5 * (f(a) + f(b))` then add interior points i = 1..n−1.",
    "Multiply the total by `h` at the end.",
],
"solution": r'''
def trapezoid(f, a, b, n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive int")
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
''',
"explanation": r'''
The endpoints are weighted by ½ and each interior point by 1, then everything is multiplied by
the strip width h. Points are computed as `a + i*h` to avoid accumulated rounding. A negative h
(for a > b) automatically gives a negative integral.
''',
"tests": r'''
class TestTrapezoid(unittest.TestCase):
    def test_n2(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: x ** 2, 0, 1, 2), 0.375)

    def test_linear_exact(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: 3 * x + 1, 0, 2, 1), 8.0)

    def test_reversed(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: x ** 2, 1, 0, 2), -0.375)

    def test_zero_width(self):
        self.assertEqual(S.trapezoid(math.sin, 2.0, 2.0, 5), 0.0)

    def test_sin_converges(self):
        self.assertAlmostEqual(S.trapezoid(math.sin, 0, math.pi, 1000), 2.0, delta=1e-5)

    def test_error_quarters(self):
        f, exact = (lambda x: x ** 2), 1 / 3
        e1 = abs(S.trapezoid(f, 0, 1, 10) - exact)
        e2 = abs(S.trapezoid(f, 0, 1, 20) - exact)
        self.assertAlmostEqual(e1 / e2, 4.0, delta=0.01)

    def test_bad_n(self):
        for bad in (0, -3, 2.0):
            with self.assertRaises(ValueError):
                S.trapezoid(math.sin, 0, 1, bad)
''',
"feedback": [
    ("test_n2", "Endpoints get weight ½, interior points weight 1, then multiply by h."),
    ("test_linear_exact", "With n = 1 the result is h·(f(a)+f(b))/2."),
    ("test_error_quarters", "Make sure you include all n−1 interior points."),
    ("test_bad_n", "n must be a positive int; reject floats and values < 1."),
],
},
# ---------------------------------------------------------------- gradient-descent-1d
{
"slug": "gradient-descent-1d", "title": "Gradient Descent in 1D",
"difficulty": "advanced", "prereqs": ["derivative-rules"], "packages": [],
"objectives": ["Implement the gradient-descent update", "Use a convergence tolerance and step cap",
               "Explain divergence when the learning rate is too large"],
"tags": ["optimisation", "gradient-descent", "learning-rate", "convergence"],
"sources": ["S009", "S013"], "entry": "gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8)",
"article": r'''
# Gradient Descent

## Intuition
Standing on a hillside in fog, you can feel which way is downhill under your feet. Take a step
that way, feel again, repeat. That is gradient descent: follow the negative slope to reach a
minimum.

## Precise explanation
To minimise $f(x)$, start at $x_0$ and repeat
$$x_{t+1} = x_t - \eta\, f'(x_t),$$
where $\eta > 0$ is the **learning rate**. Stop when the step is tiny,
$|x_{t+1} - x_t| < \text{tol}$, or after a maximum number of steps.

For $f(x) = (x-3)^2$, $f'(x) = 2(x-3)$, so
$x_{t+1} - 3 = (1 - 2\eta)(x_t - 3)$. The error is multiplied by $1-2\eta$ each step:
* $0 < \eta < 1$: $|1-2\eta| < 1$ → converges;
* $\eta = 1$: oscillates forever between two points;
* $\eta > 1$: $|1-2\eta| > 1$ → **diverges**.

```mermaid
flowchart LR
  s[x_t] --> g["compute slope f'(x_t)"] --> u["x_{t+1} = x_t − η·f'(x_t)"] --> c{"|step| < tol ?"}
  c -- no --> s
  c -- yes --> d[return x]
```

## Worked example
$f(x)=(x-3)^2$, $x_0 = 0$, $\eta = 0.25$: error multiplier $0.5$; iterates 0 → 1.5 → 2.25 →
2.625 → … → 3.

## Common mistakes
* Adding the gradient (`x + lr*g`) — that climbs uphill.
* Testing convergence on $f'(x)$ with a tolerance far smaller than the step can resolve.
* Looping forever without a step cap when the learning rate diverges.

## Why this matters
Every neural network, logistic regression ([[logistic-regression]]) and federated client update ([[local-sgd]]) is trained
with a variant of this loop.
''',
"statement": r'''
Write `gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8)`.

* `df` is the derivative function. Update `x = x - lr * df(x)`.
* Stop when `abs(step) < tol` (after applying that step) or after `max_steps` updates.
* Return `(x, history)` where `history` lists every iterate **including** `x0`.
* Raise `ValueError` if `lr <= 0` or `max_steps < 1`.
* If `x` becomes non-finite (inf/nan), stop and return immediately.

**Examples**
```python
x, h = gradient_descent(lambda x: 2*(x-3), 0.0, 0.25)
# x ≈ 3.0; h[:4] == [0.0, 1.5, 2.25, 2.625]
x, h = gradient_descent(lambda x: 2*(x-3), 0.0, 1.5, max_steps=5)
# diverges: len(h) == 6 and |x - 3| grows each step
```
''',
"starter": r'''
import math


def gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8):
    """Minimise a 1D function given its derivative df. Return (x, history)."""
    history = [x0]
    # TODO
    return x0, history
''',
"hints": [
    "Validate `lr` and `max_steps` first.",
    "In the loop: `step = lr * df(x)`, `x = x - step`, append `x`.",
    "Break when `abs(step) < tol` or `not math.isfinite(x)`.",
],
"solution": r'''
import math


def gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8):
    if lr <= 0:
        raise ValueError("lr must be positive")
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")
    x = x0
    history = [x]
    for _ in range(max_steps):
        step = lr * df(x)
        x = x - step
        history.append(x)
        if not math.isfinite(x) or abs(step) < tol:
            break
    return x, history
''',
"explanation": r'''
Each iteration computes the step from the current slope, moves against it, and records the new
point. The loop ends on a tiny step (converged), a non-finite value (diverged) or the step cap,
so it always terminates.
''',
"tests": r'''
def df(x):
    return 2 * (x - 3)


class TestGD(unittest.TestCase):
    def test_converges(self):
        x, h = S.gradient_descent(df, 0.0, 0.25)
        self.assertAlmostEqual(x, 3.0, delta=1e-7)

    def test_first_iterates(self):
        _, h = S.gradient_descent(df, 0.0, 0.25)
        for got, exp in zip(h[:4], [0.0, 1.5, 2.25, 2.625]):
            self.assertAlmostEqual(got, exp)

    def test_diverges_with_large_lr(self):
        x, h = S.gradient_descent(df, 0.0, 1.5, max_steps=5)
        self.assertEqual(len(h), 6)
        errs = [abs(v - 3) for v in h]
        self.assertTrue(all(errs[i + 1] > errs[i] for i in range(5)))

    def test_max_steps_respected(self):
        _, h = S.gradient_descent(df, 0.0, 0.01, max_steps=3)
        self.assertEqual(len(h), 4)

    def test_already_at_min(self):
        x, h = S.gradient_descent(df, 3.0, 0.1)
        self.assertEqual(x, 3.0)
        self.assertEqual(len(h), 2)

    def test_bad_lr(self):
        with self.assertRaises(ValueError):
            S.gradient_descent(df, 0.0, 0.0)

    def test_quartic(self):
        x, _ = S.gradient_descent(lambda x: 4 * (x - 1) ** 3, 2.0, 0.1, max_steps=20000, tol=1e-12)
        self.assertAlmostEqual(x, 1.0, delta=1e-2)

    def test_nonfinite_stops(self):
        x, h = S.gradient_descent(lambda x: x * x * x, 10.0, 1.0, max_steps=50)
        self.assertFalse(math.isfinite(x))
        self.assertLess(len(h), 51)
''',
"feedback": [
    ("test_first_iterates", "Update with x − lr·df(x) (minus sign) and include x0 in history."),
    ("test_already_at_min", "When the first step is 0 you should stop after one update."),
    ("test_max_steps_respected", "history has max_steps + 1 entries when the cap is hit."),
    ("test_nonfinite_stops", "Use math.isfinite to stop on overflow."),
],
},
# ---------------------------------------------------------------- numerical-gradient
{
"slug": "numerical-gradient", "title": "Numerical Gradient of f(x1..xn)",
"difficulty": "advanced", "prereqs": ["central-difference", "gradient-descent-1d"], "packages": [],
"objectives": ["Define partial derivatives and the gradient", "Approximate each partial with central differences",
               "Use the gradient in multivariable descent"],
"tags": ["multivariable-calculus", "gradient", "partial-derivatives", "optimisation"],
"sources": ["S009", "S016"], "entry": "numerical_gradient(f, x, h=1e-5); gd_step(f, x, lr)",
"article": r'''
# Partial Derivatives and the Gradient

## Intuition
A function of several variables is a landscape. The **partial derivative** with respect to
$x_i$ is the slope if you walk only along the $x_i$ axis. Collecting all partials gives the
**gradient** — an arrow pointing in the direction of steepest ascent.

## Precise explanation
For $f: \mathbb{R}^n \to \mathbb{R}$,
$$\nabla f(x) = \left(\frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n}\right),\qquad
\frac{\partial f}{\partial x_i} \approx \frac{f(x + h e_i) - f(x - h e_i)}{2h},$$
where $e_i$ is the unit vector along axis $i$ (perturb one coordinate, keep the others fixed).
This needs $2n$ function evaluations.

Gradient descent in $n$ dimensions: $x \leftarrow x - \eta \nabla f(x)$.

## Worked example
$f(x, y) = x^2 + 3xy$. Exact: $\partial f/\partial x = 2x + 3y$, $\partial f/\partial y = 3x$.
At $(1, 2)$: $\nabla f = (8, 3)$.

## Common mistakes
* Perturbing the original list in place and forgetting to restore it — later partials are wrong.
* Perturbing all coordinates at once (that gives a directional derivative along (1,…,1)).
* Returning a tuple of tuples instead of a flat list of partials.

## Why this matters
Numerical gradients are how you *check* backpropagation ([[gradient-check]]). Understanding "one coordinate at
a time" also explains why numerical gradients are too slow to train networks with millions of
parameters, motivating automatic differentiation.
''',
"statement": r'''
Implement:
* `numerical_gradient(f, x, h=1e-5)` — `f` takes a list of floats and returns a float; `x` is a
  list. Return a list of central-difference partial derivatives. Do **not** modify `x`.
* `gd_step(f, x, lr)` — return a new list `x - lr * grad`.

Raise `ValueError` if `h <= 0`.

**Examples**
```python
f = lambda v: v[0]**2 + 3*v[0]*v[1]
numerical_gradient(f, [1.0, 2.0])     # ≈ [8.0, 3.0]
gd_step(lambda v: v[0]**2 + v[1]**2, [1.0, -2.0], 0.25)   # ≈ [0.5, -1.0]
```
''',
"starter": r'''
def numerical_gradient(f, x, h=1e-5):
    """Central-difference gradient of f at x (list). Do not modify x."""
    # TODO
    return []


def gd_step(f, x, lr):
    """One gradient-descent step using the numerical gradient."""
    # TODO
    return x
''',
"hints": [
    "For each i, copy x: `xp = list(x); xp[i] += h` and similarly `xm`.",
    "Partial i is `(f(xp) - f(xm)) / (2 * h)`.",
    "`gd_step`: `[xi - lr * gi for xi, gi in zip(x, grad)]`.",
],
"solution": r'''
def numerical_gradient(f, x, h=1e-5):
    if h <= 0:
        raise ValueError("h must be positive")
    grad = []
    for i in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        grad.append((f(xp) - f(xm)) / (2 * h))
    return grad


def gd_step(f, x, lr):
    g = numerical_gradient(f, x)
    return [xi - lr * gi for xi, gi in zip(x, g)]
''',
"explanation": r'''
Each partial derivative perturbs a fresh copy of x along one axis in both directions, so x itself
is never changed. `gd_step` combines the gradient with the descent update element-wise.
''',
"tests": r'''
class TestNumGrad(unittest.TestCase):
    def assertListAlmost(self, a, b, delta):
        self.assertEqual(len(a), len(b))
        for p, q in zip(a, b):
            self.assertAlmostEqual(p, q, delta=delta)

    def test_example(self):
        f = lambda v: v[0] ** 2 + 3 * v[0] * v[1]
        self.assertListAlmost(S.numerical_gradient(f, [1.0, 2.0]), [8.0, 3.0], 1e-6)

    def test_not_modified(self):
        x = [1.0, 2.0, 3.0]
        S.numerical_gradient(lambda v: sum(t * t for t in v), x)
        self.assertEqual(x, [1.0, 2.0, 3.0])

    def test_sum_of_squares(self):
        x = [0.5, -1.5, 2.0]
        self.assertListAlmost(S.numerical_gradient(lambda v: sum(t * t for t in v), x),
                              [1.0, -3.0, 4.0], 1e-6)

    def test_single_variable(self):
        self.assertListAlmost(S.numerical_gradient(lambda v: math.sin(v[0]), [0.3]),
                              [math.cos(0.3)], 1e-8)

    def test_gd_step(self):
        self.assertListAlmost(S.gd_step(lambda v: v[0] ** 2 + v[1] ** 2, [1.0, -2.0], 0.25),
                              [0.5, -1.0], 1e-6)

    def test_gd_converges(self):
        f = lambda v: (v[0] - 1) ** 2 + 2 * (v[1] + 0.5) ** 2
        x = [0.0, 0.0]
        for _ in range(200):
            x = S.gd_step(f, x, 0.1)
        self.assertListAlmost(x, [1.0, -0.5], 1e-4)

    def test_bad_h(self):
        with self.assertRaises(ValueError):
            S.numerical_gradient(lambda v: v[0], [1.0], h=0)
''',
"feedback": [
    ("test_not_modified", "Copy x before perturbing each coordinate."),
    ("test_example", "Perturb only coordinate i; keep the others at their original values."),
    ("test_gd_step", "Subtract lr times each gradient component."),
    ("test_gd_converges", "gd_step must return a new list using the gradient at the current point."),
],
},
# ---------------------------------------------------------------- taylor-exp
{
"slug": "taylor-exp", "title": "Taylor Series for exp(x)",
"difficulty": "advanced", "prereqs": ["derivative-rules", "binomial-coefficient"], "packages": [],
"objectives": ["Evaluate a truncated Taylor series", "Compute terms recursively to avoid factorials",
               "Stop based on a tolerance"],
"tags": ["series", "approximation", "taylor", "convergence"],
"sources": ["S009"], "entry": "exp_taylor(x, n_terms); terms_needed(x, tol)",
"article": r'''
# Approximating Functions with Taylor Series

## Intuition
Near a point, smooth functions look like polynomials. A Taylor series builds that polynomial
term by term; adding more terms extends the region where it matches.

## Precise explanation
The Taylor series of $e^x$ around 0:
$$e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!} = 1 + x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots$$
Truncating after $n$ terms gives an approximation. Compute terms **recursively** rather than
with powers and factorials:
$$t_0 = 1,\qquad t_k = t_{k-1}\cdot\frac{x}{k}.$$
This avoids overflow in $k!$ and is cheaper.

**Stopping rule:** keep adding terms until the next term's magnitude is below a tolerance.

For large negative $x$, alternating terms cancel badly (loss of precision). A standard fix is
$e^{x} = 1/e^{-x}$ for $x<0$ — you can try it as an extension.

## Worked example
$e^1$ with 5 terms: $1 + 1 + 0.5 + 0.1\overline{6} + 0.041\overline{6} = 2.708\overline{3}$;
true value 2.71828…

## Common mistakes
* Starting the sum at $k=1$ and missing the constant term 1.
* Off-by-one in "number of terms" (5 terms means $k = 0..4$).
* Using `math.factorial` and `x**k` for large k → `OverflowError` or slow code.

## Why this matters
Linear (first-order) Taylor approximations justify gradient descent, and second-order ones
justify Newton's method. Softmax and sigmoid are built on $e^x$.
''',
"statement": r'''
Implement:
* `exp_taylor(x, n_terms)` — sum of the first `n_terms` terms ($k = 0..n_\text{terms}-1$).
  `n_terms = 0` returns `0.0`. Raise `ValueError` if `n_terms < 0`.
* `terms_needed(x, tol)` — the smallest `n` such that the magnitude of term $t_n$ (the first
  term *not* included) is `< tol`. Raise `ValueError` if `tol <= 0`.

Compute terms recursively (`t = t * x / k`), not with `math.factorial`.

**Examples**
```python
exp_taylor(1.0, 5)     # 2.708333333...
exp_taylor(0.0, 3)     # 1.0
terms_needed(1.0, 1e-3)  # 7   — t_7 = 1/5040 ≈ 1.98e-4 is the first term below 1e-3
```
''',
"starter": r'''
def exp_taylor(x, n_terms):
    """Sum of the first n_terms terms of the Taylor series of exp at 0."""
    # TODO
    pass


def terms_needed(x, tol):
    """Smallest n such that |x**n / n!| < tol."""
    # TODO
    pass
''',
"hints": [
    "Start `term = 1.0`, `total = 0.0`; for k in range(n_terms): add term, then update.",
    "Update rule: `term *= x / (k + 1)`.",
    "For terms_needed: start n = 0, t = 1.0, and loop while `abs(t) >= tol`: n += 1; t *= x / n.",
],
"solution": r'''
def exp_taylor(x, n_terms):
    if n_terms < 0:
        raise ValueError("n_terms must be >= 0")
    total = 0.0
    term = 1.0
    for k in range(n_terms):
        total += term
        term *= x / (k + 1)
    return total


def terms_needed(x, tol):
    if tol <= 0:
        raise ValueError("tol must be positive")
    n = 0
    t = 1.0
    while abs(t) >= tol:
        n += 1
        t *= x / n
    return n
''',
"explanation": r'''
Both functions keep the current term and multiply it by x/k to get the next one, which is exact
algebra and avoids huge factorials. `terms_needed` advances until the first omitted term is below
the tolerance and reports how many terms were included.
''',
"tests": r'''
class TestTaylor(unittest.TestCase):
    def test_five_terms(self):
        self.assertAlmostEqual(S.exp_taylor(1.0, 5), 2.708333333333333, places=12)

    def test_zero_terms(self):
        self.assertEqual(S.exp_taylor(2.0, 0), 0.0)

    def test_x_zero(self):
        self.assertEqual(S.exp_taylor(0.0, 3), 1.0)

    def test_converges(self):
        for x in (-1.5, 0.3, 2.0, 5.0):
            self.assertAlmostEqual(S.exp_taylor(x, 60), math.exp(x), delta=1e-9 * max(1, math.exp(x)))

    def test_terms_needed(self):
        self.assertEqual(S.terms_needed(1.0, 1e-3), 7)

    def test_terms_needed_zero_x(self):
        self.assertEqual(S.terms_needed(0.0, 0.5), 1)

    def test_terms_needed_consistent(self):
        n = S.terms_needed(2.0, 1e-10)
        self.assertLess(abs(S.exp_taylor(2.0, n) - math.exp(2.0)), 1e-8)

    def test_bad_args(self):
        with self.assertRaises(ValueError):
            S.exp_taylor(1.0, -1)
        with self.assertRaises(ValueError):
            S.terms_needed(1.0, 0)

    def test_large_terms_no_overflow(self):
        self.assertAlmostEqual(S.exp_taylor(1.0, 500), math.e, places=12)
''',
"feedback": [
    ("test_five_terms", "Five terms means k = 0..4, starting with the constant 1."),
    ("test_terms_needed", "n counts included terms; stop when the next term t_n is below tol."),
    ("test_large_terms_no_overflow", "Build terms recursively; math.factorial(500) * float overflows."),
    ("test_x_zero", "With x = 0 only the first term (1) is non-zero."),
],
},
# ---------------------------------------------------------------- power-iteration
{
"slug": "power-iteration", "title": "Dominant Eigenvalue by Power Iteration",
"difficulty": "advanced", "prereqs": ["vector-norm-unit", "matrix-multiply"], "packages": [],
"objectives": ["Explain eigenvalues and eigenvectors", "Implement power iteration with normalisation",
               "Use the Rayleigh quotient and a convergence test"],
"tags": ["eigenvalues", "linear-algebra", "iterative-methods", "pca"],
"sources": ["S009"], "entry": "power_iteration(A, num_iters=1000, tol=1e-10)",
"article": r'''
# Eigenvalues by Power Iteration

## Intuition
Most vectors change direction when multiplied by a matrix. **Eigenvectors** don't — they are only
stretched: $Av = \lambda v$. If you multiply a random vector by $A$ again and again, the
component along the eigenvector with the largest $|\lambda|$ grows fastest and eventually
dominates. That is **power iteration**.

## Precise explanation
Algorithm:
1. Start with $b_0$ (here: all ones).
2. Repeat $b_{k+1} = \dfrac{A b_k}{\lVert A b_k\rVert_2}$ (normalise to avoid overflow).
3. Estimate the eigenvalue with the **Rayleigh quotient** $\lambda_k = b_k^\top A b_k$
   (for unit $b_k$).
4. Stop when $|\lambda_{k+1} - \lambda_k| < \text{tol}$.

Convergence speed depends on $|\lambda_2/\lambda_1|$: the closer to 1, the slower.
Eigenvectors are only defined up to sign; fix a convention (here: make the entry with largest
absolute value positive) so results are reproducible.

## Worked example
$A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$ has eigenvalues 3 and 1 with eigenvectors
$(1,1)/\sqrt2$ and $(1,-1)/\sqrt2$. Starting from (1, 1) you are already on the dominant
eigenvector: $A(1,1) = (3,3)$, normalised $(0.707, 0.707)$, Rayleigh quotient 3.

## Common mistakes
* Not normalising → numbers overflow to `inf`.
* Starting with a vector orthogonal to the dominant eigenvector (e.g. (1,−1) above) — it never
  appears. (Real implementations start randomly.)
* Comparing eigenvectors without fixing the sign.
* Expecting the eigenvector to be as accurate as the eigenvalue. For symmetric matrices the
  Rayleigh quotient error is roughly the *square* of the vector error, so stopping on the
  eigenvalue leaves the vector accurate only to about $\sqrt{\text{tol}}$.

## Why this matters
Principal Component Analysis finds the dominant eigenvectors of a covariance matrix; Google's
PageRank is power iteration on a link matrix; the spectral radius governs whether gradient
descent and RNNs explode.
''',
"statement": r'''
Write `power_iteration(A, num_iters=1000, tol=1e-10)` for a square matrix `A` (list of rows) in
pure Python.

* Start from the all-ones vector.
* Each iteration: `w = A b`; if `‖w‖ == 0` raise `ValueError`; `b = w / ‖w‖`;
  `lam = b · (A b)`. Stop when `|lam - previous_lam| < tol`.
* Sign convention: flip `b` so its entry with largest absolute value is positive.
* Return `(lam, b)` with `b` a list of floats of unit length. Tests check `lam` to 1e-8 and
  `b` to 1e-4 (the vector converges more slowly than the eigenvalue).
* Raise `ValueError` if `A` is not square.

**Examples**
```python
power_iteration([[2, 1], [1, 2]])   # (3.0, [0.7071..., 0.7071...])
power_iteration([[4, 0], [0, -1]])  # (4.0, [1.0, 0.0])
```
''',
"starter": r'''
import math


def power_iteration(A, num_iters=1000, tol=1e-10):
    """Return (dominant eigenvalue, unit eigenvector) of square matrix A."""
    # TODO
    pass
''',
"hints": [
    "Write helpers `matvec(A, v)` and `dot(u, v)`.",
    "Normalise: `nrm = math.sqrt(dot(w, w)); b = [x / nrm for x in w]`.",
    "Track `prev` and compare `abs(lam - prev) < tol`; fix the sign at the end.",
],
"solution": r'''
import math


def _matvec(A, v):
    return [sum(a * x for a, x in zip(row, v)) for row in A]


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def power_iteration(A, num_iters=1000, tol=1e-10):
    n = len(A)
    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("A must be a non-empty square matrix")
    b = [1.0] * n
    lam = None
    for _ in range(num_iters):
        w = _matvec(A, b)
        nrm = math.sqrt(_dot(w, w))
        if nrm == 0:
            raise ValueError("A b is the zero vector; choose another start")
        b = [x / nrm for x in w]
        new_lam = _dot(b, _matvec(A, b))
        if lam is not None and abs(new_lam - lam) < tol:
            lam = new_lam
            break
        lam = new_lam
    k = max(range(n), key=lambda i: abs(b[i]))
    if b[k] < 0:
        b = [-x for x in b]
    return lam, b
''',
"explanation": r'''
Repeated multiplication amplifies the dominant eigen-direction; normalising each step keeps the
numbers bounded. The Rayleigh quotient of the unit vector estimates the eigenvalue and provides
the stopping test. Finally the sign is fixed (largest-magnitude entry positive) so the
eigenvector is reported reproducibly.
''',
"tests": r'''
class TestPower(unittest.TestCase):
    def test_symmetric(self):
        lam, v = S.power_iteration([[2, 1], [1, 2]])
        self.assertAlmostEqual(lam, 3.0, places=8)
        self.assertAlmostEqual(v[0], 1 / math.sqrt(2), places=6)
        self.assertAlmostEqual(v[1], 1 / math.sqrt(2), places=6)

    def test_diagonal_negative(self):
        lam, v = S.power_iteration([[4, 0], [0, -1]])
        self.assertAlmostEqual(lam, 4.0, places=8)
        # eigenvectors converge more slowly than the Rayleigh quotient (~sqrt(tol))
        self.assertAlmostEqual(v[0], 1.0, delta=1e-4)
        self.assertAlmostEqual(v[1], 0.0, delta=1e-4)

    def test_eigen_equation(self):
        A = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
        lam, v = S.power_iteration(A)
        Av = [sum(a * x for a, x in zip(r, v)) for r in A]
        for i in range(3):
            self.assertAlmostEqual(Av[i], lam * v[i], places=5)

    def test_unit_length(self):
        _, v = S.power_iteration([[5, 2], [2, 1]])
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in v)), 1.0, places=10)

    def test_sign_convention(self):
        _, v = S.power_iteration([[-3, 0], [0, 1]])
        self.assertGreater(max(v, key=abs), 0)

    def test_not_square(self):
        with self.assertRaises(ValueError):
            S.power_iteration([[1, 2, 3], [4, 5, 6]])

    def test_zero_matrix(self):
        with self.assertRaises(ValueError):
            S.power_iteration([[0, 0], [0, 0]])

    def test_1x1(self):
        lam, v = S.power_iteration([[7]])
        self.assertAlmostEqual(lam, 7.0)
        self.assertEqual(v, [1.0])
''',
"feedback": [
    ("test_eigen_equation", "Check A·v ≈ λ·v; normalise b every iteration and use the Rayleigh quotient."),
    ("test_sign_convention", "Flip b so its largest-magnitude entry is positive."),
    ("test_zero_matrix", "Raise ValueError when A·b has zero norm."),
    ("test_diagonal_negative", "λ is the dominant eigenvalue by absolute value; here it is 4."),
],
},
]
