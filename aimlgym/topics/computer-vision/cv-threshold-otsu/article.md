# Thresholding and Otsu's Method

## Learning outcomes

After this lesson you can:

- Binarise an image with cv2.threshold and a fixed threshold
- Let Otsu's method choose the threshold from the histogram
- Invert masks with THRESH_BINARY_INV

## Intuition
To separate dark text from a light page, or bright cells from a dark background, mark every pixel
brighter than some value as foreground. Picking that value by hand works for one photo and fails
on the next; Otsu's method picks it from the image's own histogram.

## Precise explanation
```python
t, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)          # mask = 255 where gray > 127
t, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   # t chosen by Otsu
```

* `THRESH_BINARY` sets pixels **strictly greater** than the threshold to `maxval` (255), others
  to 0; `THRESH_BINARY_INV` does the opposite.
* With `THRESH_OTSU` the threshold argument is ignored and the returned `t` is the chosen value.
  Otsu tries every threshold and keeps the one that maximises the **between-class variance**
  w₀w₁(μ₀ − μ₁)², where w are the fractions of pixels below/above and μ their mean intensities.
  It works best when the histogram has two clear peaks.
* The input must be single-channel `uint8` for Otsu.

## Worked example
Pixels [10, 30, 200, 220]: any threshold from 30 to 199 separates the two groups; Otsu returns
30, and the mask is [0, 0, 255, 255].

## What the library does inside
A fixed threshold is the comparison `gray > t` from CV-07 (the optional deep dive
after this step). Otsu adds one pass over the 256-bin histogram (CV-08 next) to score
each candidate threshold.

## Common mistakes
* Expecting pixels equal to the threshold to be foreground (the test is strict).
* Passing a colour image to Otsu.
* Thresholding a photo with uneven lighting; blur first, or use `cv2.adaptiveThreshold`.

## Why this matters
Thresholding is the first step of document scanning, cell counting and many industrial
inspection systems; contours and connected components work on its masks.

## References

- [Image Thresholding (OpenCV 4.13)](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html) — OpenCV team (`S117`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
