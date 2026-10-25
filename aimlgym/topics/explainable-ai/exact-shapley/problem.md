# XA-11 · Exact Shapley Values

**Topic:** Explainable AI · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** MA-07 Binomial Coefficient, XA-01 Linear Model Contributions

Read the lesson first: [article.md](article.md)

## Task

Implement (use `itertools.combinations` and `math.factorial`):
* `coalition_value(predict, x, baseline, subset)` → float `predict` on a single input (shape `(1, d)`)
  that takes `x` on indices in `subset` and `baseline` elsewhere.
* `shapley_values(predict, x, baseline)` → array of exact Shapley values. Raise `ValueError` if
  `d > 12` (too many coalitions) or shapes differ.

**Example**
```python
f = lambda X: X[:, 0] * X[:, 1]
shapley_values(f, np.array([1., 1.]), np.zeros(2))   # [0.5, 0.5]
```

## Hints

<details><summary>Hint 1</summary>

`z = baseline.copy(); z[list(subset)] = x[list(subset)]`; `float(predict(z[None, :])[0])`.

</details>

<details><summary>Hint 2</summary>

Loop j; for size in 0..d−1 and each `S` in `combinations(others, size)`.

</details>

<details><summary>Hint 3</summary>

Weight = `math.factorial(len(S)) * math.factorial(d - len(S) - 1) / math.factorial(d)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_efficiency` | Use weights |S|!(d−|S|−1)!/d! and include the empty coalition. |
| `test_interaction_split` | Average marginal contributions over all coalitions of the other features. |
| `test_coalition_value` | Take x on coalition indices and the baseline elsewhere; call predict on shape (1, d). |
| `test_linear_matches_xa01` | For linear models Shapley values equal w·(x − baseline). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The value function mixes the instance and the baseline according to the coalition. For each feature,
every coalition of the other features is enumerated and its weighted marginal contribution added.
A cache ensures each of the 2^d coalitions is evaluated only once.

## References

- [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874) — Scott Lundberg, Su-In Lee (`S026`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
