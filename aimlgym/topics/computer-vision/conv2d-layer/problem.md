# CV-15 · A Convolution Layer with Channels

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d, CV-10 2D Filtering (Blur)

Read the lesson first: [article.md](article.md)

## Task

Implement with NumPy:

1. `conv_output_size(n, k, padding=0, stride=1)` → output length; raise `ValueError` if it would
   be less than 1.
2. `conv2d(x, weight, bias=None, stride=1, padding=0)` for `x` of shape `(C_in, H, W)` and
   `weight` of shape `(C_out, C_in, k, k)` (square kernels) → `(C_out, H_out, W_out)` using the
   formula above (zero padding, no kernel flip). `bias` defaults to zeros. Raise `ValueError` if
   the channel counts disagree.
3. `conv_params(c_in, c_out, k)` → number of weights plus biases.

## Hints

<details><summary>Hint 1</summary>

`(n + 2 * padding - k) // stride + 1`.

</details>

<details><summary>Hint 2</summary>

`xp = np.pad(x, ((0, 0), (padding, padding), (padding, padding)))` pads only the spatial axes.

</details>

<details><summary>Hint 3</summary>

For each output position, take `patch = xp[:, i*s:i*s+k, j*s:j*s+k]` (shape (C_in, k, k)) and compute `np.sum(weight[o] * patch) + bias[o]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_output_size` | Use `(n + 2*padding - k) // stride + 1` and reject results below 1. |
| `test_sums_over_channels` | Each output value sums over all input channels as well as the kernel window. |
| `test_matches_reference` | Pad only the spatial axes and step the window by `stride`. |
| `test_no_flip` | Do not flip the kernel; weight[u, v] multiplies the input at offset (u, v). |
| `test_params` | Each output channel has C_in*k*k weights plus one bias. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Padding is applied once to the spatial axes. For each output position the input patch has shape
`(C_in, k, k)`; contracting it with all filters at once (`tensordot` over the channel and kernel
axes) yields one value per output channel, to which the bias is added. The output size follows
the floor formula, which also rejects impossible configurations.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [torch.nn.Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) — PyTorch (`S093`)
