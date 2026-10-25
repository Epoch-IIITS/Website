"""Reinforcement learning with Gymnasium (library revision, Phase 6)."""

PROBLEMS = [
# ---------------------------------------------------------------- rl-gymnasium-env
{
"slug": "rl-gymnasium-env", "title": "Gymnasium Environments",
"difficulty": "beginner", "prereqs": ["env-interface"], "packages": ["numpy", "gymnasium"],
"objectives": ["Write an environment as a gymnasium.Env subclass with observation and action spaces",
               "Use the seeded self.np_random generator through super().reset(seed=seed)",
               "Add a time limit with the TimeLimit wrapper and validate the environment with check_env"],
"tags": ["gymnasium", "environments", "spaces", "wrappers"],
"sources": ["S099", "S035"], "entry": "class LineWorldEnv(gym.Env); make_lineworld(n=5, slip=0.0, max_steps=20)",
"article": r'''
# Gymnasium Environments

## Intuition
Your `LineWorld` in [[env-interface]] followed the reset/step contract by convention. Gymnasium makes
it official: subclass `gymnasium.Env`, declare what observations and actions look like, and every
Gymnasium tool — wrappers, checkers, vectorised runners, and RL libraries — works with your environment.

## Precise explanation
```python
import gymnasium as gym
from gymnasium import spaces

class LineWorldEnv(gym.Env):
    def __init__(self, n=5, slip=0.0):
        self.observation_space = spaces.Discrete(n)     # states 0 .. n-1
        self.action_space = spaces.Discrete(2)          # 0 = left, 1 = right

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)                        # (re)seeds self.np_random
        return 0, {}

    def step(self, action):
        ...
        return obs, reward, terminated, False, {}
```

* **Spaces** describe valid values: `Discrete(n)` is {0, …, n−1}; `Box` is for real-valued vectors.
  `space.contains(x)` checks a value and `space.sample()` draws a random one.
* `super().reset(seed=seed)` creates `self.np_random`, a NumPy generator; use it for every random
  choice so a seed reproduces an episode.
* Time limits belong in a **wrapper**: `gymnasium.wrappers.TimeLimit(env, max_episode_steps=20)` sets
  `truncated=True` after 20 steps, so the environment itself only reports `terminated`.
* `gymnasium.utils.env_checker.check_env(env)` checks the API: return types, spaces, seeding.
* Built-in environments are created with `gym.make("FrozenLake-v1")`, used in the next step.

## Worked example
`make_lineworld(n=5, max_steps=6)`: moving right four times terminates with reward 1; moving left six
times returns `truncated=True` from the wrapper. With `slip=0.5` and seed 3, two runs with the same
actions produce the same states.

## Common mistakes
* Using `random` or a module-level NumPy generator instead of `self.np_random`.
* Putting the step limit inside the environment and also wrapping it.
* Returning NumPy integers outside the declared space, or forgetting the `info` dict.

## Why this matters
Q-learning on FrozenLake next, and the grid-game project idea, use this interface; so do libraries such
as Stable-Baselines3 for larger problems.
''',
"statement": r'''
1. `class LineWorldEnv(gym.Env)` with `__init__(self, n=5, slip=0.0)` (raise `ValueError` unless
   `n >= 2` and `0 <= slip <= 1`), `observation_space = spaces.Discrete(n)` and
   `action_space = spaces.Discrete(2)`.
   * `reset(self, *, seed=None, options=None)`: call `super().reset(seed=seed)`, set the state to 0 and
     return `(0, {})`.
   * `step(self, action)`: raise `ValueError` if the action is not in the action space. When `slip > 0`,
     reverse the action if `self.np_random.random() < self.slip`. Move left (0) or right (1), clipped to
     `[0, n - 1]`. Return `(state, reward, terminated, False, {})` with reward `1.0` and
     `terminated=True` at state `n - 1`, else `0.0` and `False`. States are Python ints.
2. `make_lineworld(n=5, slip=0.0, max_steps=20)` returns `TimeLimit(LineWorldEnv(n, slip), max_episode_steps=max_steps)`.
''',
"starter": r'''
import gymnasium as gym
from gymnasium import spaces
from gymnasium.wrappers import TimeLimit


class LineWorldEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, n=5, slip=0.0):
        # TODO
        pass

    def reset(self, *, seed=None, options=None):
        # TODO
        pass

    def step(self, action):
        # TODO
        pass


def make_lineworld(n=5, slip=0.0, max_steps=20):
    # TODO
    pass
''',
"hints": [
    "Validate the arguments, then create the two `spaces.Discrete` objects.",
    "`self.action_space.contains(action)` checks the action; draw the slip with `self.np_random.random()`.",
    "`min(max(self.state + step, 0), self.n - 1)` keeps the state on the line.",
],
"solution": r'''
import gymnasium as gym
from gymnasium import spaces
from gymnasium.wrappers import TimeLimit


class LineWorldEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, n=5, slip=0.0):
        if n < 2 or not 0 <= slip <= 1:
            raise ValueError("need n >= 2 and 0 <= slip <= 1")
        self.n, self.slip = n, slip
        self.observation_space = spaces.Discrete(n)
        self.action_space = spaces.Discrete(2)
        self.state = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = 0
        return self.state, {}

    def step(self, action):
        if not self.action_space.contains(action):
            raise ValueError("action must be 0 or 1")
        if self.slip > 0 and self.np_random.random() < self.slip:
            action = 1 - action
        self.state = int(min(max(self.state + (1 if action == 1 else -1), 0), self.n - 1))
        terminated = self.state == self.n - 1
        return self.state, 1.0 if terminated else 0.0, terminated, False, {}


def make_lineworld(n=5, slip=0.0, max_steps=20):
    return TimeLimit(LineWorldEnv(n, slip), max_episode_steps=max_steps)
''',
"explanation": r'''
The spaces document the interface; `super().reset(seed=...)` sets up `self.np_random`, which drives
every random slip, so seeds reproduce episodes. The environment reports only termination; the
TimeLimit wrapper adds truncation.
''',
"tests": r'''
import gymnasium as gym
from gymnasium.utils.env_checker import check_env
from gymnasium.wrappers import TimeLimit


def run(env, actions, seed=None):
    obs, _ = env.reset(seed=seed)
    states = [obs]
    for a in actions:
        obs, r, terminated, truncated, _ = env.step(a)
        states.append(obs)
        if terminated or truncated:
            return states, r, terminated, truncated
    return states, r, terminated, truncated


class TestGymnasiumEnv(unittest.TestCase):
    def test_check_env(self):
        check_env(S.LineWorldEnv(), skip_render_check=True)

    def test_spaces(self):
        env = S.LineWorldEnv(7)
        self.assertEqual((env.observation_space.n, env.action_space.n), (7, 2))

    def test_reach_goal(self):
        states, r, terminated, truncated = run(S.make_lineworld(5), [1, 1, 1, 1], seed=0)
        self.assertEqual((states, r, terminated, truncated), ([0, 1, 2, 3, 4], 1.0, True, False))

    def test_time_limit_truncates(self):
        env = S.make_lineworld(5, max_steps=6)
        self.assertIsInstance(env, TimeLimit)
        states, r, terminated, truncated = run(env, [0] * 10, seed=0)
        self.assertEqual((len(states) - 1, terminated, truncated), (6, False, True))

    def test_seeded_slip_reproducible(self):
        actions = [1] * 15
        a = run(S.make_lineworld(6, slip=0.5, max_steps=15), actions, seed=3)[0]
        b = run(S.make_lineworld(6, slip=0.5, max_steps=15), actions, seed=3)[0]
        self.assertEqual(a, b)
        self.assertTrue(all(type(s) is int for s in a))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.LineWorldEnv(1)
        env = S.LineWorldEnv()
        env.reset(seed=0)
        with self.assertRaises(ValueError):
            env.step(2)
''',
"feedback": [
    ("test_check_env", "Subclass gym.Env, define both spaces and return (obs, info) from reset."),
    ("test_time_limit_truncates", "Wrap the environment with TimeLimit(env, max_episode_steps=max_steps)."),
    ("test_seeded_slip_reproducible", "Call super().reset(seed=seed) and draw slips from self.np_random."),
    ("test_invalid", "Validate the constructor arguments and reject actions outside the action space."),
],
},
# ---------------------------------------------------------------- rl-frozenlake-q
{
"slug": "rl-frozenlake-q", "title": "Q-Learning on FrozenLake",
"difficulty": "advanced", "prereqs": ["q-learning", "rl-gymnasium-env"], "packages": ["numpy", "gymnasium"],
"objectives": ["Train a tabular Q-learning agent on gymnasium's FrozenLake-v1",
               "Explore with a decaying epsilon and break ties between equal Q-values randomly",
               "Evaluate the greedy policy by its success rate on new episodes"],
"tags": ["gymnasium", "q-learning", "frozenlake", "exploration"],
"sources": ["S141", "S033"], "entry": "q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0); success_rate(env, Q, episodes=200, seed=10000)",
"article": r'''
# Q-Learning on FrozenLake

## Intuition
FrozenLake is a 4×4 grid of ice with holes; the agent walks from the top-left to the goal at the
bottom-right and only gets reward 1 if it arrives. On slippery ice, an action may move it sideways.
Rewards are rare, so the agent must explore a lot before Q-values carry any signal.

## Precise explanation
```python
env = gym.make("FrozenLake-v1", is_slippery=True)      # 16 states, 4 actions (left, down, right, up)
Q[s, a] += alpha * (r + gamma * (0 if terminated else Q[s2].max()) - Q[s, a])
```

* This is the update of [[q-learning]]: bootstrap from the best next action **unless the episode
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
''',
"statement": r'''
1. `q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0)` returns a NumPy array
   `Q` of shape `(n_states, n_actions)` from the env's spaces. Use `rng = np.random.default_rng(seed)`.
   For episode `ep`: `eps = max(eps_min, 1 - ep / (0.7 * episodes))`; `obs, _ = env.reset(seed=seed + ep)`;
   until terminated or truncated, explore with probability `eps` (`int(rng.integers(n_actions))`),
   otherwise take a greedy action with random ties (`int(rng.choice(np.flatnonzero(q == q.max())))`);
   then apply the Q-learning update with no bootstrap on termination.
2. `success_rate(env, Q, episodes=200, seed=10000)` runs the greedy policy `int(np.argmax(Q[obs]))` for
   `episodes` episodes (`env.reset(seed=seed + i)`) and returns the fraction with reward 1 at the end.

Raise `ValueError` in `q_learning` if `episodes < 1`.
''',
"starter": r'''
import numpy as np


def q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0):
    # TODO
    pass


def success_rate(env, Q, episodes=200, seed=10000):
    # TODO
    pass
''',
"hints": [
    "`n_states, n_actions = env.observation_space.n, env.action_space.n`; `Q = np.zeros((n_states, n_actions))`.",
    "`target = r + (0.0 if terminated else gamma * Q[next_obs].max())`; `Q[obs, a] += alpha * (target - Q[obs, a])`.",
    "In `success_rate`, add the final reward of each episode and divide by the number of episodes.",
],
"solution": r'''
import numpy as np


def q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0):
    if episodes < 1:
        raise ValueError("episodes must be at least 1")
    n_states, n_actions = env.observation_space.n, env.action_space.n
    Q = np.zeros((n_states, n_actions))
    rng = np.random.default_rng(seed)
    for ep in range(episodes):
        eps = max(eps_min, 1 - ep / (0.7 * episodes))
        obs, _ = env.reset(seed=seed + ep)
        done = False
        while not done:
            if rng.random() < eps:
                a = int(rng.integers(n_actions))
            else:
                q = Q[obs]
                a = int(rng.choice(np.flatnonzero(q == q.max())))
            next_obs, r, terminated, truncated, _ = env.step(a)
            target = r + (0.0 if terminated else gamma * Q[next_obs].max())
            Q[obs, a] += alpha * (target - Q[obs, a])
            obs, done = next_obs, terminated or truncated
    return Q


def success_rate(env, Q, episodes=200, seed=10000):
    wins = 0.0
    for i in range(episodes):
        obs, _ = env.reset(seed=seed + i)
        done = False
        while not done:
            obs, r, terminated, truncated, _ = env.step(int(np.argmax(Q[obs])))
            done = terminated or truncated
        wins += r
    return wins / episodes
''',
"explanation": r'''
Decaying epsilon spends the early episodes exploring, and random tie-breaking avoids getting stuck on
action 0 while all values are equal. The update bootstraps only from non-terminal states. Evaluation
turns exploration off and counts how often the greedy policy reaches the goal.
''',
"tests": r'''
import gymnasium as gym
import numpy as np


class TestFrozenLake(unittest.TestCase):
    def test_deterministic_lake_solved(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        Q = S.q_learning(env, 300)
        self.assertEqual(S.success_rate(env, Q, episodes=20), 1.0)

    def test_slippery_lake(self):
        env = gym.make("FrozenLake-v1", is_slippery=True)
        Q = S.q_learning(env, 2000)
        self.assertGreater(S.success_rate(env, Q), 0.6)

    def test_shape_and_terminal_rows(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        Q = S.q_learning(env, 50)
        self.assertEqual(Q.shape, (16, 4))
        for hole_or_goal in (5, 7, 11, 12, 15):
            self.assertTrue(np.all(Q[hole_or_goal] == 0))

    def test_reproducible(self):
        env = gym.make("FrozenLake-v1", is_slippery=True)
        self.assertTrue(np.array_equal(S.q_learning(env, 100, seed=3), S.q_learning(env, 100, seed=3)))

    def test_untrained_policy_fails(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        self.assertEqual(S.success_rate(env, np.zeros((16, 4)), episodes=10), 0.0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.q_learning(gym.make("FrozenLake-v1"), 0)
''',
"feedback": [
    ("test_deterministic_lake_solved", "Break ties randomly among maximal actions and decay epsilon."),
    ("test_shape_and_terminal_rows", "Do not bootstrap from terminal states; their rows stay at zero."),
    ("test_reproducible", "Seed the generator and each env.reset(seed=seed + ep)."),
    ("test_untrained_policy_fails", "success_rate uses argmax of Q and counts the final reward."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "grid-game-agent", "title": "Grid Game Agent",
"tags": ["reinforcement-learning", "gymnasium", "q-learning"],
"brief": r'''
Design a small grid game of your own — collect keys and reach the door, avoid moving guards, or push a
box onto a target — as a Gymnasium environment, then train a Q-learning agent to play it and watch it
improve.
''',
"uses": ["discounted-return", "rl-gymnasium-env", "q-learning", "rl-frozenlake-q", "sarsa"],
"milestones": [
    "Define the rules, the state encoding and the rewards on paper; keep the state space small.",
    "Implement the game as a gymnasium.Env and pass check_env.",
    "Print the grid as text after each step so you can play it yourself with the keyboard.",
    "Train Q-learning and plot the success rate and average return per 100 episodes.",
    "Compare Q-learning with SARSA and explain any difference in the learned behaviour.",
],
"stretch": [
    "Make the game stochastic (slippery moves, random guards) and compare again.",
    "Replace the table with a small neural network (deep Q-learning) for a larger grid.",
    "Record and replay an episode as an animated GIF.",
],
"data": r'''
No data is needed: the agent learns from playing your game. See the
[FrozenLake documentation](https://gymnasium.farama.org/environments/toy_text/frozen_lake/) for a
text-based environment to imitate.
''',
"setup": r'''
```bash
pip install gymnasium numpy matplotlib
python train_agent.py
```
''',
},
{
"kind": "project", "slug": "bandit-recommender", "title": "Bandit-Based Recommender",
"tags": ["bandits", "recommendation", "exploration"],
"brief": r'''
Build a recommender that picks which article to show next, learning from simulated clicks. Compare
random choice, epsilon-greedy and UCB by their cumulative regret, and see what happens when reader
interests change over time.
''',
"uses": ["epsilon-greedy", "bandit-incremental", "ucb-bandit"],
"milestones": [
    "Simulate 10 articles with hidden click probabilities and a reader who clicks with those probabilities.",
    "Implement random, epsilon-greedy and UCB recommenders with the same interface.",
    "Run each for 10,000 recommendations over 20 seeds and plot average cumulative regret.",
    "Make the click probabilities drift slowly and add a sliding-window version of UCB.",
    "Write up which strategy you would deploy and why.",
],
"stretch": [
    "Implement Thompson sampling with Beta distributions.",
    "Add reader features (contextual bandits) with one linear model per article.",
    "Serve recommendations from a FastAPI endpoint that updates on click events.",
],
"data": r'''
Everything is simulated with seeded NumPy generators, so experiments are reproducible.
''',
"setup": r'''
```bash
pip install numpy matplotlib
python bandits.py --strategy ucb --steps 10000
```
''',
},
]
