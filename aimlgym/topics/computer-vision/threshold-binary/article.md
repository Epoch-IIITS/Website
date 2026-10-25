# Binary Thresholding

## Learning outcomes

After this lesson you can:

- Create binary masks from grayscale images
- Invert masks and measure foreground fraction
- Apply a mask to an image

## Intuition
To separate dark text from a white page, call every pixel brighter than some level "background"
and the rest "foreground". Thresholding is the simplest segmentation.

## Precise explanation
* Binary threshold: `mask = gray > t` (OpenCV's `THRESH_BINARY` uses strictly greater than).
  `invert=True` gives `gray <= t`.
* Foreground fraction = `mask.mean()` (True counts as 1).
* Applying a mask: keep pixels where mask is True, zero elsewhere — `np.where(mask[..., None], img, 0)`
  for colour images (the mask broadcasts over channels).
* Choosing t automatically: Otsu's method (CV-09 extension) picks the threshold that best separates
  two histogram modes.

## Worked example
gray [[10, 200], [128, 127]], t = 127 → mask [[F, T], [T, F]] → fraction 0.5.

## Common mistakes
* `>=` vs `>` at the boundary.
* Producing 0/255 uint8 images and then using them as booleans incorrectly.
* Forgetting to broadcast the mask over colour channels.

## Why this matters
Masks are the language of segmentation: models output per-pixel masks and evaluation compares them.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
