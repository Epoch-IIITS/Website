# Splitting Data with scikit-learn

## Learning outcomes

After this lesson you can:

- Split arrays with train_test_split, keeping rows paired
- Preserve class proportions with stratify
- Generate repeated stratified splits with StratifiedShuffleSplit

## Intuition
A model has to be judged on rows it never saw. scikit-learn's splitters shuffle once, keep each
row's features and label together, and can keep rare classes represented in both halves.

## Precise explanation
```python
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)
```

* Every array you pass is split with the **same** shuffled indices, so rows stay paired.
* `random_state` fixes the shuffle: the same number gives the same split every run.
* `stratify=y` splits each class separately so the class ratio is (nearly) the same in train and
  test. Use it for classification, especially with imbalanced classes.
* `StratifiedShuffleSplit(n_splits, test_size, random_state).split(X, y)` yields several
  independent stratified `(train_index, test_index)` pairs — useful for repeated evaluation.

## Worked example
With 8 negatives and 2 positives and `test_size=0.5, stratify=y`, the test set gets 4 negatives
and 1 positive. Without stratification a 5-row test set may contain no positives at all, and
accuracy on it says nothing about the rare class.

## What the library does inside
`train_test_split` draws one permutation of the row indices and slices it — exactly the
procedure in ML-05, the optional deep dive after this step. The stratified version
does that per class and merges the results.

## Common mistakes
* Calling it twice (once for X, once for y): the shuffles differ and the pairs break.
* Forgetting `random_state`, so the reported score changes on every run.
* Tuning on the test set; keep it for the final check and tune with cross-validation instead.

## Why this matters
Every evaluation in the rest of the course starts from an honest split; the capstone of this topic
uses a stratified split before any preprocessing.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
