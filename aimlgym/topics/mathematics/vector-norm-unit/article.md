# Norms: How Long is a Vector?

## Learning outcomes

After this lesson you can:

- Compute L1, L2 and L∞ norms
- Normalise a vector to unit length
- Handle the zero vector

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
(ridge regression, ML-20); gradient clipping in DL and federated learning (FL-09) rescales by the
norm.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
