# PD-05 · Derived Columns

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** PD-04 Select and Filter Rows

Read the lesson first: [article.md](article.md)

## Task

Write `add_features(df)` for a DataFrame with numeric columns `a` and `b`. Return a **new**
DataFrame with extra columns:
* `total = a + b`
* `ratio = a / b`, NaN where `b == 0`
* `passed = total >= 50` (boolean)

The input must not be modified.

**Example**
```python
add_features(pd.DataFrame({"a": [30, 10, 0], "b": [20, 0, 0]}))
#     a   b  total  ratio  passed
# 0  30  20     50    1.5    True
# 1  10   0     10    NaN   False
# 2   0   0      0    NaN   False
```

## Hints

<details><summary>Hint 1</summary>

`total = df['a'] + df['b']`.

</details>

<details><summary>Hint 2</summary>

`ratio = (df['a'] / df['b']).where(df['b'] != 0)`.

</details>

<details><summary>Hint 3</summary>

Use `df.assign(total=..., ratio=..., passed=...)`; compute passed from total.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_ratio_nan` | Mask the ratio where b == 0 using .where(df['b'] != 0). |
| `test_no_inf` | Division by zero gives inf — replace it with NaN. |
| `test_not_mutated` | Use df.assign (returns a new frame) instead of df['x'] = ... |
| `test_passed` | passed is total >= 50 (inclusive). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All three features are vectorised column expressions. `where(b != 0)` converts the undefined
ratios (inf and NaN from division by zero) into NaN. `assign` returns a new frame, so the input is
unchanged.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
