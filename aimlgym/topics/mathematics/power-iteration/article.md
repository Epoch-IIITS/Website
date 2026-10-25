# Eigenvalues by Power Iteration

## Learning outcomes

After this lesson you can:

- Explain eigenvalues and eigenvectors
- Implement power iteration with normalisation
- Use the Rayleigh quotient and a convergence test

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

## Library implementation

`numpy.linalg.eigh` (symmetric matrices) or `numpy.linalg.eig` compute *all* eigenvalues with
LAPACK; power iteration finds only the dominant one but needs nothing beyond matrix–vector
products, which is why it scales to huge sparse matrices (it is the idea behind PageRank). The
test compares your result with `eigh` on a symmetric matrix.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
