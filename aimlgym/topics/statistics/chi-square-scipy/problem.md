# ST-15 · Chi-Square Test with SciPy

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** numpy, scipy

**Builds on:** ST-14 Introducing scipy.stats

Read the lesson first: [article.md](article.md)

## Task

Write `chi_square_test(observed, probs, alpha=0.05)` returning
`{"statistic": float, "p_value": float, "df": int, "reject": bool}` where `reject` is
`p_value < alpha`.

* Expected counts are the total of `observed` times each probability.
* Raise `ValueError` if lengths differ, there are fewer than 2 categories, any probability is
  ≤ 0, probabilities do not sum to 1 within 1e-9, any count is negative, the total is 0, or
  `alpha` is not strictly between 0 and 1.

Use `scipy.stats.chisquare`.

**Examples**
```python
chi_square_test([5, 8, 9, 8, 10, 20], [1/6] * 6)
# {'statistic': 13.4, 'p_value': 0.0199..., 'df': 5, 'reject': True}
chi_square_test([5, 8, 9, 8, 10, 20], [1/6] * 6, alpha=0.01)["reject"]   # False
```

## Hints

<details><summary>Hint 1</summary>

Validate the inputs as in the hand-written test, plus `0 < alpha < 1`.

</details>

<details><summary>Hint 2</summary>

`expected = [total * p for p in probs]`; then `result = stats.chisquare(observed, f_exp=expected)`.

</details>

<details><summary>Hint 3</summary>

Return `float(result.statistic)`, `float(result.pvalue)`, `len(observed) - 1` and the comparison with alpha.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_die` | Pass expected counts (total × p), not probabilities, as f_exp. |
| `test_stricter_alpha` | reject is p_value < alpha. |
| `test_plain_types` | Convert NumPy results with float(...); the comparison gives a bool. |
| `test_invalid_inputs` | Validate before calling SciPy, including alpha. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

SciPy needs expected counts, so the probabilities are scaled by the total. `chisquare` returns the
statistic and the upper-tail probability under the chi-square distribution with k − 1 degrees of
freedom; comparing that p-value with α replaces the table lookup of a critical value.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
