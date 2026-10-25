# CV-12 · Sobel Edge Magnitude

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-10 2D Filtering (Blur)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `sobel(gray)` → `(gx, gy, magnitude)` arrays of shape `(H-2, W-2)` (valid cross-correlation with
  the kernels above). Raise `ValueError` if the image is smaller than 3×3.
* `edges(gray, t)` → boolean `(H-2, W-2)` mask `magnitude > t`.

**Example**
```python
g = np.array([[0, 0, 10, 10]] * 4, float)
gx, gy, mag = sobel(g)
gx    # [[40., 40.], [40., 40.]]
gy    # [[0., 0.], [0., 0.]]
```

## Hints

<details><summary>Hint 1</summary>

Valid output size `(H-2, W-2)`; for each kernel entry add `K[u, v] * g[u:u+H-2, v:v+W-2]`.

</details>

<details><summary>Hint 2</summary>

Apply the same helper with KX and KY.

</details>

<details><summary>Hint 3</summary>

`np.hypot(gx, gy)` is the magnitude.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_vertical_edge` | Kx = [[-1,0,1],[-2,0,2],[-1,0,1]] responds to left→right change. |
| `test_shape_and_uint8` | Convert to float first; uint8 cannot hold negative gradients. |
| `test_ramp` | Use valid (unpadded) cross-correlation, output (H−2, W−2). |
| `test_edges` | edges uses strict magnitude > t. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A valid cross-correlation helper applies each 3×3 kernel; the two gradient maps combine into a
magnitude with `hypot`. Using floats preserves negative gradients.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
