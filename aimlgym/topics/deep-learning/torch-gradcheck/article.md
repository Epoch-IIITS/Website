# Custom Gradients and gradcheck

## Learning outcomes

After this lesson you can:

- Write a torch.autograd.Function with its own forward and backward
- Verify a backward pass numerically with torch.autograd.gradcheck
- Use float64 inputs for reliable finite-difference checks

## Intuition
Autograd knows the derivatives of PyTorch's own operations. Sometimes you write an operation
yourself — for speed, numerical stability or a research idea — and then you must supply its
backward pass. A wrong backward does not crash; it silently trains badly. `gradcheck` catches it by
comparing your gradients with finite differences, as you did in DL-13.

## Precise explanation
```python
class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)          # keep what backward needs
        return torch.logaddexp(x, torch.zeros_like(x))     # log(1 + e^x), stable

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * torch.sigmoid(x)               # chain rule: upstream × local

y = Softplus.apply(x)                     # use .apply, never call forward directly
```

* `backward` receives the gradient of the loss with respect to the output and returns the
  gradient with respect to each input.
* `torch.autograd.gradcheck(fn, (x,))` perturbs each input element by a small ε, compares the
  numerical slope with your backward, and returns `True` or raises; with
  `raise_exception=False` it returns `False` instead.
* Use **float64** inputs with `requires_grad=True`: in float32 the finite differences are too noisy.

## Worked example
softplus′(x) = eˣ/(1 + eˣ) = σ(x). At x = 0 the value is log 2 = 0.693 and the derivative 0.5. A
backward that returned `grad_output * x` would pass at no point except by luck; gradcheck reports it.

## What the library does inside
For each input element gradcheck evaluates (f(x + ε) − f(x − ε))/2ε, builds the numerical Jacobian,
and compares it with the Jacobian your backward implies — the DL-13 deep dive, for
every element and output at once.

## Common mistakes
* Calling `Softplus.forward(...)` instead of `Softplus.apply(...)`, so no graph is recorded.
* Forgetting to multiply by `grad_output`.
* Running gradcheck in float32 and chasing false failures.
* Computing `log(1 + exp(x))` directly, which overflows for x around 100.

## Why this matters
Custom operations appear in fused kernels, new activation functions and differentiable
simulators; gradcheck is how their authors trust them.

## References

- [torch.autograd.gradcheck](https://docs.pytorch.org/docs/stable/generated/torch.autograd.gradcheck.gradcheck.html) — PyTorch (`S110`)
- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
