# Image Quality: MSE and PSNR

## Learning outcomes

After this lesson you can:

- Compute MSE between images without uint8 overflow
- Compute PSNR with cv2.PSNR and from the formula
- Interpret PSNR values for compression and denoising

## Intuition
How close is a compressed or denoised image to the original? The mean squared error averages
the squared pixel differences. PSNR (peak signal-to-noise ratio) puts that error on a logarithmic
scale relative to the largest possible pixel value, in decibels: higher is better.

## Precise explanation
$$\text{MSE} = \frac{1}{N}\sum (I - K)^2,\qquad \text{PSNR} = 10\log_{10}\frac{255^2}{\text{MSE}}\ \text{dB}$$

```python
cv2.PSNR(reference, distorted)        # uint8 images, peak 255
```

* Compute differences in floating point: `reference - distorted` on `uint8` arrays wraps around
  (3 − 5 = 254).
* Identical images have MSE 0 and infinite PSNR; `cv2.PSNR` instead returns a large finite value
  (about 361 dB), so handle MSE = 0 yourself.
* Rough guide for 8-bit images: above 40 dB differences are hard to see; 30–40 dB is good
  compression; below 20 dB the distortion is obvious. PSNR does not model human perception well —
  SSIM is a common complement.

## Worked example
If every pixel differs by exactly 1, MSE = 1 and PSNR = 10·log₁₀(65025) = 48.13 dB. Uniform noise
of ±10 gives about 28 dB.

## What the library does inside
The formula you implement by hand in CV-17 (the optional deep dive after this step), computed in
double precision over all channels.

## Common mistakes
* Subtracting `uint8` arrays directly.
* Comparing images of different sizes or channel orders.
* Reporting `cv2.PSNR`'s 361 dB for identical images as a meaningful number.

## Why this matters
PSNR is the standard sanity metric for compression, super-resolution and denoising models, and a
quick way to check that an image pipeline did not change pixels it should not have.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Geometric Image Transformations reference (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html) — OpenCV team (`S122`)
