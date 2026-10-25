# PD-15 · Binning with pd.cut

**Topic:** Pandas · **Difficulty:** advanced · **Allowed packages:** pandas, numpy

**Builds on:** PD-08 Group-by Aggregation, ST-04 Histogram with Equal-Width Bins

Read the lesson first: [article.md](article.md)

## Task

Implement with edges `[0, 13, 20, 65, inf)` and labels `child, teen, adult, senior`
(left-closed intervals):
* `age_groups(ages)` → categorical Series of labels (NaN for negative ages).
* `group_counts(ages)` → `dict` mapping every label (in bin order) to its count (ints, zeros
  included), ignoring NaN.

**Examples**
```python
age_groups([5, 13, 19, 20, 70, -1]).tolist()   # ['child', 'teen', 'teen', 'adult', 'senior', nan]
group_counts([5, 13, 19, 20, 70, -1])          # {'child': 1, 'teen': 2, 'adult': 1, 'senior': 1}
group_counts([30])                             # {'child': 0, 'teen': 0, 'adult': 1, 'senior': 0}
```

## Hints

<details><summary>Hint 1</summary>

`pd.cut(pd.Series(ages), bins=EDGES, labels=LABELS, right=False)`.

</details>

<details><summary>Hint 2</summary>

`value_counts(sort=False)` keeps category order and includes zeros.

</details>

<details><summary>Hint 3</summary>

Convert to a dict with int values: `{k: int(v) for k, v in counts.items()}`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_edges_left_closed` | Use right=False so 13 is a teen and 65 a senior. |
| `test_large` | The last edge must be np.inf. |
| `test_counts_zeros_and_order` | Use value_counts(sort=False) and include every label. |
| `test_groups` | Negative ages fall outside the bins and become NaN. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`pd.cut` maps each age to its left-closed interval and attaches labels; negative ages fall
outside every bin and become NaN. Counting over the categorical keeps the bin order and reports
empty categories as 0.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
