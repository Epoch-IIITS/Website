# Reinforcement Learning

**You will be able to:** Define environments and returns (including Gymnasium environments), explore with bandits, solve MDPs with dynamic programming, and learn values with Monte Carlo, TD(0), Q-learning on FrozenLake and SARSA.

**Topic prerequisites:** NumPy

Learning from rewards. You first define returns, a gridworld transition function and the
reset/step environment interface — then the same environment as a real `gymnasium.Env` with
spaces and a time-limit wrapper. You explore with ε-greedy, incremental estimates and UCB bandits,
solve known MDPs with policy evaluation, value iteration and policy iteration, and learn from
experience with first-visit Monte Carlo, TD(0), Q-learning (also on Gymnasium's FrozenLake) and
SARSA.

**Packages:** `numpy` and `gymnasium`. **MDP format (design choice):** `P[s][a]` is a list of
`(probability, next_state, reward, done)` tuples; terminal transitions stop bootstrapping.
All environments are tiny and seeded, so every result is reproducible. **Project ideas:** a grid
game agent and a bandit-based recommender.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | RL-01 | [Discounted Return](discounted-return/problem.md) | beginner | PY-14 |
| 2 | RL-02 | [Gridworld Transition Function](gridworld-step/problem.md) | beginner | RL-01 |
| 3 | RL-03 | [The Environment Interface: reset and step](env-interface/problem.md) | beginner | RL-02 |
| 4 | RL-04 | [Gymnasium Environments](rl-gymnasium-env/problem.md) | beginner | RL-03 |
| 5 | RL-05 | [Epsilon-Greedy Action Selection](epsilon-greedy/problem.md) | beginner | RL-03, NP-10 |
| 6 | RL-06 | [Incremental Value Estimates](bandit-incremental/problem.md) | intermediate | RL-05 |
| 7 | RL-07 | [UCB1 Bandit](ucb-bandit/problem.md) | intermediate | RL-06 |
| 8 | RL-08 | [Iterative Policy Evaluation](policy-evaluation/problem.md) | intermediate | RL-02, RL-01 |
| 9 | RL-09 | [Value Iteration](value-iteration/problem.md) | intermediate | RL-08 |
| 10 | RL-10 | [Policy Iteration](policy-iteration/problem.md) | intermediate | RL-08, RL-09 |
| 11 | RL-11 | [First-Visit Monte Carlo Prediction](mc-first-visit/problem.md) | advanced | RL-03, RL-08 |
| 12 | RL-12 | [TD(0) Prediction](td0-prediction/problem.md) | advanced | RL-08, RL-11 |
| 13 | RL-13 | [Tabular Q-Learning](q-learning/problem.md) | advanced | RL-05, RL-02, RL-12 |
| 14 | RL-14 | [Q-Learning on FrozenLake](rl-frozenlake-q/problem.md) | advanced | RL-13, RL-04 |
| 15 | RL-15 | [SARSA](sarsa/problem.md) | advanced | RL-13 |
| 16 | RL-P1 | [Project idea: Grid Game Agent](grid-game-agent/project.md) | ungraded | RL-01, RL-04, RL-13, RL-14, RL-15 |
| 17 | RL-P2 | [Project idea: Bandit-Based Recommender](bandit-recommender/project.md) | ungraded | RL-05, RL-06, RL-07 |
