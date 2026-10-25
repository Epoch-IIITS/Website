# CV-03 · OpenCV Basics: BGR, dtypes and Indexing

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-02 RGB to Grayscale

Read the lesson first: [article.md](article.md)

## Task

1. `to_rgb_and_gray(bgr)` returns `(rgb, gray)` using `cv2.cvtColor` with `COLOR_BGR2RGB` and
   `COLOR_BGR2GRAY`. Raise `ValueError` unless `bgr` is a `uint8` array of shape `(h, w, 3)`.
2. `crop(image, x, y, w, h)` returns a **copy** of the rectangle whose top-left corner is column
   `x`, row `y`, with width `w` and height `h`. Raise `ValueError` if `w` or `h` is not positive or
   the rectangle does not fit inside the image.

**Example**
```python
rgb, gray = to_rgb_and_gray(np.array([[[255, 0, 0]]], dtype=np.uint8))
rgb.tolist(), gray.tolist()     # ([[[0, 0, 255]]], [[29]])
```

## Hints

<details><summary>Hint 1</summary>

Check `isinstance(bgr, np.ndarray)`, `bgr.dtype == np.uint8`, `bgr.ndim == 3` and `bgr.shape[2] == 3`.

</details>

<details><summary>Hint 2</summary>

`cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)` and `cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)`.

</details>

<details><summary>Hint 3</summary>

Rows come first: `image[y:y + h, x:x + w].copy()` after checking `x + w <= width` and `y + h <= height`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_blue_pixel` | OpenCV images are BGR: use COLOR_BGR2RGB and COLOR_BGR2GRAY. |
| `test_crop_rows_then_columns` | Index image[y:y + h, x:x + w] — rows (y) first. |
| `test_crop_is_copy` | Return .copy() of the slice. |
| `test_invalid` | Require uint8 (h, w, 3) images and rectangles inside the image. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`cvtColor` handles the channel order and the greyscale weights. The crop converts OpenCV's (x, y,
w, h) rectangle into NumPy's row-then-column slice and copies it so the caller can modify the crop
without touching the original.

## References

- [Color conversions (OpenCV 4.13)](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html) — OpenCV team (`S115`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
