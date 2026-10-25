# Median and Mode

## Learning outcomes

After this lesson you can:

- Compute the median for odd and even n
- Find all modes including ties
- Explain robustness to outliers

## Intuition
The **median** is the middle value when the data is sorted — half the data is below it, half
above. The **mode** is the most common value. Unlike the mean, the median barely moves when one
value is extreme: the median salary in a room doesn't change when a billionaire walks in.

## Precise explanation
Sort the data, $x_{(1)} \le \dots \le x_{(n)}$.
* $n$ odd: median $= x_{((n+1)/2)}$ — in 0-based Python, `s[n // 2]`.
* $n$ even: median = average of the two middle values, `(s[n//2 - 1] + s[n//2]) / 2`.

A dataset may have several modes (multimodal). Returning all of them, sorted, is unambiguous.
`statistics.multimode` returns them in first-occurrence order; here we sort for determinism.

## Worked example
`[7, 1, 3, 3, 100]` → sorted `[1, 3, 3, 7, 100]` → median 3, mean 22.8 (pulled by 100).
`[4, 1, 2, 3]` → sorted `[1, 2, 3, 4]` → median 2.5. Modes of `[1, 2, 2, 3, 3]` → `[2, 3]`.

## Common mistakes
* Taking the middle element without sorting.
* Using `n / 2` (a float) as an index.
* Returning only the first mode when there is a tie.

## Why this matters
Robust statistics (median, IQR) are used for outlier-resistant scaling and to impute missing
values; the mode is the natural imputation for categorical data.

## Library implementation

`statistics.median` averages the two middle values for even-length data, and
`statistics.multimode` returns every most-common value (in first-seen order; your function
sorts them). `statistics.mode` returns only one value.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
