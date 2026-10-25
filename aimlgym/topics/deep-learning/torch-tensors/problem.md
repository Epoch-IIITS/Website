# DL-05 · PyTorch Tensors

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy, torch

**Builds on:** DL-04 Dense Layer Forward Pass

Read the lesson first: [article.md](article.md)

## Task

Write `dense_relu(x, W, b)` returning the **tensor** `relu(x @ W + b)` with dtype `torch.float32`.

* `x` (shape `(batch, n_in)`), `W` (`(n_in, n_out)`) and `b` (`(n_out,)`) may be lists, NumPy
  arrays or tensors; convert each with `torch.as_tensor(..., dtype=torch.float32)`.
* Raise `ValueError` if `x` is not 2-D, or the shapes do not fit together.
* Do not modify the inputs.

**Example**
```python
dense_relu([[1, -2]], [[1, 0, 2], [3, 1, -1]], [0.5, 0, 0])   # tensor([[0., 0., 4.]])
```

## Hints

<details><summary>Hint 1</summary>

`x = torch.as_tensor(x, dtype=torch.float32)` and the same for W and b.

</details>

<details><summary>Hint 2</summary>

Check `x.ndim == 2`, `x.shape[1] == W.shape[0]` and `b.shape == (W.shape[1],)`.

</details>

<details><summary>Hint 3</summary>

`torch.relu(x @ W + b)` broadcasts the bias over the batch.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Compute torch.relu(x @ W + b) and return the tensor itself. |
| `test_float32_from_float64` | Convert every input with dtype=torch.float32. |
| `test_inputs_unchanged` | Do not use in-place operations on the inputs. |
| `test_shape_errors` | Check that x is 2-D and that W and b have matching sizes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`torch.as_tensor` converts lists and arrays to float32 tensors (without copying when no conversion
is needed). The shape checks give a clear error before the matrix product; the bias broadcasts
over the batch exactly as it does in NumPy, and ReLU clips negatives to zero.

## References

- [Tensors (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — PyTorch (`S103`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
