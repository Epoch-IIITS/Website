# Flips, Rotations and Affine Warps

## Learning outcomes

After this lesson you can:

- Flip and rotate images by multiples of 90° with cv2.flip and cv2.rotate
- Rotate about the centre with getRotationMatrix2D and warpAffine
- Translate an image with a 2×3 affine matrix

## Intuition
Flips and quarter turns just rearrange pixels. Arbitrary rotations, shifts and scalings move
pixels to positions between grid points, so the new image must be **resampled**. OpenCV describes
all of these with one 2×3 **affine** matrix and one function, `warpAffine`.

## Precise explanation
```python
cv2.flip(img, 1)                          # 1: left-right, 0: up-down, -1: both
cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)  # also ROTATE_180, ROTATE_90_COUNTERCLOCKWISE
M = cv2.getRotationMatrix2D(center=(cx, cy), angle=30, scale=1.0)
out = cv2.warpAffine(img, M, (width, height))           # note: size is (width, height)
T = np.float32([[1, 0, dx], [0, 1, dy]])                # shift right by dx, down by dy
```

* An affine matrix maps a point (x, y) to (a·x + b·y + c, d·x + e·y + f): the left 2×2 block
  rotates/scales, the last column translates.
* Positive angles in `getRotationMatrix2D` rotate **counter-clockwise** on screen (the y axis points
  down). For the exact centre of an image use ((w − 1)/2, (h − 1)/2).
* Pixels that come from outside the source are filled with `borderValue` (0 by default).
* `cv2.ROTATE_90_CLOCKWISE` equals `np.rot90(img, -1)`; `cv2.flip(img, 1)` equals `img[:, ::-1]`.

## Worked example
Rotating a 5×5 image by 90° about (2, 2) gives exactly `np.rot90(img, 1)` (counter-clockwise).
Translating by dx = 2 moves column 0 to column 2 and fills columns 0–1 with zeros.

## What the library does inside
For every output pixel, `warpAffine` applies the inverse matrix to find where it came from and
interpolates there — bilinear by default, as in CV-19. Your CV-05 (the
optional deep dive after this step) does the exact quarter-turn rearrangements with NumPy.

## Common mistakes
* Passing `(height, width)` as the output size.
* Using the centre (w/2, h/2), which is half a pixel off for exact quarter turns.
* Expecting clockwise rotation from a positive angle.

## Why this matters
Augmentation (random flips, small rotations and shifts) and document straightening (the
document-scanner project idea) are built from these transforms.

## References

- [Geometric Transformations of Images (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) — OpenCV team (`S116`)
- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
