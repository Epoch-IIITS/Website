r"""Reference solution for NL-16 Evaluating Text Classifiers.

The confusion matrix and the report come straight from `sklearn.metrics` with a fixed label order,
so rows, columns and per-class entries line up. Collecting the misclassified texts beside their true
and predicted labels gives the material for error analysis.
"""
from sklearn.metrics import classification_report, confusion_matrix


def error_report(texts, y_true, y_pred, labels):
    if not len(texts) == len(y_true) == len(y_pred):
        raise ValueError("texts, y_true and y_pred must have the same length")
    report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
    per_class = {}
    for label in labels:
        row = report[str(label)]
        per_class[label] = {"precision": float(row["precision"]), "recall": float(row["recall"]),
                            "f1": float(row["f1-score"]), "support": int(row["support"])}
    return {"confusion": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
            "per_class": per_class, "macro_f1": float(report["macro avg"]["f1-score"]),
            "errors": [(t, a, b) for t, a, b in zip(texts, y_true, y_pred) if a != b]}
