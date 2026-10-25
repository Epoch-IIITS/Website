# XA-02 · Ranking Attributions

**Topic:** Explainable AI · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** XA-01 Linear Model Contributions

Read the lesson first: [article.md](article.md)

## Task

Write `top_attributions(names, phi, k=3)` returning a list of up to `k` tuples
`(name, value, direction, share)` ranked as above, `value` and `share` floats, `direction` one of
`"+"`, `"-"`, `"0"`. Raise `ValueError` if lengths differ or `k < 1`.

**Example**
```python
top_attributions(["age", "income", "debt"], np.array([0.5, -2.0, 1.5]), k=2)
# [('income', -2.0, '-', 0.5), ('debt', 1.5, '+', 0.375)]
```

## Hints

<details><summary>Hint 1</summary>

`total = np.abs(phi).sum()`.

</details>

<details><summary>Hint 2</summary>

Sort indices with key `(-abs(phi[i]), names[i])`.

</details>

<details><summary>Hint 3</summary>

Direction via comparisons with 0; share = abs / total (0 if total is 0).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Rank by absolute value; keep the signed value in the output. |
| `test_ties_alphabetical` | Break ties on |phi| by name ascending. |
| `test_zero` | When all attributions are 0, shares are 0 and direction is '0'. |
| `test_shares_sum` | share = |phi_j| / Σ|phi|. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Ranking uses absolute values with an alphabetical tie-break; each entry reports the signed value,
its direction and its share of the total absolute effect.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
