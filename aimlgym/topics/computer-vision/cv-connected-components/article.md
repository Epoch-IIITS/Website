# Connected Components with OpenCV

## Learning outcomes

After this lesson you can:

- Label blobs with cv2.connectedComponentsWithStats
- Read each component's area, bounding box and centroid from the stats table
- Compare 4- and 8-connectivity and filter small components

## Intuition
Counting objects in a mask means grouping touching foreground pixels into blobs and numbering them.
Unlike contours, connected components count every **pixel**, so areas are exact, and each pixel gets
the label of its blob.

## Precise explanation
```python
n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
```

* `n` counts the components **including the background** (label 0).
* `labels` is an int32 image: 0 for background, 1 … n − 1 for components.
* `stats[i]` is `[x, y, width, height, area]` (use `cv2.CC_STAT_AREA` etc. as indices); `area` is
  the pixel count.
* `centroids[i]` is the (x, y) mean position of the component's pixels.
* `connectivity=4` joins pixels that share an edge; `8` also joins diagonal neighbours. Two pixels
  touching only at a corner are one object with 8-connectivity and two with 4.

## Worked example
A 5 × 8 rectangle (40 pixels) and a 4 × 4 square (16 pixels) give n = 3, areas [40, 16] and
centroids (7.5, 7.0) and (15.5, 15.5). Removing components below 20 pixels leaves one object.

## What the library does inside
The flood fill of CV-26 (the optional deep dive after this step), done in two
fast raster passes with union–find.

## Common mistakes
* Forgetting that label 0 / `stats[0]` is the background.
* Counting noise speckles as objects — filter by area.
* Using 4-connectivity for thin diagonal structures and splitting them.

## Why this matters
Counting cells, coins, defects or parked cars usually ends with connected components; the
object-counter project idea after this step combines them with thresholding and NMS.

## References

- [Structural Analysis and Shape Descriptors (OpenCV 4.13)](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) — OpenCV team (`S121`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
