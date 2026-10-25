# Pooling with nn.MaxPool2d and nn.AvgPool2d

## Learning outcomes

After this lesson you can:

- Apply max and average pooling to (batch, channels, height, width) tensors
- Compute pooled output sizes from kernel, stride and padding
- Explain where max pooling sends its gradient

## Intuition
Pooling shrinks a feature map by summarising each small window: max pooling keeps the strongest
response ("is the feature present anywhere here?"), average pooling keeps the mean. Halving height
and width quarters the computation of later layers and makes small shifts matter less.

## Precise explanation
```python
from torch import nn
nn.MaxPool2d(kernel_size=2)(x)            # x: (B, C, H, W) → (B, C, H/2, W/2); stride defaults to kernel_size
nn.AvgPool2d(kernel_size=3, stride=1, padding=1)(x)    # same size, smoothed
```

* Output size per spatial dimension: ⌊(n + 2p − k)/s⌋ + 1.
* Pooling has no learnable parameters and acts on each channel separately.
* Max pooling passes the gradient back **only to the position of the maximum** in each window;
  average pooling spreads it equally, 1/k² per position.
* Padding for max pooling uses −∞ (padded values never win); average pooling counts padded zeros
  by default (`count_include_pad=True`).

## Worked example
For the 4×4 map [[1, 3, 2, 0], [4, 2, 1, 1], [0, 1, 5, 6], [2, 2, 7, 8]], 2×2 max pooling gives
[[4, 2], [2, 8]] and average pooling [[2.5, 1.0], [1.25, 6.5]].

## What the library does inside
The window loops of CV-14 (the optional deep dive after this step), vectorised over the
batch and channels.

## Common mistakes
* Passing an (H, W) tensor: add batch and channel dimensions with `x[None, None]`.
* Assuming stride 1 by default (it equals the kernel size).
* Expecting average pooling to ignore padding.

## Why this matters
The small CNN later in this topic alternates convolutions and max pooling — the classic recipe from
LeNet to VGG.

## References

- [torch.nn.MaxPool2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html) — PyTorch (`S123`)
- [Training a Classifier (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) — PyTorch (`S124`)
