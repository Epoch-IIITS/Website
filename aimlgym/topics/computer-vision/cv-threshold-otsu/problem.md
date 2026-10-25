# CV-06 · Thresholding and Otsu's Method

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-04 Flips, Rotations and Affine Warps

Read the lesson first: [article.md](article.md)

## Task

Write `binarise(gray, threshold=None, invert=False)` returning `(t, mask)` where `t` is a float and
`mask` a `uint8` array of 0s and 255s.

* With a number, use `cv2.threshold(gray, threshold, 255, kind)`; with `None`, use Otsu
  (`kind + cv2.THRESH_OTSU`, threshold argument 0).
* `kind` is `cv2.THRESH_BINARY_INV` when `invert` is true, else `cv2.THRESH_BINARY`.
* Raise `ValueError` unless `gray` is a 2-D `uint8` array.

## Hints

<details><summary>Hint 1</summary>

Validate: `gray.ndim == 2 and gray.dtype == np.uint8`.

</details>

<details><summary>Hint 2</summary>

`kind = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY`.

</details>

<details><summary>Hint 3</summary>

For Otsu: `cv2.threshold(gray, 0, 255, kind + cv2.THRESH_OTSU)`; return `float(t), mask`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_fixed_threshold_is_strict` | THRESH_BINARY marks pixels strictly greater than the threshold. |
| `test_otsu_matches_between_class_variance` | With threshold=None add cv2.THRESH_OTSU and return the chosen t. |
| `test_invert` | Use THRESH_BINARY_INV when invert is true. |
| `test_invalid` | Only 2-D uint8 images are accepted. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One `cv2.threshold` call covers both cases; adding the Otsu flag makes OpenCV choose the
threshold from the histogram and return it. Inversion only swaps which side becomes 255.

## References

- [Image Thresholding (OpenCV 4.13)](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) — OpenCV team (`S117`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
