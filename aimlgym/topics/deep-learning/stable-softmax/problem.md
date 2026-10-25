# DL-02 · Numerically Stable Softmax

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** DL-01 Activation Functions, MA-02 Exponentials and Logarithms

Read the lesson first: [article.md](article.md)

## Task

Implement `softmax(z, axis=-1)` and `log_softmax(z, axis=-1)` for arrays of any shape, stable
for logits as large as 1e4 in magnitude (no overflow warnings, no NaN).

**Examples**
```python
softmax(np.array([1., 2., 3.]))          # [0.09003057, 0.24472847, 0.66524096]
softmax(np.array([1000., 1001.]))        # [0.26894142, 0.73105858]
log_softmax(np.array([0., -1e4]))        # [0., -10000.]
```

## Hints

<details><summary>Hint 1</summary>

`m = z.max(axis=axis, keepdims=True)`; work with `z - m`.

</details>

<details><summary>Hint 2</summary>

`e = np.exp(z - m); e / e.sum(axis=axis, keepdims=True)`.

</details>

<details><summary>Hint 3</summary>

`(z - m) - np.log(np.exp(z - m).sum(axis=axis, keepdims=True))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_large` | Subtract the max before exponentiating. |
| `test_axis0` | Use keepdims=True with the given axis for max and sum. |
| `test_log_softmax` | Don't compute log(softmax(z)); use shifted logits minus log-sum-exp. |
| `test_rows` | Each row must sum to 1 when axis=-1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Subtracting the maximum along the chosen axis keeps every exponent ≤ 0, so `exp` cannot overflow
and the denominator is at least 1. Log-softmax uses the same shift and the log-sum-exp identity
to avoid `log(0)`.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
