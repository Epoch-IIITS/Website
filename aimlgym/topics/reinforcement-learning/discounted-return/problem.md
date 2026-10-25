# RL-01 · Discounted Return

**Topic:** Reinforcement Learning · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-14 Fibonacci Sequence

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `discounted_return(rewards, gamma)` → float $G_0$.
* `returns_to_go(rewards, gamma)` → list of $G_t$ for every t (backward pass).
Raise `ValueError` unless `0 <= gamma <= 1`. Empty rewards give `0.0` / `[]`.

**Examples**
```python
discounted_return([1, 0, 2], 0.5)   # 1.5
returns_to_go([1, 0, 2], 0.5)       # [1.5, 1.0, 2.0]
```

## Hints

<details><summary>Hint 1</summary>

Start `G = 0.0` and loop over `reversed(rewards)`.

</details>

<details><summary>Hint 2</summary>

`G = r + gamma * G`.

</details>

<details><summary>Hint 3</summary>

Collect G values and reverse the list at the end.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | The first reward is not discounted: G = R1 + γR2 + … |
| `test_gamma_one` | Use the backward recursion G = r + γG. |
| `test_long` | A single O(T) backward loop is enough. |
| `test_bad_gamma` | Validate 0 ≤ γ ≤ 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The recursion G_t = R_{t+1} + γ G_{t+1} lets one backward scan produce every return; G_0 is its first
element.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
