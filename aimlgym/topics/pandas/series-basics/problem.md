# PD-01 · Series: Labelled Columns

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** NP-04 Boolean Masks

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `make_series(data)` — a `float` Series from a dict of label → number.
2. `add_aligned(a, b)` — add two Series by label, treating a missing side as 0; return the
   result sorted by label.
3. `above_mean(s)` — list of labels whose value is strictly above the Series mean, in Series
   order.
4. `top_labels(s, k)` — list of the labels of the `k` largest values, largest first (use
   `nlargest`).
5. `count_values(items)` — a plain `dict` value → count built from `value_counts()`, with
   `int` counts.

**Examples**
```python
s = make_series({"apple": 1.2, "pear": 0.8, "fig": 2.5})
above_mean(s)                 # ['fig']
top_labels(s, 2)              # ['fig', 'apple']
count_values(["a", "b", "a"]) # {'a': 2, 'b': 1}
```

## Hints

<details><summary>Hint 1</summary>

`a.add(b, fill_value=0).sort_index()`.

</details>

<details><summary>Hint 2</summary>

`s[s > s.mean()].index.tolist()`.

</details>

<details><summary>Hint 3</summary>

`counts = pd.Series(items).value_counts()`; build `{k: int(v) for k, v in counts.items()}`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_add_aligned` | Use `a.add(b, fill_value=0)` so labels in only one Series are not NaN, then `sort_index()`. |
| `test_above_mean` | Select with `s[s > s.mean()]` and return its index as a list. |
| `test_top_labels` | `s.nlargest(k).index.tolist()` keeps the largest-first order. |
| `test_count_values` | Convert the counts to plain ints in a dict. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each function is one Series operation: `add` with `fill_value` aligns by label without producing
NaN, a boolean mask selects labels above the mean, `nlargest` ranks by value and keeps labels,
and `value_counts` produces a Series of counts that is converted back to a plain dict.

## References

- [Intro to data structures (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/dsintro.html) — pandas development team (`S084`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
