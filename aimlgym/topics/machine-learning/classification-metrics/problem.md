# ML-06 · Confusion Matrix, Precision, Recall, F1

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-01 Features, Labels and Baseline Models

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `confusion_matrix(y_true, y_pred, n_classes)` → int array `(n_classes, n_classes)`, rows =
  true labels. Raise `ValueError` for mismatched lengths or labels outside `0..n_classes-1`.
* `classification_report(y_true, y_pred, n_classes)` → dict with `"precision"`, `"recall"`,
  `"f1"` (float arrays of length n_classes, zero where undefined), `"accuracy"` and `"macro_f1"`
  (floats).

**Example**
```python
confusion_matrix([0, 0, 1, 1, 2], [0, 1, 1, 1, 0], 3)   # [[1,1,0],[0,2,0],[1,0,0]]
classification_report([0, 0, 1, 1, 2], [0, 1, 1, 1, 0], 3)["f1"]   # [0.5, 0.8, 0.0]
```

## Hints

<details><summary>Hint 1</summary>

`C = np.zeros((K, K), dtype=int); np.add.at(C, (yt, yp), 1)`.

</details>

<details><summary>Hint 2</summary>

TP = `np.diag(C)`, predicted totals = `C.sum(axis=0)`, true totals = `C.sum(axis=1)`.

</details>

<details><summary>Hint 3</summary>

Safe division: `np.divide(a, b, out=np.zeros_like(a, dtype=float), where=b > 0)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_cm` | Rows are true labels, columns predicted labels. |
| `test_precision_recall` | Precision divides by column sums, recall by row sums. |
| `test_unused_class` | Use 0 when a denominator is 0 instead of NaN. |
| `test_cm_total` | Use np.add.at so repeated (true, pred) pairs all count. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`np.add.at` increments one cell per (true, predicted) pair, even with repeated pairs. Column sums
are predicted counts, row sums true counts, the diagonal true positives. A guarded division sets
undefined ratios to zero.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
