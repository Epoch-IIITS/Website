# Boolean Masks

## Learning outcomes

After this lesson you can:

- Build boolean masks with comparisons
- Combine masks with & | ~
- Replace values with np.where without loops

## Intuition
A mask is a same-shaped array of True/False that marks which elements you care about. Indexing
with a mask keeps the True positions — the vectorised version of the filtering loop from PY-12.

## Precise explanation
* `a > 3` returns a boolean array. `a[a > 3]` returns a **1-D copy** of the selected values.
* Combine masks element-wise with `&` (and), `|` (or), `~` (not). Parentheses are required:
  `(a >= lo) & (a <= hi)` — `&` binds tighter than `>=`.
* Python's `and`/`or` do **not** work on arrays (they raise "truth value is ambiguous").
* `mask.sum()` counts True values (True = 1).
* `np.where(cond, x, y)` builds a new array taking `x` where cond is True and `y` elsewhere.
  `np.minimum(a, t)` is an alternative for capping.

## Worked example
```python
a = np.array([4, -1, 9, 3, 12])
a[(a >= 0) & (a <= 9)]   # [4, 9, 3]
(a > 5).sum()            # 2
np.where(a > 5, 5, a)    # [4, -1, 5, 3, 5]
```

## Common mistakes
* `a > 0 and a < 9` → `ValueError`.
* Missing parentheses: `a >= 0 & a <= 9` evaluates `0 & a` first.
* Modifying `a[a > 5]` expecting a view: `b = a[a > 5]; b[:] = 0` does not change `a`
  (but `a[a > 5] = 0` does, because it is an assignment through the mask).

## Why this matters
Masks select rows in pandas, threshold images (CV-07), build causal attention masks (LM-08) and
apply ReLU (`np.where(z > 0, z, 0)`).

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
