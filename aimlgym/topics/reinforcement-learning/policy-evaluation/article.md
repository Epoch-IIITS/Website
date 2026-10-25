# Iterative Policy Evaluation

## Learning outcomes

After this lesson you can:

- Apply the Bellman expectation backup
- Iterate to convergence with a tolerance
- Handle terminal transitions correctly

## Intuition
How good is it to be in each state if I follow this policy? A state's value is the expected
immediate reward plus the discounted value of where I land. Start with zeros and repeatedly apply
that rule until the numbers stop changing.

## Precise explanation (Sutton & Barto, §4.1)
Bellman expectation backup for policy π:
$$V_{k+1}(s) = \sum_a \pi(a\mid s) \sum_{(p, s', r, d)\in P[s][a]} p\,\big[r + \gamma (1 - d)\,V_k(s')\big].$$
The factor $(1-d)$ stops bootstrapping from terminal transitions. We use **synchronous** updates (a
new array each sweep). Stop when $\max_s |V_{k+1}(s) - V_k(s)| < \theta$. For γ < 1 this converges to
the unique $V^\pi$.

## Worked example
Corridor 0 → 1 → goal, always move right, reward −1 per step and +10 entering the goal, γ = 0.9:
V(1) = 10, V(0) = −1 + 0.9·10 = 8.

## Common mistakes
* Bootstrapping from terminal states.
* Mixing old and new values unintentionally (in-place sweeps are valid but converge differently).
* Policy rows that don't sum to 1.

## Why this matters
Policy evaluation is half of policy iteration (RL-10) and the conceptual basis of TD learning.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
