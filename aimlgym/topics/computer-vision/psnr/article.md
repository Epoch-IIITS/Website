# Image Quality: MSE and PSNR

## Learning outcomes

After this lesson you can:

- Compute image MSE without uint8 overflow
- Compute PSNR in decibels
- Interpret PSNR values

## Intuition
How close is a compressed or denoised image to the original? Average the squared pixel differences
(MSE). PSNR rescales this to a logarithmic decibel scale where higher is better.

## Precise explanation
$$\text{MSE} = \frac1N\sum (a_i - b_i)^2,\qquad \text{PSNR} = 10\log_{10}\frac{\text{MAX}^2}{\text{MSE}}\ \text{dB},$$
with MAX = 255 for 8-bit images (1.0 for images scaled to [0, 1]). Identical images → MSE 0 →
PSNR = ∞. Rough guide for 8-bit images: 30–50 dB is typical for good compression; each halving of the
RMSE adds ≈ 6 dB.
**Overflow trap:** `a - b` on `uint8` arrays wraps around (3 − 5 = 254). Convert to float first.

## Worked example
a = [[0, 0]], b = [[0, 255]]: MSE = 255²/2 = 32512.5 → PSNR = 10·log10(2) ≈ 3.01 dB.

## Common mistakes
* Computing on uint8.
* Wrong MAX for float images.
* Treating PSNR as perceptual quality (SSIM and learned metrics model perception better).

## Why this matters
PSNR is the standard sanity metric for denoising, super-resolution and compression.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
