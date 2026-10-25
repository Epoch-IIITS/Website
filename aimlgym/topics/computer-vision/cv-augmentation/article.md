# Data Augmentation

## Learning outcomes

After this lesson you can:

- Write label-preserving augmentations: flips, small shifts and brightness changes
- Apply augmentations reproducibly with a seeded generator
- Keep augmented images in the valid uint8 range

## Intuition
A cat is still a cat when the photo is mirrored, shifted a little or slightly darker. Showing the
network randomly transformed copies of each training image during training teaches it that these
changes do not matter, which works like having more data.

## Precise explanation
An augmentation must **preserve the label**. Typical choices for photos:

* horizontal flip with probability 0.5 (not for text or digits, where mirroring changes meaning);
* translation by a few pixels with `cv2.warpAffine` (CV-04);
* brightness scaling by a factor in [0.8, 1.2], computed in float and clipped back to [0, 255].

```python
rng = np.random.default_rng(seed)
if rng.random() < 0.5:
    image = cv2.flip(image, 1)
dx, dy = rng.integers(-2, 3, size=2)
image = cv2.warpAffine(image, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h))
image = np.clip(image.astype(np.float32) * rng.uniform(0.8, 1.2), 0, 255).astype(np.uint8)
```

* Augment **only the training data**, and freshly every epoch; evaluate on unchanged images.
* Draw all random choices from one seeded generator so a run can be reproduced.
* Libraries such as `torchvision.transforms` and Albumentations provide ready-made pipelines of
  these operations.

## Worked example
Training the small CNN of CV-21 on 60 images, then testing on images shifted to new
positions: without augmentation accuracy drops noticeably; with random shifts during training it
stays high, because the network has seen shapes in many positions.

## Common mistakes
* Augmenting the test set.
* Transforms that change the label (flipping a "b" into a "d", rotating a "6" into a "9").
* Brightness changes on uint8 arrays without float conversion and clipping.
* Using an unseeded generator, so results cannot be reproduced.

## Why this matters
Augmentation is one of the most effective regularisers for vision models and is standard in every
modern training pipeline; the shape-sorter project idea uses it.

## References

- [Transforming and augmenting images (torchvision)](https://docs.pytorch.org/vision/stable/transforms.html) — PyTorch (`S125`)
- [Geometric Transformations of Images (OpenCV 4.13)](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) — OpenCV team (`S116`)
