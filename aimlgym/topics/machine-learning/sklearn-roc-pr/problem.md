# ML-24 · Thresholds, ROC and Precision–Recall Curves

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-23 Gradient Boosting, ML-06 Confusion Matrix, Precision, Recall, F1

Read the lesson first: [article.md](article.md)

## Task

Write `threshold_report(y_true, scores, min_recall)` for binary labels returning
`{"roc_auc": float, "average_precision": float, "threshold": float, "precision": float, "recall": float}`.

* `threshold` is the **highest** threshold from `precision_recall_curve` whose recall is at least
  `min_recall`; `precision` and `recall` are the values at that threshold.
* Raise `ValueError` if `y_true` does not contain both classes, lengths differ, or `min_recall`
  is not in (0, 1].

**Example**
```python
threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.9)
# {'roc_auc': 0.888..., 'average_precision': 0.916..., 'threshold': 0.6, 'precision': 0.75, 'recall': 1.0}
```

## Hints

<details><summary>Hint 1</summary>

Validate: `set(y_true) == {0, 1}`, equal lengths, `0 < min_recall <= 1`.

</details>

<details><summary>Hint 2</summary>

`precision, recall, thresholds = precision_recall_curve(y_true, scores)`; only the first `len(thresholds)` points have thresholds.

</details>

<details><summary>Hint 3</summary>

Among indices i with `recall[i] >= min_recall`, take the one with the largest `thresholds[i]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Pick the highest threshold whose recall still reaches min_recall. |
| `test_auc_is_pairwise_ranking` | roc_auc_score takes scores, not thresholded labels. |
| `test_recall_target_met` | precision[i], recall[i] belong to thresholds[i]; ignore the final extra point. |
| `test_invalid` | Require both classes, equal lengths and 0 < min_recall <= 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The two summary scores rank the classifier independently of any threshold. To meet a recall
target with as few false alarms as possible, pick the highest threshold that still reaches the
target: the lowest threshold always has recall 1, so a valid choice always exists.

## References

- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
