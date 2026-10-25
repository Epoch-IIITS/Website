# PD-07 · Sort and Rank

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-06 Finding and Handling Missing Values

Read the lesson first: [article.md](article.md)

## Task

Write `leaderboard(df, n=None)` for columns `name` and `score`. Return a new DataFrame:
* sorted by `score` descending, then `name` ascending,
* with an `int` column `rank` using competition ranking (`method="min"`) on score,
* index reset to 0..k−1, keeping only the first `n` rows if `n` is given (ties beyond row n are
  cut).

**Example**
```python
leaderboard(pd.DataFrame({"name": ["bob", "ann", "dee", "cy"], "score": [85, 90, 70, 90]}))
#   name  score  rank
# 0  ann     90     1
# 1   cy     90     1
# 2  bob     85     3
# 3  dee     70     4
```

## Hints

<details><summary>Hint 1</summary>

`out = df.sort_values(['score', 'name'], ascending=[False, True])`.

</details>

<details><summary>Hint 2</summary>

`out['rank'] = out['score'].rank(method='min', ascending=False).astype(int)` on the copy.

</details>

<details><summary>Hint 3</summary>

`reset_index(drop=True)` and `head(n)` if n is not None.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_order` | ascending=[False, True]: score descending, name ascending. |
| `test_ranks` | Use rank(method='min', ascending=False). |
| `test_rank_int` | Convert ranks to int with .astype(int). |
| `test_input_unchanged` | Don't add the rank column to the original DataFrame. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A two-key stable sort gives the display order; ranking on the score column with `method="min"`
assigns shared ranks to ties and skips the following rank. `assign` keeps the input untouched.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
