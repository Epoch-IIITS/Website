# CV-20 · Contours and Bounding Boxes

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-18 Resizing with cv2.resize

Read the lesson first: [article.md](article.md)

## Task

Write `find_objects(mask, min_area=0)` returning one dict per outer contour,
`{"x", "y", "w", "h", "area", "centroid"}`, sorted by `(y, x)`.

* Use `cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
* `x, y, w, h` are ints from `cv2.boundingRect`; `area` is `float(cv2.contourArea(c))`;
  `centroid` is `(cx, cy)` from `cv2.moments`, or the bounding-box centre `(x + (w - 1) / 2, y + (h - 1) / 2)`
  when `m00` is 0.
* Keep only contours whose `area >= min_area`.
* Raise `ValueError` unless `mask` is a 2-D `uint8` array.

## Hints

<details><summary>Hint 1</summary>

Validate the mask; then `contours, _ = cv2.findContours(...)`.

</details>

<details><summary>Hint 2</summary>

For each contour read `boundingRect`, `contourArea` and `moments`; guard `m00 == 0`.

</details>

<details><summary>Hint 3</summary>

Filter by area and sort with `key=lambda o: (o["y"], o["x"])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_boxes` | Use RETR_EXTERNAL and boundingRect, and sort by (y, x). |
| `test_area_and_centroid` | area is cv2.contourArea; the centroid is (m10/m00, m01/m00). |
| `test_holes_ignored` | RETR_EXTERNAL returns only outer boundaries. |
| `test_empty_and_single_pixel` | When m00 is 0 use the bounding-box centre. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`RETR_EXTERNAL` gives one contour per separate blob; bounding box, polygon area and moments
describe each one. Degenerate contours (a line or a single pixel) have zero area, so their centre
falls back to the middle of the bounding box. Sorting gives a stable, top-to-bottom order.

## References

- [Contours: Getting Started (OpenCV 4.13)](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html) — OpenCV team (`S120`)
- [Structural Analysis and Shape Descriptors (OpenCV 4.13)](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) — OpenCV team (`S121`)
