# Resizing with cv2.resize

## Learning outcomes

After this lesson you can:

- Resize images with cv2.resize and the (width, height) size convention
- Choose nearest, linear, cubic or area interpolation for the task
- Downscale without aliasing using INTER_AREA

## Intuition
Models want fixed input sizes, screens want thumbnails, and big photos are slow. Resizing computes
new pixels from old ones. Enlarging must invent values between pixels; shrinking must combine many
pixels into one without creating jagged patterns.

## Precise explanation
```python
small = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)    # size is (W, H)!
big = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
```

| Method | Use for |
|---|---|
| `INTER_NEAREST` | label masks and class maps (never invents new values) |
| `INTER_LINEAR` (default) | general enlarging, fast |
| `INTER_CUBIC` | higher-quality enlarging, slower, may overshoot |
| `INTER_AREA` | **shrinking** — averages the pixels each output pixel covers |

* Shrinking with nearest or linear interpolation skips pixels and causes aliasing (moiré on fine
  patterns); `INTER_AREA` averages instead. Halving with it averages each 2×2 block.
* For masks, any interpolation other than nearest creates in-between labels such as 127.

## Worked example
Halving [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]] with `INTER_AREA` gives the
block means [[2.5, 4.5], [10.5, 12.5]], rounded to uint8 as [[3, 5], [11, 13]].

## What the library does inside
`INTER_LINEAR` is the bilinear interpolation you implement in CV-19 (the optional
deep dive after this step), with OpenCV's half-pixel alignment of the pixel grids.

## Common mistakes
* Passing `(height, width)`.
* Resizing segmentation masks with linear interpolation.
* Shrinking photos with `INTER_NEAREST` and getting jagged or flickering results.

## Why this matters
Every CNN pipeline resizes its inputs; choosing the interpolation correctly keeps labels valid and
images free of artefacts.

## References

- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
