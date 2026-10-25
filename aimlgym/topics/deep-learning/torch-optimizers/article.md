# Optimisers in torch.optim

## Learning outcomes

After this lesson you can:

- Run the zero_grad / backward / step cycle with torch.optim
- Compare SGD, SGD with momentum, Adam and AdamW on the same problem
- Explain what weight decay does and how AdamW applies it

## Intuition
An optimiser turns gradients into updates. Plain SGD steps straight downhill; momentum
(DL-14) keeps a running velocity; Adam scales each parameter's step by a running
estimate of its gradient size, so steep and flat directions both make progress. In PyTorch they all
share one three-line loop.

## Precise explanation
```python
params = torch.tensor([0.0, 0.0], requires_grad=True)
opt = torch.optim.Adam([params], lr=0.1)
for _ in range(steps):
    opt.zero_grad()           # clear old gradients (they accumulate)
    loss = f(params)
    loss.backward()           # fill params.grad
    opt.step()                # update params in place
```

| Optimiser | Update (per parameter) |
|---|---|
| `SGD(lr)` | θ ← θ − lr·g |
| `SGD(lr, momentum=0.9)` | v ← 0.9v + g; θ ← θ − lr·v |
| `Adam(lr)` | m, v running means of g and g², bias-corrected; θ ← θ − lr·m̂/(√v̂ + ε) |
| `AdamW(lr, weight_decay)` | Adam, plus θ ← θ − lr·wd·θ applied directly to the weights |

* The optimiser receives the tensors to update (`model.parameters()` for a model).
* **Weight decay** shrinks weights a little every step, a form of the regularisation in
  ML-19. In Adam it interacts with the adaptive scaling; AdamW decouples it,
  which is why AdamW is the usual default for transformers.

## Worked example
For f(x, y) = (x − 3)² + 10(y + 1)² from (0, 0): SGD with lr 0.01 crawls along x because the
y-direction forces a small step; Adam with lr 0.1 moves both coordinates at similar speed and reaches
(3, −1) within about 200 steps.

## What the library does inside
`Adam.step` keeps the two running averages per parameter and applies the bias correction you
implement in DL-16, the optional deep dive after this step.

## Common mistakes
* Forgetting `zero_grad()`, so gradients from every previous step are added together.
* Creating the optimiser before the model's parameters exist, or for a copy of them.
* Using the same learning rate for SGD and Adam: good values differ by orders of magnitude.

## Why this matters
The training loop in DL-18 is this loop with a model and data; changing the
optimiser is a one-line experiment.

## References

- [torch.optim](https://docs.pytorch.org/docs/stable/optim.html) — PyTorch (`S107`)
- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
