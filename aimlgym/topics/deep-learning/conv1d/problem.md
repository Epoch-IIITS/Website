# DL-25 · 1D Convolution by Hand (valid, stride)

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** DL-04 Dense Layer Forward Pass, NP-14 Moving Average with cumsum

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `conv_output_length(n, k, stride, padding)` → int using the formula; raise `ValueError` if the
  result would be < 1, `k < 1` or `stride < 1` or `padding < 0`.
* `conv1d(x, kernel, stride=1, padding=0, bias=0.0)` → float array (cross-correlation with zero
  padding).

**Examples**
```python
conv1d([1, 2, 3, 4, 5], [1, 0, -1])              # [-2., -2., -2.]
conv1d([1, 2, 3, 4, 5], [1, 0, -1], stride=2)    # [-2., -2.]
conv1d([1, 2, 3, 4, 5], [1, 0, -1], padding=1)   # [-2., -2., -2., -2., 4.]
```

## Hints

<details><summary>Hint 1</summary>

`(n + 2 * padding - k) // stride + 1`.

</details>

<details><summary>Hint 2</summary>

Pad with `np.pad(x, padding)`.

</details>

<details><summary>Hint 3</summary>

Window i starts at `i * stride`: `xp[i*stride : i*stride + k] @ kernel + bias`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_no_flip` | Don't flip the kernel; DL 'convolution' is cross-correlation. |
| `test_padding` | Pad both ends with zeros using np.pad(x, padding). |
| `test_stride` | Window i starts at i * stride. |
| `test_output_length` | n_out = floor((n + 2p − k)/s) + 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The output length comes from the formula, which also validates the configuration. After zero
padding, each output is the dot product of the kernel with the window starting at i·stride — the
cross-correlation used by deep-learning libraries.

## References

- [CS231n: Convolutional Neural Networks notes](https://cs231n.github.io/convolutional-networks/) — Stanford University CS231n (`S015`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
