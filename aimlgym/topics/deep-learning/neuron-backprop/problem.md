# DL-10 · Backprop Through One Neuron

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** DL-08 A Tiny Autograd Engine

Read the lesson first: [article.md](article.md)

## Task

Write `neuron_forward_backward(x, y, w, b)` for one example (`x`, `w` 1-D arrays, `y` in {0, 1})
returning a dict with keys `z, p, loss, dL_dp, dp_dz, dL_dz, grad_w, grad_b` (floats, `grad_w`
an array). Clip `p` to `[1e-12, 1 - 1e-12]` only when computing `loss` and `dL_dp`.

**Example**
```python
r = neuron_forward_backward(np.array([1., 2.]), 1, np.array([0.5, -0.25]), 0.0)
r["loss"], r["dL_dz"], r["grad_w"]    # (0.6931..., -0.5, array([-0.5, -1. ]))
```

## Hints

<details><summary>Hint 1</summary>

`z = float(w @ x + b)`; `p = 1 / (1 + np.exp(-z))`.

</details>

<details><summary>Hint 2</summary>

`dL_dp = -y / pc + (1 - y) / (1 - pc)` with clipped `pc`; `dp_dz = p * (1 - p)`.

</details>

<details><summary>Hint 3</summary>

`dL_dz = dL_dp * dp_dz`; `grad_w = dL_dz * x`; `grad_b = dL_dz`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | dL/dp = −y/p + (1−y)/(1−p); dp/dz = p(1−p). |
| `test_p_minus_y` | Multiply the two local derivatives; the product should equal p − y. |
| `test_numeric_w` | grad_w = dL/dz · x. |
| `test_large_z_stable` | Use a stable sigmoid and clip p for the log. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The forward pass computes and stores z and p. The backward pass multiplies local derivatives
from the loss back to the parameters, exactly following the graph. The product dL/dp · dp/dz
simplifies to p − y, which the tests check.

## References

- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — free online book (author not stated on landing page) (`S014`)
