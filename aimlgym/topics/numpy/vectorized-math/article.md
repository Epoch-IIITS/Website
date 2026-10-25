# Vectorised Arithmetic and ufuncs

## Learning outcomes

After this lesson you can:

- Replace element-by-element loops with array expressions
- Use universal functions (np.exp, np.sqrt, np.abs, np.where)
- Check a vectorised result against a loop with np.allclose
- Write a sigmoid that never overflows on arrays

## Intuition
In MA-04 you wrote a loop that multiplies matching elements and adds them up. NumPy
lets you write the *whole* operation at once: `a * b` multiplies every pair of elements, and
`.sum()` adds them. The loop still happens, but inside fast compiled code, typically tens to
hundreds of times faster than a Python loop on large arrays.

## Precise explanation
* Arithmetic operators on arrays of the same shape work **element-wise**:
  `a + b`, `a * b`, `a ** 2`, `a / 2`, `-a`. Mixing an array and a number applies the number to
  every element: `c * 9 / 5 + 32`.
* **Universal functions (ufuncs)** are element-wise functions: `np.exp`, `np.log`, `np.sqrt`,
  `np.abs`, `np.maximum(a, b)`. `math.exp` only accepts single numbers; `np.exp` accepts arrays.
* Reductions collapse an array: `a.sum()`, `a.mean()`, `a.max()`.
* `np.where(cond, x, y)` picks from `x` where `cond` is true and from `y` elsewhere. Both `x` and
  `y` are computed for every element, so they must not overflow.
* Comparing floats: use `np.allclose(a, b)` (tolerance) instead of `==`.

**Stable vectorised sigmoid.** MA-03 branched on the sign of one number. For
arrays, compute `e = np.exp(-np.abs(x))` (never larger than 1), then
`np.where(x >= 0, 1 / (1 + e), e / (1 + e))`.

## Worked example
```python
import numpy as np
a = np.array([1.0, 2.0, 3.0]); b = np.array([4.0, 5.0, 6.0])
a * b            # array([ 4., 10., 18.])
(a * b).sum()    # 32.0 — the dot product
np.sqrt(np.mean(a ** 2))   # root-mean-square ≈ 2.160
```

## Common mistakes
* Using `math.exp(array)` → `TypeError`; use `np.exp`.
* Python lists do not vectorise: `[1, 2] * 2` is `[1, 2, 1, 2]`. Convert with `np.asarray`.
* Integer arrays: `np.array([1, 2]) / 2` is float, but in-place `a /= 2` on an int array fails;
  create float arrays with `dtype=float`.
* Shape mismatches such as `(3,) * (4,)` raise `ValueError` — check shapes first.

## Why this matters
Every later topic expresses its maths as array expressions; checking them against a slow,
obviously-correct loop is the standard way to test numerical code.

## Library implementation

NumPy also has a dedicated function for this step: `np.dot(a, b)` (or `a @ b`, introduced in
NP-06) computes the dot product directly, and is what you would normally write.
The element-wise form `(a * b).sum()` shows what `np.dot` does. `scipy.special.expit` is a
library sigmoid for arrays. The tests compare your functions with these.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Universal functions (ufunc) basics (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/basics.ufuncs.html) — NumPy Developers (`S081`)
