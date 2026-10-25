# 1-D Convolution with nn.Conv1d

## Learning outcomes

After this lesson you can:

- Use F.conv1d and nn.Conv1d with (batch, channels, length) tensors
- Compute output lengths from kernel size, stride and padding
- Recognise that deep-learning convolution is cross-correlation

## Intuition
A 1-D convolution slides a small kernel along a signal and takes a weighted sum at each position —
a learnable moving average (NP-14). With several input channels (for example x, y and
z of an accelerometer) each output channel combines all of them.

## Precise explanation
Shapes follow the convention **(batch, channels, length)**:

```python
import torch.nn.functional as F
out = F.conv1d(x, weight, bias, stride=1, padding=0)
# x: (B, C_in, L), weight: (C_out, C_in, K), bias: (C_out,), out: (B, C_out, L_out)
layer = nn.Conv1d(C_in, C_out, kernel_size=K, stride=1, padding=0)   # holds weight and bias
```

$$\text{out}[b, o, t] = \text{bias}[o] + \sum_{c}\sum_{k} \text{weight}[o, c, k]\,x[b, c, t\cdot s + k]$$
(after zero padding), and $L_{out} = \lfloor (L + 2p - K)/s \rfloor + 1$.

* The kernel is **not flipped**: this is cross-correlation, matching `np.correlate`, not
  `np.convolve`. Since the kernel is learned, the difference does not matter for training.
* `padding=K//2` keeps the length for odd K and stride 1.

## Worked example
x = [1, 2, 3, 4, 5] with kernel [1, 0, −1]: outputs are 1 − 3, 2 − 4, 3 − 5 = [−2, −2, −2]
(length 3). With padding 1 the signal becomes [0, 1, 2, 3, 4, 5, 0], giving
[0 − 2, 1 − 3, 2 − 4, 3 − 5, 4 − 0] = [−2, −2, −2, −2, 4] (length 5).

## What the library does inside
Your DL-25 (the optional deep dive after this step) loops over positions; PyTorch unfolds the
windows into a matrix and does one large matrix multiplication for all channels and batch items.

## Common mistakes
* Passing a (B, L, C) tensor (channels last) instead of (B, C, L).
* Flipping the kernel to "do a real convolution" and getting mirrored results.
* Forgetting that stride shortens the output.

## Why this matters
Conv1d models audio, sensor data and text; the 2-D version in Computer Vision works identically
with one more spatial dimension.

## References

- [torch.nn.Conv1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv1d.html) — PyTorch (`S114`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)
