# ST-16 · Chi-Square Goodness of Fit by Hand

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** ST-08 Binomial Probabilities

Read the lesson first: [article.md](article.md)

## Task

Write `chi_square_gof(observed, probs, critical=None)` returning a dict
`{"statistic": float, "df": int, "expected": list[float], "reject": bool | None}`.

* `reject` is `statistic > critical` if `critical` is given, else `None`.
* Raise `ValueError` if lengths differ, fewer than 2 categories, any prob ≤ 0, probs don't sum to
  1 within 1e-9, any observed count is negative, or the total count is 0.

**Examples**
```python
chi_square_gof([5, 8, 9, 8, 10, 20], [1/6]*6, critical=11.070)
# {'statistic': 13.4, 'df': 5, 'expected': [10.0]*6, 'reject': True}
chi_square_gof([50, 50], [0.5, 0.5])
# {'statistic': 0.0, 'df': 1, 'expected': [50.0, 50.0], 'reject': None}
```

## Hints

<details><summary>Hint 1</summary>

Validate inputs, then `N = sum(observed)` and `expected = [N * p for p in probs]`.

</details>

<details><summary>Hint 2</summary>

`stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))`.

</details>

<details><summary>Hint 3</summary>

`df = len(observed) - 1`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_die` | Divide each squared difference by the expected count, and df = k − 1. |
| `test_unequal_probs` | Expected counts are N × p_i for each category. |
| `test_bad_probs` | Check that probs sum to 1 (within 1e-9). |
| `test_not_reject` | reject is statistic > critical. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

After validation, expected counts are the total times each probability. The statistic sums the
squared gaps scaled by expected counts; df is one less than the number of categories because the
counts are constrained to sum to N. The optional critical value turns the statistic into a decision.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
