# Series: Labelled Columns

## Learning outcomes

After this lesson you can:

- Create a Series from a dict and read values by label
- Explain index alignment in arithmetic between Series
- Filter with boolean masks and summarise with mean, nlargest and value_counts
- Compare each Series operation with the equivalent dict code

## Intuition
A NumPy array is a row of numbers addressed by position. A pandas **Series** is a NumPy array
plus a **label** for every value — like a dict that also supports vectorised arithmetic.
Labels make data self-describing: `prices["apple"]` instead of `prices[3]`.

## Precise explanation
```python
import pandas as pd
s = pd.Series({"apple": 1.2, "pear": 0.8, "fig": 2.5})
s["pear"]          # 0.8   — by label
s.index            # Index(['apple', 'pear', 'fig'], dtype=...)
s.values           # the underlying NumPy array
s[s > 1.0]         # boolean mask, as in NumPy: apple and fig
s.mean(), s.max()  # reductions
s.nlargest(2)      # the two largest values with their labels
pd.Series(["a", "b", "a"]).value_counts()   # counts of each value, largest first
```
* **Alignment**: `a + b` matches values **by label**, not position. A label present in only one
  Series gives `NaN` (missing). `a.add(b, fill_value=0)` treats a missing side as 0 instead.
* `.to_dict()` turns a Series back into a dict; `.index.tolist()` gives the labels.

| Task | dict version | Series version |
|---|---|---|
| add matching keys | `{k: a.get(k, 0) + b.get(k, 0) for k in a.keys() | b.keys()}` | `a.add(b, fill_value=0)` |
| keys with value above the mean | loop + `sum(d.values()) / len(d)` | `s[s > s.mean()]` |
| counts | `Counter(items)` | `pd.Series(items).value_counts()` |

## Worked example
```python
a = pd.Series({"x": 1, "y": 2}); b = pd.Series({"y": 10, "z": 5})
a + b                      # x NaN, y 12, z NaN
a.add(b, fill_value=0)     # x 1.0, y 12.0, z 5.0
```

## Common mistakes
* Expecting `a + b` to pair values by position.
* `s[0]` on a Series with string labels: use `s.iloc[0]` for positions and `s.loc[...]` or `s[...]`
  for labels.
* Forgetting that `value_counts` drops missing values unless `dropna=False`.

## Why this matters
Every DataFrame column is a Series (PD-02), and label alignment is what makes
joins and group-by results line up correctly.

## References

- [Intro to data structures (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/dsintro.html) — pandas development team (`S084`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
