# DL-08 · A Tiny Autograd Engine

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** DL-06 Models with nn.Module, MA-11 Derivative Rules and the Chain Rule

Read the lesson first: [article.md](article.md)

## Task

Write `class Value` supporting:

* `Value(data)` with attributes `data` (float) and `grad` (starts at `0.0`).
* `+`, `*`, unary `-`, `-` (binary), `**` with an `int`/`float` exponent, and the reflected forms
  `number + Value`, `number * Value`, `number - Value`. Plain numbers are wrapped in `Value`.
* Methods `tanh()` and `exp()`.
* `backward()` — sets this value's gradient to 1 and fills `grad` for every value it depends on,
  using reverse topological order and accumulated (`+=`) gradients.

**Example**
```python
a, b = Value(2.0), Value(-3.0)
c = a * b + a
c.backward()
(c.data, a.grad, b.grad)    # (-4.0, -2.0, 2.0)
```

## Hints

<details><summary>Hint 1</summary>

Copy the `__add__` pattern for `__mul__`: the local derivatives are `other.data` and `self.data`.

</details>

<details><summary>Hint 2</summary>

`__neg__` can return `self * -1`, `__sub__` can return `self + (-other)`; `__radd__` returns `self + other` and `__rsub__` returns `other + (-self)`.

</details>

<details><summary>Hint 3</summary>

Topological order: a recursive `build(v)` that visits `v._prev` first, then appends `v`; skip nodes already in a `visited` set.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Implement `__mul__` with local derivatives `other.data` and `self.data`, and a working `backward`. |
| `test_reused_value_accumulates` | Use `+=` in every backward closure so reused values collect all contributions. |
| `test_reflected_and_sub` | Add `__radd__`, `__rmul__`, `__sub__` and `__rsub__`, wrapping numbers in Value. |
| `test_tanh_exp` | tanh's derivative is `1 - t**2`; exp's derivative is its own output. |
| `test_deep_chain_order` | Visit nodes in reverse topological order so each gradient is complete before it is pushed further. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every operation stores its inputs and a closure implementing its local chain-rule step.
`backward` performs a depth-first search to list nodes after their children, seeds the output
gradient with 1 and runs the closures from the output back to the leaves. Accumulating with `+=`
handles values that are used several times. Derived operations (`-`, subtraction, reflected
operators) are built from `+` and `*`, so they need no backward rule of their own.

## References

- [micrograd: a tiny scalar-valued autograd engine](https://github.com/karpathy/micrograd) — Andrej Karpathy (`S094`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
