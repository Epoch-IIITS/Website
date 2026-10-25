# CV-25 · Connected Components with OpenCV

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-24 Non-Maximum Suppression

Read the lesson first: [article.md](article.md)

## Task

Write `label_objects(mask, connectivity=8, min_area=1)` returning
`{"count": int, "areas": list[int], "boxes": list[tuple], "centroids": list[tuple]}` for the
non-background components whose area is at least `min_area`, in label order.

* Use `cv2.connectedComponentsWithStats(mask, connectivity=connectivity)`.
* `boxes` are `(x, y, w, h)` int tuples, `centroids` `(cx, cy)` float tuples.
* Raise `ValueError` unless `mask` is 2-D `uint8` and `connectivity` is 4 or 8.

## Hints

<details><summary>Hint 1</summary>

Validate the mask and connectivity first.

</details>

<details><summary>Hint 2</summary>

`n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=connectivity)`.

</details>

<details><summary>Hint 3</summary>

Loop over `range(1, n)`: `x, y, w, h, area = stats[i]` and keep those with `area >= min_area`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_counts_and_areas` | Skip label 0, the background, and report stats areas in label order. |
| `test_min_area` | Keep only components with area >= min_area. |
| `test_connectivity` | Pass connectivity through to connectedComponentsWithStats. |
| `test_types_and_empty` | Convert stats to ints and centroids to floats. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

OpenCV labels every pixel and returns one stats row and centroid per label. Skipping label 0
removes the background; the area filter drops speckles; the remaining rows are converted to plain
ints and floats.

## References

- [Structural Analysis and Shape Descriptors (OpenCV 4.13)](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) — OpenCV team (`S121`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
