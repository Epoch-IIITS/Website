# ML-05 · Seeded Train/Test Split

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-01 Features, Labels and Baseline Models, NP-10 Seeded Random Generators

Read the lesson first: [article.md](article.md)

## Task

Write `train_test_split(X, y, test_size=0.25, seed=0, stratify=False)` returning
`(X_train, X_test, y_train, y_test)` as NumPy arrays.

* `rng = np.random.default_rng(seed)`.
* Non-stratified: `perm = rng.permutation(n)`; `n_test = round(n * test_size)` clipped to
  `[1, n-1]`; test = `perm[:n_test]`, train = `perm[n_test:]`.
* Stratified: for each class `c` in `np.unique(y)` (sorted), shuffle that class's indices with
  `rng.permutation`, put `round(n_c * test_size)` of them in test (rest in train); concatenate
  over classes in class order.
* Raise `ValueError` if `len(X) != len(y)`, `n < 2`, or `test_size` not in `(0, 1)`.

**Example**
```python
X = np.arange(20).reshape(10, 2); y = np.array([0]*8 + [1]*2)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, seed=1, stratify=True)
sorted(yte.tolist())    # [0, 0, 0, 0, 1]  — class ratio preserved
```

## Hints

<details><summary>Hint 1</summary>

Convert with `np.asarray`, validate, and create one `rng`.

</details>

<details><summary>Hint 2</summary>

Non-stratified: `perm = rng.permutation(n)`; slice into test/train index arrays.

</details>

<details><summary>Hint 3</summary>

Stratified: loop over `np.unique(y)`, permute `np.flatnonzero(y == c)` and split each.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_alignment` | Index X and y with the same permutation. |
| `test_recipe` | Use rng = default_rng(seed); perm = rng.permutation(n); test = perm[:n_test]. |
| `test_stratified` | Split each class separately with round(n_c * test_size) test samples. |
| `test_disjoint_cover` | Train and test must partition all rows. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A single permutation of row indices is used for both X and y, so pairs stay aligned. The
stratified variant applies the same idea per class, preserving class proportions. All randomness
flows through one seeded generator.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
