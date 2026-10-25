# DL-24 · 1-D Convolution with nn.Conv1d

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** DL-22 Batch Normalisation with nn.BatchNorm1d, NP-14 Moving Average with cumsum

Read the lesson first: [article.md](article.md)

## Task

Write `conv1d_layer(x, weight, bias=None, stride=1, padding=0)` returning
`F.conv1d(x, weight, bias, stride=stride, padding=padding)` as a float32 tensor.

* Accept lists, NumPy arrays or tensors; convert each with `torch.as_tensor(..., dtype=torch.float32)`.
* Raise `ValueError` if `x` is not 3-D, `weight` is not 3-D, the channel counts differ, `bias`
  (when given) does not have one value per output channel, or the padded input is shorter than
  the kernel.

**Example**
```python
conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]])              # tensor([[[-2., -2., -2.]]])
conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]], padding=1)   # tensor([[[-2., -2., -2., -2., 4.]]])
```

## Hints

<details><summary>Hint 1</summary>

Convert x and weight (and bias if given) to float32 tensors.

</details>

<details><summary>Hint 2</summary>

Check `x.ndim == 3`, `weight.ndim == 3`, `x.shape[1] == weight.shape[1]` and `x.shape[2] + 2 * padding >= weight.shape[2]`.

</details>

<details><summary>Hint 3</summary>

`F.conv1d(x, weight, bias, stride=stride, padding=padding)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Shapes are (batch, channels, length); call F.conv1d. |
| `test_not_flipped` | Do not flip the kernel: PyTorch computes cross-correlation. |
| `test_channels_stride_bias` | Pass bias, stride and padding through to F.conv1d. |
| `test_invalid` | Check dimensions, channel counts, bias length and that the kernel fits. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

After conversion and shape checks, `F.conv1d` does the sliding weighted sums for every batch item,
output channel and position at once. Padding adds zeros at both ends; stride skips positions.

## References

- [torch.nn.Conv1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv1d.html) — PyTorch (`S114`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)
