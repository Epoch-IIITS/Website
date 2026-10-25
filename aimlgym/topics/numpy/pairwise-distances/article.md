# Pairwise Distances without Loops

## Learning outcomes

After this lesson you can:

- Compute all pairwise squared distances with broadcasting
- Use the expansion ‖a−b‖² = ‖a‖² + ‖b‖² − 2a·b
- Find nearest neighbours with argmin

## Intuition
k-NN, k-means and retrieval all need the distance from every query to every reference point. A
double Python loop over 1000 × 1000 points is a million slow iterations; one matrix expression
does it in milliseconds.

## Precise explanation
For rows $a_i$ of $A$ ($m\times d$) and $b_j$ of $B$ ($n\times d$):
$$D_{ij} = \lVert a_i - b_j\rVert^2 = \lVert a_i\rVert^2 + \lVert b_j\rVert^2 - 2\,a_i\cdot b_j.$$
In NumPy:
```python
aa = (A**2).sum(axis=1)[:, None]    # (m, 1)
bb = (B**2).sum(axis=1)[None, :]    # (1, n)
D = aa + bb - 2 * A @ B.T           # (m, n)
```
Rounding can make tiny entries slightly negative (e.g. −1e−15); clip with `np.maximum(D, 0)`.
An alternative, `((A[:, None, :] - B[None, :, :])**2).sum(-1)`, is simpler but builds an
`(m, n, d)` temporary that uses much more memory.

## Worked example
A = [[0, 0], [1, 1]], B = [[1, 0], [3, 4]]:
D = [[1, 25], [1, 13]]; nearest B-row for each A-row: [0, 0].

## Common mistakes
* Forgetting the transpose in `A @ B.T`.
* Taking `sqrt` of slightly negative values → NaN.
* Mixing up which axis to `argmin` over (axis=1 → nearest B for each A).

## Why this matters
This exact function is the engine of k-NN (ML-13), k-means (ML-26), embedding retrieval (NL-11)
and non-max suppression ideas in CV.

## Library implementation

The expansion $\lVert a-b\rVert^2 = \lVert a\rVert^2 + \lVert b\rVert^2 - 2a\cdot b$ is what fast
libraries use. SciPy exposes it as `scipy.spatial.distance.cdist(A, B, "sqeuclidean")` and
scikit-learn as `sklearn.metrics.pairwise.euclidean_distances(A, B, squared=True)`. The tests
compare with a plain double loop and, when installed, with SciPy.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
