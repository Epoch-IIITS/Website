# Solving Two Equations in Two Unknowns

## Learning outcomes

After this lesson you can:

- Compute a 2×2 determinant
- Solve a linear system with Cramer's rule
- Detect singular systems with a tolerance

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
Linear systems are solved inside least squares (ML-09), ridge regression (ML-20) and Newton's
method. Recognising near-singular systems explains why ML adds regularisation.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
