# One-Hot Encoding

## Learning outcomes

After this lesson you can:

- Encode integer labels as one-hot rows
- Decode with argmax
- Validate label ranges

## Intuition
Class labels like 0 = cat, 1 = dog, 2 = bird are names, not quantities — "bird" is not "twice
dog". One-hot encoding turns each label into a row with a single 1 in its class column, so no
false ordering is implied.

## Precise explanation
For labels $y_i \in \{0,\dots,K-1\}$, the one-hot matrix $Y \in \{0,1\}^{n\times K}$ has
$Y_{i, y_i} = 1$ and zeros elsewhere. Vectorised construction:
```python
Y = np.zeros((n, K))
Y[np.arange(n), labels] = 1
```
(or `np.eye(K)[labels]`). Decoding: `Y.argmax(axis=1)`.

Validation: labels must be non-negative integers below K; if K is not given, use
`labels.max() + 1`.

## Worked example
labels [2, 0, 1] with K = 3 → [[0,0,1],[1,0,0],[0,1,0]].

## Common mistakes
* `Y[:, labels] = 1` — sets whole columns.
* Inferring K from a *batch* and getting different widths for different batches; pass K.
* Negative labels index from the end without error — validate.

## Why this matters
Softmax cross-entropy (DL-03) compares predictions to one-hot targets; categorical features are
one-hot encoded for linear models; tokens are one-hot before an embedding lookup.

## Library implementation

A compact NumPy idiom is `np.eye(K)[labels]`: row `i` of the identity matrix is the one-hot
vector for class `i`, and fancy indexing picks one row per label. scikit-learn's `OneHotEncoder`
and pandas' `pd.get_dummies` do the same for tables, including string categories.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
