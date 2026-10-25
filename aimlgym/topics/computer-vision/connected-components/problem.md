# CV-26 · Connected Components Labeling by Hand

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** CV-07 Binary Thresholding

Read the lesson first: [article.md](article.md)

## Task

Write `label_components(mask, connectivity=4)` for a 2-D boolean array returning
`(labels, sizes)`: `labels` int array (0 = background, components 1..K in raster order of their first
pixel) and `sizes` a list of K pixel counts. `connectivity` in {4, 8}, else `ValueError`.

**Example**
```python
m = np.array([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1]], bool)
labels, sizes = label_components(m)
labels   # [[1,1,0,0],[0,1,0,2],[0,0,0,2]]
sizes    # [3, 2]
label_components(np.array([[1, 0], [0, 1]], bool), 8)[1]   # [2]
```

## Hints

<details><summary>Hint 1</summary>

Offsets: 4 → `[(-1,0),(1,0),(0,-1),(0,1)]`; 8 adds the four diagonals.

</details>

<details><summary>Hint 2</summary>

Raster scan; when `mask[r, c] and labels[r, c] == 0`, assign a new label and BFS.

</details>

<details><summary>Hint 3</summary>

Set the label when *pushing* a pixel onto the queue to avoid duplicates.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_diagonal` | 8-connectivity includes diagonal neighbours; 4 does not. |
| `test_raster_order` | Assign labels in order of first pixel in a row-by-row scan. |
| `test_large_no_recursion` | Use an explicit queue (deque) instead of recursion. |
| `test_example` | Label pixels when pushing them so each is counted once. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A raster scan finds the first pixel of each new component, which fixes the label order. BFS with a
deque floods the component, labelling pixels as they are enqueued so none is visited twice, and
counts its size.

## References

- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
