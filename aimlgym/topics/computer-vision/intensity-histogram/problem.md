# CV-09 · Intensity Histogram

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** CV-02 RGB to Grayscale, ST-04 Histogram with Equal-Width Bins

Read the lesson first: [article.md](article.md)

## Task

For `uint8` grayscale images implement:
* `histogram256(gray)` → int array of length 256 (raise `ValueError` if dtype is not uint8).
* `cdf(hist)` → cumulative counts.
* `equalize(gray)` → uint8 image using the formula above (rounding with `np.rint`).

**Example**
```python
g = np.array([[50, 50], [51, 52]], dtype=np.uint8)
equalize(g)   # [[  0,   0], [128, 255]]
```

## Hints

<details><summary>Hint 1</summary>

`np.bincount(gray.ravel(), minlength=256)`.

</details>

<details><summary>Hint 2</summary>

`c_min = c[c > 0].min()`; build a 256-entry lookup table.

</details>

<details><summary>Hint 3</summary>

`lut[gray]` applies the mapping to every pixel at once.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_hist` | Use np.bincount(..., minlength=256). |
| `test_equalize` | Use the first non-zero CDF value as c_min and N − c_min in the denominator. |
| `test_constant` | If every pixel has the same value, return the image unchanged. |
| `test_full_range` | Round the lookup table and cast to uint8. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`bincount` counts each of the 256 intensities. The cumulative counts define a monotone lookup table
that maps the darkest present value to 0 and the brightest to 255; fancy indexing applies the table
to all pixels.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
