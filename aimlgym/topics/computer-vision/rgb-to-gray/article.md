# Images as Arrays and Grayscale Conversion

## Learning outcomes

After this lesson you can:

- Represent colour images as (H, W, 3) arrays
- Convert to luminance with weighted channels
- Convert safely to uint8 with rounding and clipping

## Intuition
A colour image is a grid of pixels, each with red, green and blue intensities. Our eyes are most
sensitive to green and least to blue, so a perceptually sensible grey level weights green most.

## Precise explanation
* Colour image: array `(H, W, 3)`, usually `uint8` in 0..255 (RGB order here; OpenCV loads BGR).
* Grayscale: `(H, W)`.
* ITU-R BT.601 luma weights (used by OpenCV's `cvtColor` RGB→GRAY):
  $Y = 0.299R + 0.587G + 0.114B$. With broadcasting: `img @ np.array([0.299, 0.587, 0.114])`.
* Arithmetic on `uint8` wraps around (250 + 10 = 4). Convert to float first; convert back with
  rounding and clipping to [0, 255].

## Worked example
Pure red (255, 0, 0) → 76.245 → 76; pure green → 149.685 → 150; white → 255.

## Common mistakes
* Averaging channels equally (looks wrong: blue appears too bright).
* BGR/RGB confusion with OpenCV.
* `astype(np.uint8)` without rounding/clipping (truncation and wrap-around).

## Why this matters
Many classical algorithms (edges, thresholding) work on single-channel images; dtype handling
prevents silent overflow bugs.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
