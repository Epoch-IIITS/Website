# DL-03 · Cross-Entropy Loss

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** DL-02 Numerically Stable Softmax

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `cross_entropy(logits, labels)` → float mean loss for `logits` `(n, K)` and integer `labels`
  `(n,)`; stable for large logits.
* `cross_entropy_grad(logits, labels)` → `(n, K)` gradient of the mean loss.

Raise `ValueError` if shapes disagree or a label is outside `0..K-1`.

**Examples**
```python
cross_entropy(np.array([[2., 0., -1.]]), np.array([0]))        # 0.16984...
cross_entropy(np.array([[0., 0.], [0., 0.]]), np.array([0, 1]))# 0.693147... (= log 2)
```

## Hints

<details><summary>Hint 1</summary>

Write `_log_softmax` with max subtraction (DL-02).

</details>

<details><summary>Hint 2</summary>

Loss: `-lsm[np.arange(n), labels].mean()`.

</details>

<details><summary>Hint 3</summary>

Gradient: `P = np.exp(lsm); P[np.arange(n), labels] -= 1; P / n`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_large_logits` | Use a stable log-softmax; log(softmax) underflows. |
| `test_grad_numeric` | Gradient of the *mean* loss: divide (softmax − one_hot) by n. |
| `test_single` | Pick log-probabilities with [np.arange(n), labels]. |
| `test_bad_label` | Validate labels are in 0..K−1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A stable log-softmax gives log-probabilities directly, and paired indexing selects each row's
correct-class entry. The gradient is softmax minus one-hot, divided by the batch size because the
loss is a mean.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
