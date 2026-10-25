# Contours and Bounding Boxes

## Learning outcomes

After this lesson you can:

- Find object outlines in a binary mask with cv2.findContours
- Measure each object's bounding box, area and centroid
- Filter small objects and ignore holes with RETR_EXTERNAL

## Intuition
After thresholding, each white blob is an object. A **contour** is the list of points along a
blob's boundary. From it you get a bounding box (where is it?), an area (how big?) and a centroid
(where is its centre of mass?) — enough to count, locate and filter objects.

## Precise explanation
```python
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)       # top-left corner and size, in pixels
    area = cv2.contourArea(c)               # area of the polygon through the boundary pixels
    m = cv2.moments(c)
    cx, cy = m["m10"] / m["m00"], m["m01"] / m["m00"]   # centroid (needs m00 > 0)
```

* The mask must be single-channel `uint8`; any non-zero pixel is foreground.
* `RETR_EXTERNAL` returns only outer boundaries, so holes inside objects are ignored;
  `RETR_TREE` returns the full nesting.
* `CHAIN_APPROX_SIMPLE` stores only the corners of straight runs (a rectangle has 4 points).
* `contourArea` measures the polygon through boundary **pixel centres**, so a filled w × h rectangle
  has area (w − 1)(h − 1), not w·h. For pixel counts use connected components (later in this topic).
* In OpenCV 4.x `findContours` returns two values.

## Worked example
A filled rectangle covering columns 4–11 and rows 5–9 gives `boundingRect` (4, 5, 8, 5),
`contourArea` 7 × 4 = 28 and centroid (7.5, 7.0).

## Common mistakes
* Passing a greyscale photo instead of a binary mask.
* Expecting `contourArea` to equal the number of pixels.
* Dividing by `m00` for a degenerate contour (a single pixel or line) without checking for zero.

## Why this matters
Contours locate documents in photos, count parts on a conveyor belt and produce the boxes that
detection post-processing (IoU and NMS, later in this topic) works with. The document-scanner
project idea after this step is built on them.

## References

- [Contours: Getting Started (OpenCV 4.13)](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html) — OpenCV team (`S120`)
- [Structural Analysis and Shape Descriptors (OpenCV 4.13)](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) — OpenCV team (`S121`)
