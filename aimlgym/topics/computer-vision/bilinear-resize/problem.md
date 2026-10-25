# CV-19 · Bilinear Resize

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** CV-05 Flip and Rotate, NP-09 Fancy Indexing and Gather

Read the lesson first: [article.md](article.md)

## Task

Write `resize_bilinear(img, out_h, out_w)` for a 2-D float image using the mapping above. Return a
float array `(out_h, out_w)`. Raise `ValueError` for non-positive sizes or non-2-D input.

**Examples**
```python
img = np.array([[0., 10.], [20., 30.]])
resize_bilinear(img, 4, 4)[1, 1]   # 7.5
resize_bilinear(img, 2, 2)         # equals img (identity size)
resize_bilinear(img, 1, 1)         # [[15.]]  (centre of the image)
```

## Hints

<details><summary>Hint 1</summary>

`y = (np.arange(out_h) + 0.5) * (H / out_h) - 0.5`, then `np.clip(y, 0, H - 1)`.

</details>

<details><summary>Hint 2</summary>

`y0 = np.floor(y).astype(int)`; `y1 = np.minimum(y0 + 1, H - 1)`; `wy = (y - y0)[:, None]`.

</details>

<details><summary>Hint 3</summary>

Corner values: `img[y0][:, x0]`, `img[y0][:, x1]`, `img[y1][:, x0]`, `img[y1][:, x1]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_point` | Map with (i + 0.5)·scale − 0.5 (half-pixel centres), not i·scale. |
| `test_corners_clamped` | Clamp source coordinates to [0, n_in − 1]. |
| `test_identity` | With equal sizes the mapping is the identity. |
| `test_linear_ramp_interior` | Interpolate horizontally between x0 and x1 using weight x − x0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Row and column source coordinates are computed once with half-pixel centres and clamped. Fancy
indexing gathers the four neighbour grids, and broadcasting the fractional weights interpolates
horizontally and then vertically.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
