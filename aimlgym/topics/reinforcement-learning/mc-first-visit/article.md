# Monte Carlo Prediction

## Learning outcomes

After this lesson you can:

- Estimate values by averaging sampled returns
- Implement the first-visit rule
- Compare with every-visit estimates

## Intuition
Don't know the environment's rules? Play complete episodes, record the return that followed each
visit to a state, and average. With enough episodes the averages approach the true values.

## Precise explanation (Sutton & Barto, §5.1)
An episode is a list of `(state, reward)` pairs: the state at time t and the reward received after
acting there, $R_{t+1}$. Compute returns backwards (RL-01). **First-visit MC** averages, for each state,
only the return following its *first* occurrence in each episode; **every-visit MC** uses every
occurrence. Both converge to $V^\pi(s)$. States never visited keep value 0 (and count 0).

## Worked example
Episodes [(A, 1), (B, 0), (A, 2)] and [(B, 5)], γ = 1, states A = 0, B = 1:
episode 1 returns: t0: 3, t1: 2, t2: 2. First-visit: A ← 3, B ← 2. Episode 2: B ← 5.
V = [3, 3.5]. Every-visit: A ← {3, 2}, B ← {2, 5} → [2.5, 3.5].

## Common mistakes
* Using the *last* visit instead of the first.
* Forward return computation per visit (O(T²)).
* Averaging returns across episodes incorrectly (keep sums and counts).

## Why this matters
MC methods need no model of the environment, only experience — the foundation of model-free RL.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
