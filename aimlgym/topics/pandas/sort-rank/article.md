# Sorting and Ranking

## Learning outcomes

After this lesson you can:

- Sort by several columns with different directions
- Rank with ties (method='min')
- Take the top-n rows

## Intuition
A leaderboard sorts by score (highest first) and assigns ranks. When two people tie, they share
a rank and the next rank is skipped (1, 2, 2, 4) — "competition ranking".

## Precise explanation
* `df.sort_values(["score", "name"], ascending=[False, True])` sorts by score descending and
  breaks ties by name ascending. Use `kind="mergesort"` (stable) when order of equal keys matters.
* `df["score"].rank(method="min", ascending=False)` gives competition ranks: tied values get the
  smallest rank of their group. Other methods: `"dense"` (1, 2, 2, 3), `"average"` (1, 2.5, 2.5, 4),
  `"first"` (by appearance).
* Ranks are floats; convert with `.astype(int)` when there are no NaNs.
* `df.head(n)` keeps the first n rows after sorting.

## Worked example
scores ann 90, bob 85, cy 90, dee 70 → sorted ann 90, cy 90, bob 85, dee 70 → ranks 1, 1, 3, 4.

## Common mistakes
* `ascending=False` for both keys, reversing the alphabetical tie-break.
* Using `method="dense"` when competition ranking is required (or vice versa).
* Ranking before filtering, then wondering why ranks have gaps.

## Why this matters
Ranking metrics (precision@k), feature importance tables (XA-02) and leaderboards all require
correct, deterministic tie handling.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
