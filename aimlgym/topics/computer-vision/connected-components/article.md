# Connected-Component Labelling

## Learning outcomes

After this lesson you can:

- Label connected foreground regions with BFS
- Compare 4- and 8-connectivity
- Report component sizes deterministically

## Intuition
After thresholding (CV-07) you have blobs of foreground pixels. Which pixels belong to the same blob?
Treat pixels as graph nodes connected to their neighbours and find connected groups.

## Precise explanation
* **4-connectivity:** neighbours up, down, left, right. **8-connectivity:** also diagonals.
* Algorithm: scan pixels in raster order (row by row, left to right). When an unlabelled foreground
  pixel is found, start a new label and flood-fill its component with breadth-first search (BFS)
  using a queue (`collections.deque`).
* Labels 1, 2, 3, … in order of the first pixel encountered; background stays 0.
* Return also the size (pixel count) of each component.
BFS visits each pixel once: $O(HW)$. Recursion (DFS) can exceed Python's recursion limit on large
blobs, so use an explicit queue.

## Worked example
```
1 1 0 0        1 1 0 0
0 1 0 1   →    0 1 0 2      (4-connectivity: 2 components, sizes [3, 2])
0 0 0 1        0 0 0 2
```
Diagonal pixels (0,0) and (1,1) would also join under 8-connectivity.

## Common mistakes
* Marking pixels visited only when popped (duplicates in the queue).
* Index errors at the image border.
* Recursive flood fill on large images.

## Why this matters
Component labelling counts objects (cells, characters), filters small noise blobs, and is a direct
application of graph search, which reappears in agent planning (AG-11).

## Library implementation

`scipy.ndimage.label(mask, structure=...)` labels connected components with optimised code; a
3×3 cross structure is 4-connectivity and `np.ones((3, 3))` is 8-connectivity. Label numbers are
assigned in scan order of each component's first pixel, so they match yours. The comparison runs
when SciPy is installed.

## References

- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
