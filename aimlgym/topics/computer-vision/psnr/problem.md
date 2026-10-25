# CV-17 · MSE and PSNR by Hand

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-01 Images as Arrays, ML-02 The scikit-learn Estimator API

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `mse(a, b)` → float; raise `ValueError` if shapes differ or arrays are empty.
* `psnr(a, b, max_val=255.0)` → float dB, `math.inf` for identical images.

**Examples**
```python
mse(np.array([[0, 0]], np.uint8), np.array([[0, 255]], np.uint8))    # 32512.5
psnr(np.array([[0, 0]], np.uint8), np.array([[0, 255]], np.uint8))   # 3.0103
mse(np.array([3], np.uint8), np.array([5], np.uint8))                # 4.0 (not 254**2)
```

## Hints

<details><summary>Hint 1</summary>

`a = np.asarray(a, dtype=float)` before subtracting.

</details>

<details><summary>Hint 2</summary>

`float(np.mean((a - b) ** 2))`.

</details>

<details><summary>Hint 3</summary>

`10 * math.log10(max_val ** 2 / m)`; return `math.inf` if `m == 0`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_overflow` | Cast to float before subtracting uint8 arrays. |
| `test_identical` | Return math.inf when MSE is 0. |
| `test_max_val` | PSNR = 10·log10(MAX² / MSE). |
| `test_shape` | Raise ValueError if shapes differ. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Converting to float before subtraction avoids uint8 wrap-around. PSNR applies the logarithmic
formula, handling the zero-error case explicitly.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
