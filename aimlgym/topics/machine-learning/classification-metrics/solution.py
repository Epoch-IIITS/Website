r"""Reference solution for ML-06 Confusion Matrix, Precision, Recall, F1.

`np.add.at` increments one cell per (true, predicted) pair, even with repeated pairs. Column sums
are predicted counts, row sums true counts, the diagonal true positives. A guarded division sets
undefined ratios to zero.
"""
import numpy as np


def confusion_matrix(y_true, y_pred, n_classes):
    yt = np.asarray(y_true, dtype=int)
    yp = np.asarray(y_pred, dtype=int)
    if yt.shape != yp.shape:
        raise ValueError("length mismatch")
    if yt.size and (min(yt.min(), yp.min()) < 0 or max(yt.max(), yp.max()) >= n_classes):
        raise ValueError("label out of range")
    C = np.zeros((n_classes, n_classes), dtype=int)
    np.add.at(C, (yt, yp), 1)
    return C


def _safe_div(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.divide(a, b, out=np.zeros_like(a), where=b > 0)


def classification_report(y_true, y_pred, n_classes):
    C = confusion_matrix(y_true, y_pred, n_classes)
    tp = np.diag(C)
    precision = _safe_div(tp, C.sum(axis=0))
    recall = _safe_div(tp, C.sum(axis=1))
    f1 = _safe_div(2 * precision * recall, precision + recall)
    total = C.sum()
    return {"precision": precision, "recall": recall, "f1": f1,
            "accuracy": float(tp.sum() / total) if total else 0.0,
            "macro_f1": float(f1.mean())}
