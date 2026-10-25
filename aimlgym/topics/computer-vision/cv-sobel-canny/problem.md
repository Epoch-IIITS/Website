# CV-11 · Edges with Sobel and Canny

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-10 2D Filtering (Blur), CV-08 Histograms and Equalisation

Read the lesson first: [article.md](article.md)

## Task

Write `edges(gray, low, high, blur_ksize=5)` returning
`{"gx": float64 array, "gy": float64 array, "magnitude": float64 array, "canny": uint8 array}`.

* `gx`, `gy`: `cv2.Sobel` with `cv2.CV_64F`, `ksize=3`, on the original image.
* `magnitude`: `np.hypot(gx, gy)`.
* `canny`: `cv2.Canny` on `cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)` with `low`, `high`.
* Raise `ValueError` unless `gray` is 2-D `uint8`, `0 <= low <= high`, and `blur_ksize` is a positive
  odd integer.

## Hints

<details><summary>Hint 1</summary>

Validate the image, the thresholds and that `blur_ksize % 2 == 1`.

</details>

<details><summary>Hint 2</summary>

`cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)` for gx and `(0, 1)` for gy.

</details>

<details><summary>Hint 3</summary>

`cv2.Canny(cv2.GaussianBlur(gray, (k, k), 0), low, high)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_negative_gradients_kept` | Use cv2.CV_64F as the Sobel output depth. |
| `test_magnitude` | magnitude = np.hypot(gx, gy). |
| `test_canny_outline` | Blur with GaussianBlur, then cv2.Canny(blurred, low, high). |
| `test_invalid` | Check the image type, 0 <= low <= high and an odd blur size. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Sobel with a float depth keeps the sign of the gradient; the magnitude combines both directions.
Canny runs on a blurred copy so that noise does not produce spurious edges, and returns a binary
mask of thin, connected edges.

## References

- [Canny Edge Detection (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html) — OpenCV team (`S119`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
