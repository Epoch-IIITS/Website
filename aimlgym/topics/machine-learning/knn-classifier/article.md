# k-Nearest Neighbours

## Learning outcomes

After this lesson you can:

- Classify by majority vote of the k nearest training points
- Break distance and vote ties deterministically
- See how k trades bias and variance

## Intuition
"Tell me who your neighbours are and I'll tell you who you are." To classify a new point, find
the *k* training points closest to it and take a majority vote of their labels. There is no
training phase beyond storing the data.

## Precise explanation
For each test point $x$:
1. Compute distances to all training points (squared Euclidean distance ranks the same as
   Euclidean, NP-11).
2. Take the $k$ smallest. Distance ties are broken by lower training index (stable sort).
3. Vote: the most frequent label among the $k$ neighbours.
4. **Vote ties** (e.g. k = 4 with 2–2): choose, among the tied labels, the one whose nearest
   member among the k neighbours is closest (i.e. the first tied label in distance order).

Small k → flexible, noisy boundaries (high variance); large k → smoother boundaries (high bias);
k = n predicts the majority class everywhere. Features should be standardised (ML-08), or large-
scale features dominate distances.

**Corrected from the outline:** classifying by the nearest *class mean* is a different method
(nearest centroid); k-NN votes among actual training points.

## Worked example
Train: (0,0)→A, (1,0)→A, (5,5)→B, (6,5)→B, (5,6)→B. Query (2,1), k = 3: nearest are (1,0) A,
(0,0) A, (5,5) B → A. With k = 5: 3 B vs 2 A → B.

## Common mistakes
* Using `np.argsort` without a stable kind and getting inconsistent tie handling.
* Forgetting to scale features.
* Including the query point itself when evaluating on training data.

## Why this matters
k-NN is a strong baseline, the idea behind retrieval-augmented generation (nearest documents)
and example-based explanations in XAI.

## Library implementation

`sklearn.neighbors.KNeighborsClassifier(n_neighbors=k)` gives the same predictions when there are
no ties; for tied votes it picks the smallest label, whereas this exercise picks the label of the
nearest tied neighbour. It also uses tree structures to find neighbours quickly in large data.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
