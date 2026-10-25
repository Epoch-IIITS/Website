# Pooling

## Learning outcomes

After this lesson you can:

- Downsample with max and average pooling
- Compute pooled output sizes
- Vectorise non-overlapping pooling with reshape

## Intuition
Pooling summarises each small window by its maximum (or average), shrinking feature maps while
keeping the strongest responses — a bit of translation tolerance for free.

## Precise explanation
For window size $k$ and stride $s$ (default $s = k$, non-overlapping), output size per axis is
$\lfloor (n - k)/s \rfloor + 1$ (CS231n formula with no padding). Rows/columns that don't fit a
full window are dropped.
For the non-overlapping case a reshape trick avoids loops:
```python
x[:Ho*k, :Wo*k].reshape(Ho, k, Wo, k).max(axis=(1, 3))
```
Overlapping pooling (s < k) can use `sliding_window_view` (NP-14) or a loop over output cells.

## Worked example
4×4 [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 2×2 max → [[6, 8], [14, 16]];
average → [[3.5, 5.5], [11.5, 13.5]].

## Common mistakes
* Reshaping `(H, W)` to `(Ho, Wo, k, k)` directly — mixes rows and columns.
* Forgetting to crop to a multiple of k.
* Off-by-one in the output size with strides.

## Why this matters
Pooling layers appear in classic CNNs (LeNet, VGG) and global average pooling feeds classifier heads.

## Library implementation

`torch.nn.functional.max_pool2d` and `avg_pool2d` (with `kernel_size` and `stride`) implement
the same windows for batched, multi-channel tensors. The comparison runs when PyTorch is installed.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
