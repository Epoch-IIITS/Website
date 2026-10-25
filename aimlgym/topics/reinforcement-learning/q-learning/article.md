# Q-Learning

## Learning outcomes

After this lesson you can:

- Implement the off-policy Q-learning update
- Train with ε-greedy exploration on a gridworld
- Extract and evaluate the learned greedy policy

## Intuition
Learn the value of every (state, action) pair directly from experience, always assuming you will act
optimally afterwards — even while you are still exploring. Then act greedily on those values.

## Precise explanation (Sutton & Barto, §6.5)
$$Q(s,a) \leftarrow Q(s,a) + \alpha\big[r + \gamma(1-d)\max_{a'}Q(s',a') - Q(s,a)\big].$$
**Off-policy:** the target uses the greedy $\max_{a'}$ even though the behaviour policy is ε-greedy.
Training loop (this course's recipe, one seeded generator):
```text
for each episode:
    s = start
    for up to max_steps steps:
        a = epsilon_greedy(Q[s], epsilon, rng)      # RL-05 recipe
        s2, r, done = env_step(s, a)
        q_update(Q, s, a, r, s2, done, alpha, gamma)
        s = s2; stop if done
```
The greedy policy $\arg\max_a Q(s,a)$ converges to optimal with sufficient exploration and a suitable α.

## Worked example
Q(s,·) = [0, 0], action 1 gives r = −1 to s' with max Q = 5, α = 0.5, γ = 0.9:
Q(s,1) = 0 + 0.5(−1 + 4.5 − 0) = 1.75.

## Common mistakes
* Using $Q(s', a_\text{next})$ (that's SARSA, RL-15).
* Bootstrapping from terminal states.
* Never decaying/limiting episodes → infinite loops; use max_steps.

## Why this matters
Q-learning is the basis of DQN, which learned to play Atari games from pixels.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
