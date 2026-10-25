# SARSA: On-Policy TD Control

## Learning outcomes

After this lesson you can:

- Implement the on-policy SARSA update
- Choose the next action before updating
- Contrast SARSA's safer behaviour with Q-learning on a risky path

## Intuition
Q-learning learns values as if it will act perfectly later; SARSA learns the values of what it will
*actually* do, exploration included. Near a cliff, an exploring agent that sometimes slips should
prefer a safer path — and SARSA learns exactly that.

## Precise explanation (Sutton & Barto, §6.4; cliff-walking example 6.6)
Name from the tuple $(S, A, R, S', A')$:
$$Q(s,a) \leftarrow Q(s,a) + \alpha\big[r + \gamma(1-d)\,Q(s', a') - Q(s,a)\big],$$
where $a'$ is the action the ε-greedy policy will take next. Loop recipe:
```text
for each episode:
    s = start; a = eps_greedy(Q[s])
    repeat up to max_steps:
        s2, r, done = env_step(s, a)
        a2 = eps_greedy(Q[s2]) if not done else 0
        sarsa_update(Q, s, a, r, s2, a2, done, ...)
        s, a = s2, a2; stop if done
```
(One shared seeded generator; ε-greedy recipe from RL-05.)

## Worked example
Q(s', ·) = [5, 2], next action a′ = 1, r = −1, α = 0.5, γ = 0.9 → target −1 + 0.9·2 = 0.8
(Q-learning would use 5).

## Common mistakes
* Choosing a′ after the update (the update must use the a′ actually taken next).
* Using max over actions (that's Q-learning).
* Forgetting to carry a′ forward as the next action.

## Why this matters
The on/off-policy distinction matters whenever exploration is costly or dangerous (robots, real
systems).

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
