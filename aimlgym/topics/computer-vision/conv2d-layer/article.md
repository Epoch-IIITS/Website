# A Convolution Layer with Channels

## Learning outcomes

After this lesson you can:

- Apply a bank of filters to a multi-channel input (C_in → C_out)
- Compute output sizes from kernel size, padding and stride
- Count a convolution layer's parameters
- Compare a loop implementation with PyTorch's conv2d

## Intuition
CV-10 slid one kernel over one greyscale image. A CNN layer does this with *many*
kernels over *many* input channels: each output channel has its own small 3-D filter that looks
at every input channel at once and sums the results. Early layers learn edge and colour
detectors; later layers combine them.

## Precise explanation
Shapes (channels-first, as in PyTorch, see CV-01):
* input `x`: `(C_in, H, W)`; weights: `(C_out, C_in, k, k)`; bias: `(C_out,)`;
* output: `(C_out, H_out, W_out)` with
  $$H_{out} = \left\lfloor \frac{H + 2p - k}{s} \right\rfloor + 1$$
  for padding $p$ (zeros added on each side) and stride $s$ (same for $W$).

$$\text{out}[o, i, j] = b_o + \sum_{c=0}^{C_{in}-1}\sum_{u=0}^{k-1}\sum_{v=0}^{k-1}
  w[o, c, u, v]\; x_p[c,\; i s + u,\; j s + v]$$
where $x_p$ is the zero-padded input. This is **cross-correlation** (the kernel is not flipped),
which is what deep-learning libraries call convolution.

* Parameters: $C_{out}\,(C_{in} k^2 + 1)$ — independent of the image size, unlike a dense layer.
* A 1×1 convolution mixes channels without looking at neighbours.

## Worked example
Input `(2, 4, 4)`, 3 filters of size 3, padding 1, stride 2: $H_{out} = \lfloor (4 + 2 - 3)/2\rfloor + 1 = 2$,
so the output is `(3, 2, 2)`; the layer has $3(2\cdot 9 + 1) = 57$ parameters.

## Common mistakes
* Summing only over the kernel window and forgetting to sum over input channels.
* Using `H - k + 1` when there is padding or stride.
* Flipping the kernel (that is mathematical convolution; CNN layers do not flip).
* Mixing up `(C_out, C_in, k, k)` order.

## Why this matters
Stacks of convolution, ReLU and pooling (CV-14) form the CNNs used for image
classification and detection.

## Library implementation

`torch.nn.functional.conv2d(x, weight, bias, stride, padding)` (or the layer `torch.nn.Conv2d`)
computes exactly this, batched over a leading `N` axis and using fast algorithms instead of
loops. SciPy's `scipy.signal.correlate` handles a single channel. The tests compare your
function with PyTorch when it is installed.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)
