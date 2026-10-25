# Solving Linear Systems in NumPy

## Learning outcomes

After this lesson you can:

- Solve Ax=b with np.linalg.solve
- Detect ill-conditioned systems with np.linalg.cond
- Fit least squares with np.linalg.lstsq

## Intuition
MA-08 solved 2×2 systems by hand. Real problems have hundreds of unknowns, and some systems are
*nearly* singular: tiny changes in the data cause huge changes in the answer. The **condition
number** measures that sensitivity.

## Precise explanation
* `np.linalg.solve(A, b)` solves square systems using an LU factorisation (more accurate and
  faster than `inv(A) @ b`). It raises `LinAlgError` for exactly singular matrices.
* `np.linalg.cond(A)` — ratio of largest to smallest singular value. Rule of thumb: you can lose
  about $\log_{10}(\text{cond})$ digits of accuracy; above ~1e12 in float64, answers are mostly
  noise.
* Residual $\lVert Ax - b\rVert_2$ (`np.linalg.norm(A @ x - b)`) checks a solution.
* Over-determined systems (more equations than unknowns) have no exact solution; least squares
  minimises the residual: `np.linalg.lstsq(X, y, rcond=None)`.

To fit $y \approx w_0 + w_1 x$, build $X = [\mathbf 1, x]$ and solve the least-squares problem.

## Worked example
A = [[3, 1], [1, 2]], b = [9, 8] → x = [2, 3]; residual 0.
Points (0, 1), (1, 3), (2, 5) → line intercept 1, slope 2.

## Common mistakes
* Using `np.linalg.inv` for solving.
* Ignoring warnings about near-singular matrices.
* Forgetting the column of ones (forcing the line through the origin).

## Why this matters
Least squares is linear regression (ML-09), ridge adds a stabilising term to fix
ill-conditioning (ML-20), and many ML solvers report condition problems as convergence warnings.

## Library implementation

`np.linalg.solve` is the library version of MA-08 for any size (it uses an LU
factorisation, not Cramer's rule, which would be far slower and less stable). For fitting lines,
`np.polyfit(x, y, 1)` returns `[slope, intercept]` — the reverse order of `fit_line`. The tests
compare against Cramer's rule for a 2×2 system and `np.polyfit`.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
