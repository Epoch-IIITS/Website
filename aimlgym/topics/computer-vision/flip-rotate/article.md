# Flips and 90° Rotations

## Learning outcomes

After this lesson you can:

- Flip images with negative-step slicing
- Rotate by 90° using transpose + flip
- Use flips/rotations as data augmentation

## Intuition
A mirrored photo of a cat is still a cat. Flips and rotations create extra training examples for
free (**data augmentation**) and are pure index rearrangements — no interpolation needed.

## Precise explanation
For an image with rows (axis 0) and columns (axis 1):
* Horizontal flip (left↔right): `img[:, ::-1]`.
* Vertical flip (top↔bottom): `img[::-1, :]`.
* Rotate 90° **clockwise**: transpose rows/columns, then flip horizontally:
  `img.transpose(1, 0, *rest)[:, ::-1]`. Applying it k times rotates by 90k°; k mod 4 matters.
* `np.rot90(img, k)` rotates **counter-clockwise** — a classic source of confusion.
These work for `(H, W)` and `(H, W, C)` (channels must stay last).

## Worked example
```
[[1, 2, 3],        cw        [[4, 1],
 [4, 5, 6]]      ------>      [5, 2],
                              [6, 3]]
```

## Common mistakes
* Using `np.rot90` and rotating the wrong way.
* Transposing a colour image with `.T` (reverses all three axes, moving channels first).
* Flipping digits/text where orientation changes meaning (augmentation must preserve labels).

## Why this matters
Augmentation pipelines in every CV training script use these operations.

## References

- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
