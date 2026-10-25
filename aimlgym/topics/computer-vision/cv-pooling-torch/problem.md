# CV-13 · Pooling with nn.MaxPool2d and nn.AvgPool2d

**Topic:** Computer Vision · **Difficulty:** intermediate · **Allowed packages:** torch

**Builds on:** CV-11 Edges with Sobel and Canny, DL-24 1-D Convolution with nn.Conv1d

Read the lesson first: [article.md](article.md)

## Task

1. `pool(x, kind, kernel_size, stride=None, padding=0)` applies `nn.MaxPool2d` (`kind="max"`) or
   `nn.AvgPool2d` (`kind="avg"`) to a 4-D float tensor (convert with `torch.as_tensor(..., dtype=torch.float32)`).
   Raise `ValueError` for another kind or a tensor that is not 4-D.
2. `pooled_size(n, kernel_size, stride=None, padding=0)` returns ⌊(n + 2·padding − kernel_size)/stride⌋ + 1,
   with `stride` defaulting to `kernel_size`.

## Hints

<details><summary>Hint 1</summary>

Choose the class with a dict: `{"max": nn.MaxPool2d, "avg": nn.AvgPool2d}`.

</details>

<details><summary>Hint 2</summary>

`layer = cls(kernel_size, stride=stride, padding=padding)`; stride=None means stride = kernel size.

</details>

<details><summary>Hint 3</summary>

`(n + 2 * padding - kernel_size) // stride + 1` after `stride = stride or kernel_size`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_max_example` | Use nn.MaxPool2d(kernel_size, stride=stride, padding=padding). |
| `test_avg_example` | Use nn.AvgPool2d for kind 'avg'. |
| `test_sizes` | The output size is (n + 2p - k) // s + 1 with s defaulting to k. |
| `test_invalid` | Reject unknown kinds and tensors that are not 4-D. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Both pooling layers take the same window arguments, so one dictionary selects the class. The size
formula is the same as for convolution, with the stride defaulting to the kernel size.

## References

- [torch.nn.MaxPool2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html) — PyTorch (`S123`)
- [Training a Classifier (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html) — PyTorch (`S124`)
