# ML-04 · Splitting Data with scikit-learn

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-02 The scikit-learn Estimator API

Read the lesson first: [article.md](article.md)

## Task

Write two functions.

1. `split_data(X, y, test_size=0.25, seed=0, stratify=False)` returns
   `(X_train, X_test, y_train, y_test)` using `train_test_split` with `random_state=seed`, and
   `stratify=y` when `stratify` is true.
2. `stratified_splits(X, y, n_splits=3, test_size=0.25, seed=0)` returns a list of
   `(train_index, test_index)` pairs (as Python lists of ints) from `StratifiedShuffleSplit`.

Raise `ValueError` in both if `X` and `y` have different lengths.

**Example**
```python
X = np.arange(20).reshape(10, 2); y = np.array([0] * 8 + [1] * 2)
Xtr, Xte, ytr, yte = split_data(X, y, test_size=0.5, seed=1, stratify=True)
sorted(yte.tolist())     # [0, 0, 0, 0, 1]
```

## Hints

<details><summary>Hint 1</summary>

Pass both arrays to one `train_test_split` call so they are shuffled together.

</details>

<details><summary>Hint 2</summary>

`stratify=y if stratify else None`, `random_state=seed`.

</details>

<details><summary>Hint 3</summary>

`for train, test in StratifiedShuffleSplit(n_splits=..., test_size=..., random_state=seed).split(X, y)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_stratified_ratio` | Pass stratify=y when stratify is true. |
| `test_rows_stay_paired` | Split X and y in a single train_test_split call. |
| `test_reproducible` | Use random_state=seed. |
| `test_stratified_splits` | Convert StratifiedShuffleSplit's index arrays to lists of ints. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One `train_test_split` call shuffles all arrays with the same permutation, so features and labels
stay aligned; `stratify` makes the split per class. `StratifiedShuffleSplit` yields index arrays,
which are converted to lists of plain ints.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
