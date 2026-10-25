# CV-04 · Flips, Rotations and Affine Warps

**Topic:** Computer Vision · **Difficulty:** beginner · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-03 OpenCV Basics: BGR, dtypes and Indexing

Read the lesson first: [article.md](article.md)

## Task

1. `transform(image, op)` with `op` one of `"flip_h"`, `"flip_v"`, `"rot90_cw"`, `"rot180"`,
   `"rot90_ccw"`, using `cv2.flip` and `cv2.rotate`; any other op raises `ValueError`.
2. `rotate_about_centre(image, angle, scale=1.0)` rotates about ((w − 1)/2, (h − 1)/2) with
   `getRotationMatrix2D` and `warpAffine`, keeping the image size.
3. `translate(image, dx, dy)` shifts the image right by `dx` and down by `dy` pixels with
   `warpAffine`, filling uncovered pixels with 0.

Results keep the input's dtype.

## Hints

<details><summary>Hint 1</summary>

Map op names to `lambda img: cv2.flip(img, 1)`, `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)` and so on.

</details>

<details><summary>Hint 2</summary>

`h, w = image.shape[:2]`; `M = cv2.getRotationMatrix2D(((w - 1) / 2, (h - 1) / 2), angle, scale)`.

</details>

<details><summary>Hint 3</summary>

`cv2.warpAffine(image, M, (w, h))` — the size is (width, height); for translation `M = np.float32([[1, 0, dx], [0, 1, dy]])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_flips` | flip_h is cv2.flip(img, 1); flip_v is cv2.flip(img, 0). |
| `test_rotate_about_centre_is_counter_clockwise` | Rotate about ((w - 1) / 2, (h - 1) / 2). |
| `test_rotation_keeps_size_and_dtype` | warpAffine's size argument is (width, height). |
| `test_translate` | The translation matrix is [[1, 0, dx], [0, 1, dy]]. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Flips and quarter turns are exact rearrangements. A rotation about the pixel-exact centre and a
pure translation are both affine matrices; `warpAffine` resamples the image through them into an
output of the original (width, height), filling uncovered pixels with zeros.

## References

- [Geometric Transformations of Images (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) — OpenCV team (`S116`)
- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
