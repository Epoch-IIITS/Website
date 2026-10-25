# CV-08 · Histograms and Equalisation

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-06 Thresholding and Otsu's Method

Read the lesson first: [article.md](article.md)

## Task

Write `histogram_and_equalise(gray, bins=256)` returning
`{"hist": list[int], "equalized": uint8 array}` where `hist` is `cv2.calcHist` with `bins` bins over
`[0, 256)` converted to a list of ints, and `equalized` is `cv2.equalizeHist(gray)`.

Raise `ValueError` unless `gray` is a 2-D `uint8` array and `1 <= bins <= 256`.

## Hints

<details><summary>Hint 1</summary>

Validate the image and the bin count first.

</details>

<details><summary>Hint 2</summary>

`cv2.calcHist([gray], [0], None, [bins], [0, 256])` returns shape (bins, 1).

</details>

<details><summary>Hint 3</summary>

`[int(v) for v in hist.ravel()]`; `cv2.equalizeHist(gray)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_matches_bincount` | calcHist ranges are [0, 256): the upper bound is exclusive. |
| `test_coarse_bins` | Pass [bins] as histSize. |
| `test_types` | Convert the float32 counts to a list of ints. |
| `test_invalid` | Require a 2-D uint8 image and 1 <= bins <= 256. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`calcHist` counts pixels in equal-width bins across [0, 256); flattening and converting gives a
plain list of counts. `equalizeHist` remaps intensities through the cumulative histogram so the
output spreads over the full range.

## References

- [Histogram Equalization (OpenCV 4.13)](https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html) — OpenCV team (`S118`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
