# Edges with Sobel and Canny

## Learning outcomes

After this lesson you can:

- Compute image gradients with cv2.Sobel in a float output type
- Detect thin edges with Gaussian blur and cv2.Canny
- Explain Canny's hysteresis thresholds

## Intuition
An edge is where brightness changes quickly. The Sobel filter measures that change in x and y;
the gradient magnitude is large on edges. Canny goes further: it keeps only the thin ridge of
strongest change and links edge pieces together, giving clean one-pixel-wide outlines.

## Precise explanation
```python
gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)     # d/dx — responds to vertical edges
gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)     # d/dy — horizontal edges
magnitude = np.hypot(gx, gy)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)                 # uint8 mask of 0 and 255
```

* Use a float output depth (`cv2.CV_64F`): gradients are negative on one side of an edge, and a
  `uint8` output would clip them to 0.
* Canny steps: smooth, Sobel gradients, **non-maximum suppression** (keep a pixel only if it is the
  largest along the gradient direction), then **hysteresis**: pixels above `high` are edges, pixels
  between `low` and `high` are kept only if connected to a strong edge.
* A ratio high:low of about 2:1 to 3:1 is typical. Blurring first removes noise edges.

## Worked example
A white square on black: gx is large on the left and right sides (positive on one, negative on the
other) and 0 on the top and bottom; Canny returns a closed one-pixel outline around the square.

## What the library does inside
`cv2.Sobel` is the convolution with the 3×3 kernels in CV-12 (the optional deep dive
after this step); Canny adds the suppression and hysteresis passes.

## Common mistakes
* `cv2.Sobel(gray, -1, 1, 0)`: keeps uint8 and loses negative gradients.
* Running Canny on a noisy, unblurred photo.
* Setting `low` above `high`.

## Why this matters
Edges feed contour finding, lane detection and document scanning, and they are what the first layer
of a trained CNN tends to learn.

## References

- [Canny Edge Detection (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html) — OpenCV team (`S119`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
