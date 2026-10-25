# OpenCV Basics: BGR, dtypes and Indexing

## Learning outcomes

After this lesson you can:

- Convert between OpenCV's BGR order, RGB and greyscale with cv2.cvtColor
- Keep images as uint8 arrays and know where OpenCV expects them
- Translate OpenCV (x, y) coordinates into NumPy [row, column] indexing

## Intuition
OpenCV images are plain NumPy arrays, so everything from CV-01 still applies. Two
conventions trip everyone up: OpenCV stores colour channels as **B, G, R** (not R, G, B), and its
functions take points as **(x, y)** — column first — while NumPy indexes `[row, column]`.

## Precise explanation
```python
import cv2
bgr = cv2.imread("photo.jpg")                    # (height, width, 3), uint8, channels B, G, R
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)        # for matplotlib or PyTorch models
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)      # (height, width), uint8
patch = bgr[y:y + h, x:x + w]                     # rows first: y, then x
```

* Greyscale uses 0.299 R + 0.587 G + 0.114 B, rounded to the nearest integer — the weights from
  CV-02. Passing an RGB image with `COLOR_BGR2GRAY` silently swaps the red and blue
  weights.
* Most OpenCV functions expect `uint8` (0–255) or `float32`. Arithmetic on `uint8` arrays wraps
  around (250 + 10 = 4), so convert with `.astype(np.float32)` before doing maths.
* A slice such as `bgr[y:y+h, x:x+w]` is a **view**: writing to it changes the original image.
  Use `.copy()` when you need an independent crop.
* `cv2.imread` returns `None` (no exception) when the file is missing.

## Worked example
A pure blue pixel in BGR is `[255, 0, 0]`. Converted to RGB it becomes `[0, 0, 255]`, and to grey
round(0.114 × 255) = 29. The rectangle with top-left corner x = 4, y = 1, width 3 and height 2 is
`image[1:3, 4:7]`.

## Common mistakes
* Showing a BGR image with matplotlib and getting blue faces.
* Indexing `image[x, y]`.
* Adding brightness to a `uint8` image without clipping and getting dark wrap-around pixels.
* Forgetting to check `cv2.imread`'s result for `None`.

## Why this matters
Every later step — thresholds, edges, contours, CNN inputs — starts from a correctly ordered,
correctly typed array.

## References

- [Color conversions (OpenCV 4.13)](https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html) — OpenCV team (`S115`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
