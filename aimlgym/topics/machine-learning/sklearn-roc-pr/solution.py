r"""Reference solution for ML-24 Thresholds, ROC and Precision–Recall Curves.

The two summary scores rank the classifier independently of any threshold. To meet a recall
target with as few false alarms as possible, pick the highest threshold that still reaches the
target: the lowest threshold always has recall 1, so a valid choice always exists.
"""
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score


def threshold_report(y_true, scores, min_recall):
    if len(y_true) != len(scores) or set(y_true) != {0, 1}:
        raise ValueError("need matching lengths and both classes")
    if not 0 < min_recall <= 1:
        raise ValueError("min_recall must be in (0, 1]")
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    ok = [i for i in range(len(thresholds)) if recall[i] >= min_recall]
    best = max(ok, key=lambda i: thresholds[i])
    return {"roc_auc": float(roc_auc_score(y_true, scores)),
            "average_precision": float(average_precision_score(y_true, scores)),
            "threshold": float(thresholds[best]), "precision": float(precision[best]),
            "recall": float(recall[best])}
