# CV-22 · Data Augmentation

**Topic:** Computer Vision · **Difficulty:** advanced · **Allowed packages:** numpy, opencv-python-headless

**Builds on:** CV-21 A Small CNN in PyTorch

Read the lesson first: [article.md](article.md)

## Task

1. `augment(image, rng, max_shift=2)` for a 2-D or 3-D `uint8` image, using the NumPy generator
   `rng` in this order:
   * if `rng.random() < 0.5`, flip horizontally with `cv2.flip(image, 1)`;
   * `dx, dy = rng.integers(-max_shift, max_shift + 1, size=2)`, then translate with `warpAffine`
     (uncovered pixels 0);
   * multiply by `rng.uniform(0.8, 1.2)` in float32, clip to [0, 255] and convert back to uint8.
   Return an image with the same shape and dtype. Raise `ValueError` for non-uint8 input.
2. `augment_batch(images, seed=0, max_shift=2)` augments each image in order with one generator
   `np.random.default_rng(seed)` and returns a NumPy array of the same shape.

## Hints

<details><summary>Hint 1</summary>

Keep the order of random draws exactly as stated, so results are reproducible.

</details>

<details><summary>Hint 2</summary>

`M = np.float32([[1, 0, dx], [0, 1, dy]])`; `cv2.warpAffine(image, M, (w, h))`.

</details>

<details><summary>Hint 3</summary>

`np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_reproducible` | Use one np.random.default_rng(seed) for the whole batch and draw in the stated order. |
| `test_label_preserved` | Use small shifts and horizontal flips only, so a horizontal bar stays horizontal. |
| `test_values_clipped` | Scale brightness in float32 and clip to [0, 255] before converting to uint8. |
| `test_zero_shift_and_flip_frequency` | Flip when rng.random() < 0.5. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each augmentation draws its random choices from the generator in a fixed order, so the same seed
always produces the same batch. Flip and shift rearrange pixels; the brightness change is done in
float and clipped so no value wraps around.

## References

- [Transforming and augmenting images (torchvision)](https://docs.pytorch.org/vision/stable/transforms.html) — PyTorch (`S125`)
- [Geometric Transformations of Images (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) — OpenCV team (`S116`)
