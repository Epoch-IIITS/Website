# Beyond Accuracy

## Learning outcomes

After this lesson you can:

- Build a multi-class confusion matrix
- Compute per-class precision, recall and F1
- Handle zero-division and macro averaging

## Intuition
A spam filter that never flags spam is 95 % accurate if only 5 % of emails are spam — and
useless. The **confusion matrix** shows which classes are confused with which; precision and
recall summarise it per class.

## Precise explanation
Confusion matrix $C$ with rows = true class, columns = predicted class: $C_{ij}$ counts examples
of class $i$ predicted as $j$. For class $k$:
* TP $= C_{kk}$, FP = column sum − TP, FN = row sum − TP.
* Precision $= \frac{TP}{TP+FP}$ ("of those predicted k, how many were k").
* Recall $= \frac{TP}{TP+FN}$ ("of the true k, how many were found").
* $F_1 = \frac{2PR}{P+R}$ — harmonic mean, low if either is low.
* When a denominator is 0 we define the value as 0 (scikit-learn's `zero_division=0`).
* **Macro average** = unweighted mean over classes; accuracy = trace / total.

Vectorised construction: `np.add.at(C, (y_true, y_pred), 1)`.

## Worked example
y = [0, 0, 1, 1, 2], ŷ = [0, 1, 1, 1, 0]:
C = [[1,1,0],[0,2,0],[1,0,0]]; class 1: P = 2/3, R = 1, F1 = 0.8; class 2: P = R = F1 = 0.

## Common mistakes
* Transposing the matrix (rows vs columns).
* Averaging F1 incorrectly (F1 of averages ≠ average of F1s).
* Dividing by zero for classes never predicted.

## Why this matters
Imbalanced problems (fraud, disease, rare tokens) are judged by precision/recall, and per-class
reports reveal fairness issues.

## Library implementation

`sklearn.metrics.confusion_matrix(y_true, y_pred, labels=range(K))` uses the same layout (rows =
true class, columns = predicted), and `precision_recall_fscore_support(..., zero_division=0)`
returns per-class precision, recall and F1 with the same convention for empty classes.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
