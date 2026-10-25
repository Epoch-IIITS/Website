# DL-14 · SGD with Momentum

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** DL-11 Backpropagation Through a Dense Layer, MA-13 Gradient Descent in 1D

Read the lesson first: [article.md](article.md)

## Task

Implement `class Momentum(lr=0.01, beta=0.9)`:
* `step(params, grads)` — `params` and `grads` are dicts name → NumPy array (same keys/shapes).
  Update velocities (created lazily as zeros on first use) and return a **new** dict of updated
  params; inputs must not be modified.
* Raise `ValueError` if keys differ, shapes differ, `lr <= 0`, or `beta` not in `[0, 1)`.

**Example**
```python
opt = Momentum(lr=0.1, beta=0.9)
p = {"w": np.array([0.0])}
for _ in range(3):
    p = opt.step(p, {"w": np.array([1.0])})
p["w"]    # [-0.561]  (= -(0.1 + 0.19 + 0.271))
```

## Hints

<details><summary>Hint 1</summary>

Store `self.v = {}` and create `np.zeros_like(param)` the first time a key appears.

</details>

<details><summary>Hint 2</summary>

`self.v[k] = self.beta * self.v[k] + grads[k]`.

</details>

<details><summary>Hint 3</summary>

Build `new[k] = params[k] - self.lr * self.v[k]` (a new array).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | v ← βv + g; θ ← θ − lr·v, with v persisting between calls. |
| `test_separate_state` | Keep one velocity array per parameter name. |
| `test_no_mutation` | Return new arrays; don't use -= on the inputs. |
| `test_errors` | Validate beta in [0, 1) and matching shapes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Velocity arrays persist inside the optimiser, one per parameter name. Each step blends the old
velocity with the new gradient and moves the parameter against the velocity, returning fresh
arrays so caller data is never mutated.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
