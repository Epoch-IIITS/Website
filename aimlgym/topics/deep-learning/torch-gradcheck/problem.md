# DL-12 · Custom Gradients and gradcheck

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** torch

**Builds on:** DL-11 Backpropagation Through a Dense Layer, DL-09 Autograd in PyTorch

Read the lesson first: [article.md](article.md)

## Task

1. Write `class Softplus(torch.autograd.Function)` with static `forward(ctx, x)` returning
   softplus(x) = log(1 + eˣ) computed stably with `torch.logaddexp(x, torch.zeros_like(x))`, and
   `backward(ctx, grad_output)` returning `grad_output * sigmoid(x)`.
2. Write `softplus(x)` returning `Softplus.apply(x)`.
3. Write `passes_gradcheck(fn, shape, seed=0)` that makes a float64 input of that shape with
   `torch.randn` from `torch.Generator().manual_seed(seed)`, `requires_grad=True`, and returns
   `torch.autograd.gradcheck(fn, (x,), raise_exception=False)`.

## Hints

<details><summary>Hint 1</summary>

In forward: `ctx.save_for_backward(x)`; in backward: `(x,) = ctx.saved_tensors`.

</details>

<details><summary>Hint 2</summary>

The derivative of softplus is the sigmoid, so return `grad_output * torch.sigmoid(x)`.

</details>

<details><summary>Hint 3</summary>

`x = torch.randn(shape, generator=g, dtype=torch.float64, requires_grad=True)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_backward_is_sigmoid` | backward must return grad_output * torch.sigmoid(x). |
| `test_wrong_backward_fails` | Pass raise_exception=False so gradcheck returns False instead of raising. |
| `test_stable_for_large_inputs` | Use torch.logaddexp(x, torch.zeros_like(x)) instead of log(1 + exp(x)). |
| `test_uses_custom_function` | softplus should call Softplus.apply(x). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The forward pass saves its input and uses `logaddexp`, which never overflows. The backward pass
multiplies the upstream gradient by the local derivative σ(x). gradcheck compares that backward
with central differences on a float64 input and reports whether they agree.

## References

- [torch.autograd.gradcheck](https://docs.pytorch.org/docs/stable/generated/torch.autograd.gradcheck.gradcheck.html) — PyTorch (`S110`)
- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
