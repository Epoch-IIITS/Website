# CV-02 · RGB to Grayscale

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** CV-01 Images as Arrays

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `rgb_to_gray(img)` → float array `(H, W)` with BT.601 weights; raise `ValueError` unless
  `img.shape[-1] == 3` and `img.ndim == 3`.
* `to_uint8(x)` → round to nearest (`np.rint`), clip to [0, 255], return `uint8`.

**Examples**
```python
img = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)
to_uint8(rgb_to_gray(img))   # [[ 76, 150], [ 29, 255]]
to_uint8(np.array([-5., 300., 12.5]))   # [  0, 255,  12]   (rint rounds half to even)
```

## Hints

<details><summary>Hint 1</summary>

Convert with `img.astype(float)` before multiplying.

</details>

<details><summary>Hint 2</summary>

`img @ np.array([0.299, 0.587, 0.114])` contracts the channel axis.

</details>

<details><summary>Hint 3</summary>

`np.clip(np.rint(x), 0, 255).astype(np.uint8)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_values` | Use weights 0.299, 0.587, 0.114 for R, G, B. |
| `test_no_overflow` | Convert to float before arithmetic; uint8 wraps around. |
| `test_clip_round` | Round with np.rint, then clip, then cast to uint8. |
| `test_bad_shape` | Require ndim == 3 and 3 channels. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Casting to float avoids uint8 overflow; a matrix product with the weight vector collapses the
channel axis. Conversion back rounds, clips and casts, in that order.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
