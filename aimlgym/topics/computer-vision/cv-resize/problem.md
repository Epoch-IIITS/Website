# CV-18 · Resizing with cv2.resize

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-16 Image Quality: MSE and PSNR

Read the lesson first: [article.md](article.md)

## Task

Write `resize(image, width, height, method="linear")` returning `cv2.resize(image, (width, height),
interpolation=...)` with `method` one of `"nearest"`, `"linear"`, `"cubic"`, `"area"`.

Raise `ValueError` for an unknown method or a non-positive width or height.

## Hints

<details><summary>Hint 1</summary>

Map the names to `cv2.INTER_NEAREST`, `cv2.INTER_LINEAR`, `cv2.INTER_CUBIC`, `cv2.INTER_AREA`.

</details>

<details><summary>Hint 2</summary>

Validate `width > 0 and height > 0`.

</details>

<details><summary>Hint 3</summary>

`cv2.resize(image, (width, height), interpolation=METHODS[method])` — width first.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_size_order` | cv2.resize takes (width, height). |
| `test_area_halving_averages_blocks` | Use cv2.INTER_AREA for 'area'. |
| `test_nearest_keeps_labels` | Use cv2.INTER_NEAREST for 'nearest'. |
| `test_invalid` | Reject unknown methods and non-positive sizes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A dictionary maps readable names to OpenCV's interpolation flags. The only subtle part is the size
argument, which OpenCV takes as (width, height) although the result's shape is (height, width).

## References

- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
