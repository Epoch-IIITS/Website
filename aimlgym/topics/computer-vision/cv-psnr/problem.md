# CV-16 · Image Quality: MSE and PSNR

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-15 A Convolution Layer with Channels, CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d

Read the lesson first: [article.md](article.md)

## Task

Write `image_quality(reference, distorted)` returning `{"mse": float, "psnr": float}` for two
`uint8` images of the same shape.

* `mse` is computed in floating point.
* `psnr` is `math.inf` when `mse` is 0, otherwise `cv2.PSNR(reference, distorted)`.
* Raise `ValueError` if the shapes differ or either image is not `uint8`.

## Hints

<details><summary>Hint 1</summary>

Check `reference.shape == distorted.shape` and both dtypes.

</details>

<details><summary>Hint 2</summary>

`diff = reference.astype(np.float64) - distorted.astype(np.float64)`; `mse = float(np.mean(diff ** 2))`.

</details>

<details><summary>Hint 3</summary>

Return `math.inf` for zero error, otherwise `float(cv2.PSNR(reference, distorted))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_no_wraparound` | Convert to float before subtracting uint8 images. |
| `test_identical_is_infinite` | Return math.inf when the MSE is zero. |
| `test_symmetric_and_formula` | PSNR = 10·log10(255² / MSE). |
| `test_invalid` | Require two uint8 images with the same shape. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Converting to float before subtracting avoids uint8 wrap-around. OpenCV's PSNR uses the 8-bit peak
of 255; zero error is reported as infinity instead of OpenCV's large finite stand-in.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
