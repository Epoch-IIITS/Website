# The Inverse of a 2×2 Matrix

## Learning outcomes

After this lesson you can:

- Compute the inverse via the adjugate formula
- Verify A·A⁻¹ = I numerically
- Explain when a matrix has no inverse

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

Numerically, solving $Ax=b$ directly (MA-08) is usually preferred over forming $A^{-1}$, but the
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

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
