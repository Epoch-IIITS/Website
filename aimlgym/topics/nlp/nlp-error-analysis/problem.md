# NL-16 · Evaluating Text Classifiers

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** NL-15 A Text Classification Pipeline

Read the lesson first: [article.md](article.md)

## Task

Write `error_report(texts, y_true, y_pred, labels)` returning

* `"confusion"`: `confusion_matrix(y_true, y_pred, labels=labels)` as a list of int lists;
* `"per_class"`: `{label: {"precision": float, "recall": float, "f1": float, "support": int}}` from
  `classification_report(..., labels=labels, output_dict=True, zero_division=0)`;
* `"macro_f1"`: the report's `"macro avg"` F1 as a float;
* `"errors"`: `(text, true_label, predicted_label)` tuples for every misclassified example, in input order.

Raise `ValueError` if the three sequences differ in length.

## Hints

<details><summary>Hint 1</summary>

Check that the three lengths match.

</details>

<details><summary>Hint 2</summary>

`report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)`; per-class entries are keyed by `str(label)`.

</details>

<details><summary>Hint 3</summary>

Errors: `[(t, a, b) for t, a, b in zip(texts, y_true, y_pred) if a != b]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_worked_example` | Rows of the confusion matrix are true labels, columns predicted, in the given label order. |
| `test_per_class_matches_metrics` | Read precision, recall, f1-score and support from classification_report(output_dict=True). |
| `test_errors_in_order` | Keep (text, true, predicted) for mismatches in input order. |
| `test_invalid` | All three sequences must have the same length. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The confusion matrix and the report come straight from `sklearn.metrics` with a fixed label order,
so rows, columns and per-class entries line up. Collecting the misclassified texts beside their true
and predicted labels gives the material for error analysis.

## References

- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
