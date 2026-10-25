# ε-Greedy Exploration

## Learning outcomes

After this lesson you can:

- Balance exploration and exploitation
- Implement ε-greedy with a seeded generator
- Compute the ε-greedy action probabilities

## Intuition
Always ordering your favourite dish means you never discover a better one. ε-greedy usually exploits
the best-known action but, with small probability ε, tries a random one.

## Precise explanation
Given action values $Q(a)$:
* with probability ε choose uniformly among all $|A|$ actions;
* otherwise choose $\arg\max_a Q(a)$ (ties → lowest index in this course).
So the greedy action has probability $1 - \varepsilon + \varepsilon/|A|$ and every other action
$\varepsilon/|A|$ (with ties broken to the lowest index).
Recipe: `if rng.random() < epsilon: return int(rng.integers(n))` else argmax. ε is often decayed over
time (explore early, exploit later).

## Worked example
Q = [1, 5, 2], ε = 0.3 → probabilities [0.1, 0.8, 0.1].

## Common mistakes
* Excluding the greedy action from the random choice (changes the probabilities).
* Global random state.
* ε = 0 from the start (no exploration → may never find good actions).

## Why this matters
ε-greedy is the behaviour policy in Q-learning and SARSA (RL-13, RL-15).

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
