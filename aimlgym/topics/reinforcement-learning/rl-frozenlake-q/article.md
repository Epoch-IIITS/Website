# Q-Learning on FrozenLake

## Learning outcomes

After this lesson you can:

- Train a tabular Q-learning agent on gymnasium's FrozenLake-v1
- Explore with a decaying epsilon and break ties between equal Q-values randomly
- Evaluate the greedy policy by its success rate on new episodes

## Intuition
FrozenLake is a 4×4 grid of ice with holes; the agent walks from the top-left to the goal at the
bottom-right and only gets reward 1 if it arrives. On slippery ice, an action may move it sideways.
Rewards are rare, so the agent must explore a lot before Q-values carry any signal.

## Precise explanation
```python
env = gym.make("FrozenLake-v1", is_slippery=True)      # 16 states, 4 actions (left, down, right, up)
Q[s, a] += alpha * (r + gamma * (0 if terminated else Q[s2].max()) - Q[s, a])
```

* This is the update of RL-13: bootstrap from the best next action **unless the episode
  terminated** (a hole or the goal). A truncated episode (100-step limit) is not terminal.
* **Decaying epsilon**: explore almost always at first, then less: ε = max(ε_min, 1 − episode/(0.7·episodes)).
* **Random tie-breaking**: at the start all Q-values are 0, and `argmax` would always choose action 0;
  pick uniformly among the actions with the maximum value instead.
* Seed both the environment (`env.reset(seed=...)`) and your own generator, so training is reproducible.
* **Evaluate** the greedy policy (no exploration) over many new episodes and report the success rate.
  On the slippery lake even the optimal policy succeeds only about three times in four.

## Worked example
On the non-slippery lake, 300 episodes are enough for a 100% success rate. On the slippery lake, 2,000
episodes give about 73%.

## Common mistakes
* Bootstrapping from the next state after falling into a hole.
* Plain `argmax` with all-zero Q-values, so the agent never leaves the first column.
* Evaluating with exploration still on.

## Why this matters
FrozenLake is the classic sanity check for tabular RL; the grid-game project idea after this step asks
you to design your own environment and train the same agent on it.

## References

- [Frozen Lake (Gymnasium docs)](https://gymnasium.farama.org/environments/toy_text/frozen_lake/) — Farama Foundation (`S141`)
- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
