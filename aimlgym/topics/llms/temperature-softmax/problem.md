# LM-03 · Logits, Temperature and Softmax

**Topic:** Large Language Models · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** LM-02 Next-Token Probabilities (Add-k), DL-02 Numerically Stable Softmax

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `softmax_t(logits, T=1.0)` → stable softmax of `logits / T` (1-D); raise `ValueError` if `T <= 0`.
* `entropy(p)` → natural-log entropy of a probability vector (0·log 0 treated as 0).

**Examples**
```python
softmax_t(np.array([2., 1., 0.]), 0.5)   # [0.8668, 0.1173, 0.0159]
entropy(np.array([0.5, 0.5]))            # 0.6931...
entropy(np.array([1.0, 0.0]))            # 0.0
```

## Hints

<details><summary>Hint 1</summary>

`z = np.asarray(logits, float) / T`, subtract the max, exponentiate, normalise.

</details>

<details><summary>Hint 2</summary>

Entropy: use only `p > 0` entries: `-(p[p > 0] * np.log(p[p > 0])).sum()`.

</details>

<details><summary>Hint 3</summary>

Validate T before dividing.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_t_half` | Divide logits by T (T = 0.5 doubles them). |
| `test_entropy` | Skip zero probabilities to avoid log(0). |
| `test_low_t_greedy` | Use the max-subtraction trick so tiny T does not overflow. |
| `test_bad_t` | T must be > 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Scaling logits by 1/T before a stable softmax implements temperature. Entropy ignores zero
entries, matching the 0·log 0 = 0 convention.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi (`S021`)
