# NP-02 · Vectorised Arithmetic and ufuncs

**Topic:** NumPy · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** NP-01 Create an Array and Inspect It, MA-03 The Sigmoid Function

Read the lesson first: [article.md](article.md)

## Task

Implement (inputs may be lists or arrays; convert with `np.asarray(x, dtype=float)`):

1. `dot_loop(a, b)` — the dot product with a Python loop (raise `ValueError` if lengths differ).
2. `dot_vectorized(a, b)` — the same with `*` and `.sum()` (same `ValueError`); return a `float`.
3. `fahrenheit(celsius)` — `celsius * 9 / 5 + 32` as an array.
4. `rms(x)` — root-mean-square $\sqrt{\frac1n\sum x_i^2}$ as a `float`.
5. `sigmoid(x)` — stable element-wise sigmoid returning an array of the same shape; must not
   produce warnings or `nan` for inputs like `[-1000, 0, 1000]`.

**Examples**
```python
dot_vectorized([1, 2, 3], [4, 5, 6])   # 32.0
fahrenheit([0, 100])                    # array([ 32., 212.])
sigmoid([-1000, 0, 1000])               # array([0. , 0.5, 1. ])
```

## Hints

<details><summary>Hint 1</summary>

`a = np.asarray(a, dtype=float)`; compare `a.shape != b.shape` before multiplying; `float((a * b).sum())`.

</details>

<details><summary>Hint 2</summary>

`float(np.sqrt(np.mean(x ** 2)))` for RMS.

</details>

<details><summary>Hint 3</summary>

`e = np.exp(-np.abs(x)); return np.where(x >= 0, 1 / (1 + e), e / (1 + e))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_dot_matches_loop` | Multiply the arrays element-wise and call `.sum()`; return a Python float. |
| `test_dot_mismatch` | Compare the shapes and raise ValueError before multiplying. |
| `test_rms` | Square, average, then take the square root. |
| `test_sigmoid_stable` | Avoid `np.exp(-x)` for very negative x; use `np.exp(-np.abs(x))` with `np.where`. |
| `test_sigmoid_shape` | Keep the input shape: operate on the whole array without flattening. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Converting inputs to float arrays makes every operator element-wise. The dot product becomes one
multiplication and one reduction; RMS chains a power, a mean and a square root. The sigmoid only
exponentiates non-positive numbers, so both branches given to `np.where` are finite everywhere.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Universal functions (ufunc) basics (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/basics.ufuncs.html) — NumPy Developers (`S081`)
