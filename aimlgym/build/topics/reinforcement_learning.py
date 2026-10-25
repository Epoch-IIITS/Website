"""Problem definitions for the reinforcement learning topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- discounted-return
{
"slug": "discounted-return", "title": "Discounted Return",
"difficulty": "beginner", "prereqs": ["fibonacci-sequence"], "packages": [],
"objectives": ["Compute the discounted return of a reward sequence", "Compute returns for every time step in one backward pass",
               "Explain the role of the discount factor γ"],
"tags": ["returns", "discounting", "rewards"],
"sources": ["S033", "S034"], "entry": "discounted_return(rewards, gamma); returns_to_go(rewards, gamma)",
"article": r'''
# Returns and Discounting

## Intuition
An RL agent cares about the total reward it will collect, not just the next reward. Rewards far in
the future are usually worth a bit less — like money with interest — so we **discount** them.

## Precise explanation (Sutton & Barto, ch. 3)
For rewards $R_{t+1}, R_{t+2}, \dots, R_T$ and $0 \le \gamma \le 1$:
$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k=0}^{T-t-1}\gamma^k R_{t+k+1}.$$
**Recursive form:** $G_t = R_{t+1} + \gamma G_{t+1}$ with $G_T = 0$. Scanning rewards backwards
computes all returns in O(T) — the same "carry state through a loop" pattern as Fibonacci ([[fibonacci-sequence]]).
γ = 0: only the immediate reward matters; γ close to 1: far-sighted.

## Worked example
rewards [1, 0, 2], γ = 0.5: G₂ = 2; G₁ = 0 + 0.5·2 = 1; G₀ = 1 + 0.5·1 = 1.5.

## Common mistakes
* Discounting the first reward ($\gamma^1 R_1$ instead of $\gamma^0 R_1$).
* Forward loops recomputing sums (O(T²)).
* γ > 1 (returns may diverge).

## Why this matters
Every value function, policy-gradient method and RL loss is built on returns.
''',
"statement": r'''
Implement:
* `discounted_return(rewards, gamma)` → float $G_0$.
* `returns_to_go(rewards, gamma)` → list of $G_t$ for every t (backward pass).
Raise `ValueError` unless `0 <= gamma <= 1`. Empty rewards give `0.0` / `[]`.

**Examples**
```python
discounted_return([1, 0, 2], 0.5)   # 1.5
returns_to_go([1, 0, 2], 0.5)       # [1.5, 1.0, 2.0]
```
''',
"starter": r'''
def discounted_return(rewards, gamma):
    pass


def returns_to_go(rewards, gamma):
    return []
''',
"hints": [
    "Start `G = 0.0` and loop over `reversed(rewards)`.",
    "`G = r + gamma * G`.",
    "Collect G values and reverse the list at the end.",
],
"solution": r'''
def returns_to_go(rewards, gamma):
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be in [0, 1]")
    out = []
    G = 0.0
    for r in reversed(rewards):
        G = r + gamma * G
        out.append(G)
    return out[::-1]


def discounted_return(rewards, gamma):
    rtg = returns_to_go(rewards, gamma)
    return rtg[0] if rtg else 0.0
''',
"explanation": r'''
The recursion G_t = R_{t+1} + γ G_{t+1} lets one backward scan produce every return; G_0 is its first
element.
''',
"tests": r'''
class TestReturns(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(S.discounted_return([1, 0, 2], 0.5), 1.5)
        self.assertEqual([round(g, 10) for g in S.returns_to_go([1, 0, 2], 0.5)], [1.5, 1.0, 2.0])

    def test_gamma_zero(self):
        self.assertEqual(S.returns_to_go([3, 4, 5], 0.0), [3, 4, 5])

    def test_gamma_one(self):
        self.assertEqual(S.returns_to_go([1, 2, 3], 1.0), [6, 5, 3])

    def test_empty(self):
        self.assertEqual(S.discounted_return([], 0.9), 0.0)
        self.assertEqual(S.returns_to_go([], 0.9), [])

    def test_formula(self):
        r = [0.5, -1.0, 2.0, 0.0, 3.0]
        g = 0.9
        self.assertAlmostEqual(S.discounted_return(r, g), sum(g ** k * x for k, x in enumerate(r)))

    def test_long(self):
        self.assertAlmostEqual(S.discounted_return([1.0] * 2000, 0.99), (1 - 0.99 ** 2000) / 0.01, places=6)

    def test_bad_gamma(self):
        with self.assertRaises(ValueError):
            S.discounted_return([1], 1.5)
''',
"feedback": [
    ("test_example", "The first reward is not discounted: G = R1 + γR2 + …"),
    ("test_gamma_one", "Use the backward recursion G = r + γG."),
    ("test_long", "A single O(T) backward loop is enough."),
    ("test_bad_gamma", "Validate 0 ≤ γ ≤ 1."),
],
},
# ---------------------------------------------------------------- epsilon-greedy
{
"slug": "epsilon-greedy", "title": "Epsilon-Greedy Action Selection",
"difficulty": "beginner", "prereqs": ["env-interface", "seeded-generator"], "packages": ["numpy"],
"objectives": ["Balance exploration and exploitation", "Implement ε-greedy with a seeded generator",
               "Compute the ε-greedy action probabilities"],
"tags": ["exploration", "epsilon-greedy", "policies"],
"sources": ["S033"], "entry": "epsilon_greedy(q_values, epsilon, rng); epsilon_greedy_probs(q_values, epsilon)",
"article": r'''
# ε-Greedy Exploration

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
ε-greedy is the behaviour policy in Q-learning and SARSA ([[q-learning]], [[sarsa]]).
''',
"statement": r'''
Implement:
* `epsilon_greedy(q_values, epsilon, rng)` → int action following the recipe (one `rng.random()`
  call, then `rng.integers(n)` only when exploring).
* `epsilon_greedy_probs(q_values, epsilon)` → probability array as described.
Raise `ValueError` unless `0 <= epsilon <= 1` and `q_values` is non-empty.

**Examples**
```python
epsilon_greedy_probs([1, 5, 2], 0.3)               # [0.1, 0.8, 0.1]
epsilon_greedy([1, 5, 2], 0.0, np.random.default_rng(0))   # 1
```
''',
"starter": r'''
import numpy as np


def epsilon_greedy(q_values, epsilon, rng):
    pass


def epsilon_greedy_probs(q_values, epsilon):
    pass
''',
"hints": [
    "`q = np.asarray(q_values)`; `n = len(q)`.",
    "`if rng.random() < epsilon: return int(rng.integers(n))`.",
    "Probs: `p = np.full(n, epsilon / n); p[np.argmax(q)] += 1 - epsilon`.",
],
"solution": r'''
import numpy as np


def _check(q_values, epsilon):
    q = np.asarray(q_values, dtype=float)
    if q.size == 0 or not 0 <= epsilon <= 1:
        raise ValueError("need non-empty q_values and 0 <= epsilon <= 1")
    return q


def epsilon_greedy(q_values, epsilon, rng):
    q = _check(q_values, epsilon)
    if rng.random() < epsilon:
        return int(rng.integers(len(q)))
    return int(np.argmax(q))


def epsilon_greedy_probs(q_values, epsilon):
    q = _check(q_values, epsilon)
    p = np.full(len(q), epsilon / len(q))
    p[int(np.argmax(q))] += 1 - epsilon
    return p
''',
"explanation": r'''
One uniform draw decides between exploring and exploiting; exploration samples any action uniformly,
including the greedy one. The probability vector follows directly from that procedure.
''',
"tests": r'''
import numpy as np

class TestEpsGreedy(unittest.TestCase):
    def test_probs(self):
        np.testing.assert_allclose(S.epsilon_greedy_probs([1, 5, 2], 0.3), [0.1, 0.8, 0.1])

    def test_greedy(self):
        self.assertEqual(S.epsilon_greedy([1, 5, 2], 0.0, np.random.default_rng(0)), 1)

    def test_ties_lowest(self):
        self.assertEqual(S.epsilon_greedy([3, 3, 1], 0.0, np.random.default_rng(0)), 0)

    def test_recipe(self):
        rng_a, rng_b = np.random.default_rng(5), np.random.default_rng(5)
        for _ in range(50):
            got = S.epsilon_greedy([0., 1., 0.5, 0.2], 0.4, rng_a)
            exp = int(rng_b.integers(4)) if rng_b.random() < 0.4 else 1
            self.assertEqual(got, exp)

    def test_frequencies(self):
        rng = np.random.default_rng(1)
        counts = np.bincount([S.epsilon_greedy([1, 5, 2], 0.3, rng) for _ in range(30000)], minlength=3) / 30000
        np.testing.assert_allclose(counts, [0.1, 0.8, 0.1], atol=0.01)

    def test_full_exploration(self):
        np.testing.assert_allclose(S.epsilon_greedy_probs([9, 0, 0, 0], 1.0), 0.25)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.epsilon_greedy_probs([], 0.1)
        with self.assertRaises(ValueError):
            S.epsilon_greedy([1], 1.5, np.random.default_rng(0))
''',
"feedback": [
    ("test_recipe", "Draw rng.random() first; call rng.integers(n) only when exploring."),
    ("test_probs", "Greedy action gets 1 − ε + ε/|A|; others ε/|A|."),
    ("test_ties_lowest", "np.argmax returns the lowest index on ties."),
    ("test_frequencies", "Random exploration chooses among all actions, including the greedy one."),
],
},
# ---------------------------------------------------------------- gridworld-step
{
"slug": "gridworld-step", "title": "Gridworld Transition Function",
"difficulty": "beginner", "prereqs": ["discounted-return"], "packages": [],
"objectives": ["Encode an environment as states, actions, rewards and terminal flags",
               "Implement deterministic transitions with walls and boundaries", "Build the full transition table P"],
"tags": ["environments", "mdp", "gridworld", "transitions"],
"sources": ["S033", "S035"], "entry": "class GridWorld(rows): step(state, action), build_P()",
"article": r'''
# A Gridworld Environment

## Intuition
An RL environment answers one question: "If I'm here and do this, where do I end up, what reward do I
get, and is the episode over?" A gridworld answers it with a map.

## Precise explanation
Map as strings: `.` empty, `#` wall, `S` start, `G` goal (+10, terminal), `X` pit (−10, terminal).
Every other move costs −1. States are indices `r * n_cols + c`. Actions: 0 = up, 1 = right,
2 = down, 3 = left. Moving into a wall or off the grid leaves the agent in place (still −1).
Stepping from a terminal state is not allowed (episodes end there).

**Transition table:** `P[s][a] = [(1.0, s', r, done)]` for this deterministic world (Sutton & Barto's
four-argument dynamics $p(s', r \mid s, a)$ written as a list). Terminal and wall states map every action
to themselves with reward 0 and `done=True` so that algorithms can iterate over all states safely.

```text
S . . G        state ids:  0  1  2  3
. # . X                    4  5  6  7
```

## Worked example
From state 0, action right → state 1, reward −1, not done. From 2, right → 3 (goal), +10, done.
From 4, right → wall at 5 → stays 4, −1.

## Common mistakes
* Row/column confusion in state ids.
* Treating the goal reward as +10 −1 (choose one convention and document it; here +10).
* Allowing movement through walls.

## Why this matters
[[policy-evaluation]] … [[policy-iteration]] all run on environments built this way; Gymnasium environments expose the same
`step` interface idea.
''',
"statement": r'''
Implement `class GridWorld(rows)` (list of equal-length strings) with attributes `n_rows`, `n_cols`,
`n_states`, `start` (state id of `S`), methods:
* `step(state, action)` → `(next_state, reward, done)` per the rules; raise `ValueError` for invalid
  action/state, a wall state, or a terminal state.
* `build_P()` → dict `P[s][a] = [(1.0, s', r, done)]` for all states (terminal/wall states map to
  themselves with reward 0.0 and `done=True`).

**Example**
```python
g = GridWorld(["S..G", ".#.X"])
g.step(0, 1)   # (1, -1.0, False)
g.step(2, 1)   # (3, 10.0, True)
g.step(4, 1)   # (4, -1.0, False)  — blocked by wall
```
''',
"starter": r'''
MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


class GridWorld:
    def __init__(self, rows):
        # TODO
        pass

    def step(self, state, action):
        # TODO
        pass

    def build_P(self):
        # TODO
        return {}
''',
"hints": [
    "Store `self.grid = rows`; `cell(s)` returns `rows[s // n_cols][s % n_cols]`.",
    "Target `(r + dr, c + dc)`; if outside or a wall, stay.",
    "Reward/done from the target cell: G → (10, True), X → (−10, True), else (−1, False).",
],
"solution": r'''
MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


class GridWorld:
    def __init__(self, rows):
        if not rows or len({len(r) for r in rows}) != 1:
            raise ValueError("rows must be non-empty and equal length")
        self.grid = list(rows)
        self.n_rows, self.n_cols = len(rows), len(rows[0])
        self.n_states = self.n_rows * self.n_cols
        starts = [i for i in range(self.n_states) if self.cell(i) == "S"]
        self.start = starts[0] if starts else 0

    def cell(self, s):
        return self.grid[s // self.n_cols][s % self.n_cols]

    def is_terminal(self, s):
        return self.cell(s) in "GX"

    def step(self, state, action):
        if action not in MOVES or not 0 <= state < self.n_states:
            raise ValueError("invalid state or action")
        if self.cell(state) == "#" or self.is_terminal(state):
            raise ValueError("cannot step from a wall or terminal state")
        r, c = divmod(state, self.n_cols)
        dr, dc = MOVES[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.n_rows and 0 <= nc < self.n_cols and self.grid[nr][nc] != "#":
            nxt = nr * self.n_cols + nc
        else:
            nxt = state
        ch = self.cell(nxt)
        if ch == "G":
            return nxt, 10.0, True
        if ch == "X":
            return nxt, -10.0, True
        return nxt, -1.0, False

    def build_P(self):
        P = {}
        for s in range(self.n_states):
            P[s] = {}
            for a in MOVES:
                if self.cell(s) == "#" or self.is_terminal(s):
                    P[s][a] = [(1.0, s, 0.0, True)]
                else:
                    P[s][a] = [(1.0, *self.step(s, a))]
        return P
''',
"explanation": r'''
States are flattened grid coordinates. A move is applied unless it leaves the grid or hits a wall;
the destination cell determines reward and termination. The transition table enumerates `step` for
every state–action pair and makes walls and terminal states absorbing with zero reward.
''',
"tests": r'''
ROWS = ["S..G", ".#.X"]

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.g = S.GridWorld(ROWS)

    def test_dims(self):
        self.assertEqual((self.g.n_rows, self.g.n_cols, self.g.n_states, self.g.start), (2, 4, 8, 0))

    def test_moves(self):
        self.assertEqual(self.g.step(0, 1), (1, -1.0, False))
        self.assertEqual(self.g.step(0, 2), (4, -1.0, False))

    def test_goal_and_pit(self):
        self.assertEqual(self.g.step(2, 1), (3, 10.0, True))
        self.assertEqual(self.g.step(6, 1), (7, -10.0, True))

    def test_walls_and_bounds(self):
        self.assertEqual(self.g.step(4, 1), (4, -1.0, False))
        self.assertEqual(self.g.step(0, 0), (0, -1.0, False))
        self.assertEqual(self.g.step(0, 3), (0, -1.0, False))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            self.g.step(3, 0)
        with self.assertRaises(ValueError):
            self.g.step(0, 7)

    def test_P(self):
        P = self.g.build_P()
        self.assertEqual(P[2][1], [(1.0, 3, 10.0, True)])
        self.assertEqual(P[3][0], [(1.0, 3, 0.0, True)])
        self.assertEqual(P[5][2], [(1.0, 5, 0.0, True)])
        self.assertEqual(len(P), 8)
        self.assertTrue(all(len(P[s]) == 4 for s in P))
''',
"feedback": [
    ("test_moves", "State id = row * n_cols + col; action 1 = right, 2 = down."),
    ("test_walls_and_bounds", "Moves into walls or off-grid keep the agent in place with reward −1."),
    ("test_goal_and_pit", "Goal gives +10 and pit −10, both terminal."),
    ("test_P", "Terminal and wall states map to themselves with reward 0 and done=True."),
],
},
# ---------------------------------------------------------------- bandit-incremental
{
"slug": "bandit-incremental", "title": "Incremental Value Estimates",
"difficulty": "intermediate", "prereqs": ["epsilon-greedy"], "packages": ["numpy"],
"objectives": ["Update sample-average estimates incrementally", "Use a constant step size for non-stationary rewards",
               "Track action counts"],
"tags": ["bandits", "incremental-mean", "step-size"],
"sources": ["S033"], "entry": "class ValueEstimates(n_actions, alpha=None): update(a, r), q, n",
"article": r'''
# Incremental Estimates for Bandits

## Intuition
A slot machine's average payout can be tracked without storing every result: nudge the estimate
towards each new reward by a fraction of the error.

## Precise explanation (Sutton & Barto, §2.4–2.5)
Sample average after n rewards: $Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)$ — exactly the mean, using
O(1) memory. General form "NewEstimate ← OldEstimate + StepSize · (Target − OldEstimate)".
With a **constant** step size α, recent rewards weigh more (exponential recency-weighted average),
which tracks changing (non-stationary) reward distributions:
$Q_{n+1} = Q_n + \alpha(R_n - Q_n)$.

## Worked example
Rewards for one arm: 2, 4, 6. Sample average: 0 → 2 → 3 → 4. α = 0.5 from 0: 1 → 2.5 → 4.25.

## Common mistakes
* Incrementing the count after computing 1/n (off by one).
* Sharing one count across all arms.
* Using 1/n on non-stationary problems (adapts too slowly).

## Why this matters
This update pattern is the seed of TD learning and Q-learning ([[td0-prediction]], [[q-learning]]).
''',
"statement": r'''
Implement `class ValueEstimates(n_actions, alpha=None)` with arrays `q` (zeros) and `n` (int zeros)
and method `update(a, r)` that increments `n[a]` and updates `q[a]` with step `1/n[a]` (if `alpha`
is None) or `alpha`. Return the new `q[a]`. Raise `ValueError` for an invalid action or
`alpha` not in `(0, 1]`.

**Example**
```python
v = ValueEstimates(2)
[v.update(0, r) for r in (2, 4, 6)]       # [2.0, 3.0, 4.0]
w = ValueEstimates(1, alpha=0.5)
[w.update(0, r) for r in (2, 4, 6)]       # [1.0, 2.5, 4.25]
```
''',
"starter": r'''
import numpy as np


class ValueEstimates:
    def __init__(self, n_actions, alpha=None):
        pass

    def update(self, a, r):
        pass
''',
"hints": [
    "`self.q = np.zeros(n_actions)`; `self.n = np.zeros(n_actions, dtype=int)`.",
    "Increment `self.n[a]` first, then `step = 1 / self.n[a]` (or alpha).",
    "`self.q[a] += step * (r - self.q[a])`.",
],
"solution": r'''
import numpy as np


class ValueEstimates:
    def __init__(self, n_actions, alpha=None):
        if alpha is not None and not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self.q = np.zeros(n_actions)
        self.n = np.zeros(n_actions, dtype=int)
        self.alpha = alpha

    def update(self, a, r):
        if not 0 <= a < len(self.q):
            raise ValueError("invalid action")
        self.n[a] += 1
        step = 1.0 / self.n[a] if self.alpha is None else self.alpha
        self.q[a] += step * (r - self.q[a])
        return float(self.q[a])
''',
"explanation": r'''
Incrementing the count before computing 1/n makes the first update replace the initial zero with the
first reward, and later updates reproduce the running mean exactly. A constant α instead gives an
exponentially weighted average.
''',
"tests": r'''
import numpy as np

class TestIncremental(unittest.TestCase):
    def test_sample_average(self):
        v = S.ValueEstimates(2)
        self.assertEqual([v.update(0, r) for r in (2, 4, 6)], [2.0, 3.0, 4.0])
        self.assertEqual(v.n.tolist(), [3, 0])

    def test_constant_alpha(self):
        w = S.ValueEstimates(1, alpha=0.5)
        self.assertEqual([w.update(0, r) for r in (2, 4, 6)], [1.0, 2.5, 4.25])

    def test_equals_mean(self):
        rng = np.random.default_rng(0)
        rs = rng.normal(size=500)
        v = S.ValueEstimates(1)
        for r in rs:
            v.update(0, r)
        self.assertAlmostEqual(v.q[0], rs.mean(), places=10)

    def test_tracks_change(self):
        a, b = S.ValueEstimates(1), S.ValueEstimates(1, alpha=0.1)
        for r in [0.0] * 500 + [10.0] * 100:
            a.update(0, r); b.update(0, r)
        self.assertGreater(b.q[0], 9.0)
        self.assertLess(a.q[0], 2.0)

    def test_independent_arms(self):
        v = S.ValueEstimates(3)
        v.update(2, 5.0)
        self.assertEqual(v.q.tolist(), [0.0, 0.0, 5.0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ValueEstimates(2).update(2, 1.0)
        with self.assertRaises(ValueError):
            S.ValueEstimates(2, alpha=0.0)
''',
"feedback": [
    ("test_sample_average", "Increment n[a] before computing the 1/n step."),
    ("test_constant_alpha", "With alpha set, use it as a constant step size."),
    ("test_tracks_change", "Constant α forgets old rewards; 1/n does not."),
    ("test_independent_arms", "Keep separate counts and estimates per action."),
],
},
# ---------------------------------------------------------------- policy-evaluation
{
"slug": "policy-evaluation", "title": "Iterative Policy Evaluation",
"difficulty": "intermediate", "prereqs": ["gridworld-step", "discounted-return"], "packages": ["numpy"],
"objectives": ["Apply the Bellman expectation backup", "Iterate to convergence with a tolerance",
               "Handle terminal transitions correctly"],
"tags": ["dynamic-programming", "bellman-equation", "policy-evaluation", "mdp"],
"sources": ["S033", "S034"], "entry": "policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000)",
"article": r'''
# Iterative Policy Evaluation

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
Policy evaluation is half of policy iteration ([[policy-iteration]]) and the conceptual basis of TD learning.
''',
"statement": r'''
Write `policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000)` returning
`(V, n_iter)` where `P` uses the topic's format, `policy` is an array `(n_states, n_actions)` of
probabilities, and `V` a float array. Synchronous sweeps; stop when the max change `< theta`.
Raise `ValueError` if a policy row does not sum to 1 (tolerance 1e-8) or `gamma` not in `[0, 1)`.

**Example**
```python
P = {0: {0: [(1.0, 1, -1.0, False)]}, 1: {0: [(1.0, 2, 10.0, True)]}, 2: {0: [(1.0, 2, 0.0, True)]}}
V, _ = policy_evaluation(P, np.ones((3, 1)), gamma=0.9)
V   # [8., 10., 0.]
```
''',
"starter": r'''
import numpy as np


def policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000):
    pass
''',
"hints": [
    "`V = np.zeros(n_states)`; each sweep build `new = np.zeros_like(V)`.",
    "`new[s] += policy[s, a] * p * (r + gamma * (0 if done else V[s2]))`.",
    "Stop when `np.max(np.abs(new - V)) < theta`.",
],
"solution": r'''
import numpy as np


def policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000):
    policy = np.asarray(policy, dtype=float)
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    if not np.allclose(policy.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("policy rows must sum to 1")
    n = len(P)
    V = np.zeros(n)
    for it in range(1, max_iter + 1):
        new = np.zeros(n)
        for s in range(n):
            for a, outcomes in P[s].items():
                pa = policy[s, a]
                if pa == 0:
                    continue
                for p, s2, r, done in outcomes:
                    new[s] += pa * p * (r + gamma * (0.0 if done else V[s2]))
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            return V, it
    return V, max_iter
''',
"explanation": r'''
Each sweep computes, for every state, the policy-weighted expected one-step reward plus discounted
next-state value, using the previous sweep's values. Terminal transitions contribute only their
reward. Iteration stops once values change by less than θ.
''',
"tests": r'''
import numpy as np

CORR = {0: {0: [(1.0, 1, -1.0, False)]}, 1: {0: [(1.0, 2, 10.0, True)]}, 2: {0: [(1.0, 2, 0.0, True)]}}

class TestPolicyEval(unittest.TestCase):
    def test_corridor(self):
        V, _ = S.policy_evaluation(CORR, np.ones((3, 1)), gamma=0.9)
        np.testing.assert_allclose(V, [8., 10., 0.])

    def test_stochastic_policy(self):
        P = {0: {0: [(1.0, 1, 1.0, True)], 1: [(1.0, 1, 3.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)], 1: [(1.0, 1, 0.0, True)]}}
        V, _ = S.policy_evaluation(P, np.array([[0.25, 0.75], [0.5, 0.5]]), gamma=0.5)
        np.testing.assert_allclose(V, [2.5, 0.0])

    def test_stochastic_transitions(self):
        P = {0: {0: [(0.5, 0, 1.0, False), (0.5, 1, 0.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)]}}
        V, _ = S.policy_evaluation(P, np.ones((2, 1)), gamma=0.9)
        self.assertAlmostEqual(V[0], 0.5 / (1 - 0.45), places=8)

    def test_bellman_fixed_point(self):
        P = {0: {0: [(1.0, 0, 1.0, False)]}}
        V, _ = S.policy_evaluation(P, np.ones((1, 1)), gamma=0.8)
        self.assertAlmostEqual(V[0], 5.0, places=8)

    def test_iterations_reported(self):
        _, it = S.policy_evaluation(CORR, np.ones((3, 1)), gamma=0.9)
        self.assertTrue(1 <= it <= 5)

    def test_bad_policy(self):
        with self.assertRaises(ValueError):
            S.policy_evaluation(CORR, np.full((3, 1), 0.5))
''',
"feedback": [
    ("test_corridor", "Don't bootstrap from transitions with done=True."),
    ("test_stochastic_policy", "Weight each action's backup by π(a|s)."),
    ("test_stochastic_transitions", "Weight each outcome by its probability p."),
    ("test_bellman_fixed_point", "Keep sweeping until the max change is below θ."),
],
},
# ---------------------------------------------------------------- value-iteration
{
"slug": "value-iteration", "title": "Value Iteration",
"difficulty": "intermediate", "prereqs": ["policy-evaluation"], "packages": ["numpy"],
"objectives": ["Apply the Bellman optimality backup", "Extract a greedy policy from values",
               "Solve a small gridworld optimally"],
"tags": ["dynamic-programming", "value-iteration", "optimal-policy", "bellman-optimality"],
"sources": ["S033", "S034"], "entry": "q_from_v(P, V, gamma); value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000)",
"article": r'''
# Value Iteration

## Intuition
Instead of evaluating a fixed policy, assume you will always pick the best action. Repeatedly update
each state's value with the best one-step lookahead; the values converge to the optimal ones, and
acting greedily on them is optimal.

## Precise explanation (Sutton & Barto, §4.4)
$$Q(s, a) = \sum_{(p, s', r, d)} p\,[r + \gamma(1-d)V(s')],\qquad V_{k+1}(s) = \max_a Q_k(s, a).$$
Stop when the max change < θ; then the **greedy policy** $\pi(s) = \arg\max_a Q(s, a)$ (ties →
lowest action) is optimal (for small enough θ).

```mermaid
flowchart LR
  V[V_k] --> Q["Q(s,a) = Σ p[r + γV(s')]"] --> M["V_{k+1}(s) = max_a Q"] --> C{converged?}
  C -- no --> V
  C -- yes --> G["π(s) = argmax_a Q(s,a)"]
```

## Worked example
Corridor with "left" (stay, −1) and "right" (towards goal): optimal values match always-right
evaluation ([[policy-evaluation]]); greedy policy = right everywhere.

## Common mistakes
* Taking the max over next states instead of over actions.
* Extracting the policy from stale values.
* Including terminal successors' values.

## Why this matters
Value iteration is the prototypical planning algorithm and the dynamic-programming ancestor of
Q-learning.
''',
"statement": r'''
Implement:
* `q_from_v(P, V, gamma)` → array `(n_states, n_actions)` of one-step lookahead values (all states
  have the same action set).
* `value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000)` → `(V, policy)` where `policy` is an
  int array of greedy actions (ties → lowest). Synchronous updates.

**Example**
```python
g = GridWorld(["S..G", ".#.X"])     # from [[gridworld-step]] (provide your own copy or use P directly)
V, pi = value_iteration(g.build_P(), gamma=0.9)
pi[0], pi[1], pi[2]                 # (1, 1, 1)  — go right towards G
```
''',
"starter": r'''
import numpy as np


def q_from_v(P, V, gamma):
    pass


def value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000):
    pass
''',
"hints": [
    "`nA = len(P[0])`; `Q = np.zeros((nS, nA))`.",
    "`Q[s, a] = sum(p * (r + gamma * (0 if d else V[s2])) for p, s2, r, d in P[s][a])`.",
    "Loop: `Q = q_from_v(P, V, gamma); new = Q.max(axis=1)`; policy = `q_from_v(P, V, gamma).argmax(axis=1)`.",
],
"solution": r'''
import numpy as np


def q_from_v(P, V, gamma):
    nS, nA = len(P), len(P[0])
    Q = np.zeros((nS, nA))
    for s in range(nS):
        for a in range(nA):
            Q[s, a] = sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][a])
    return Q


def value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000):
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    V = np.zeros(len(P))
    for _ in range(max_iter):
        new = q_from_v(P, V, gamma).max(axis=1)
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            break
    return V, q_from_v(P, V, gamma).argmax(axis=1)
''',
"explanation": r'''
The lookahead helper computes Q from V for every state–action pair. Each sweep replaces V with the
row-wise maximum of Q; after convergence, argmax of Q gives the optimal greedy policy with the
lowest-index tie-break.
''',
"tests": r'''
import numpy as np

MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

def grid_P(rows):
    R, C = len(rows), len(rows[0]); P = {}
    for s in range(R * C):
        r, c = divmod(s, C); ch = rows[r][c]; P[s] = {}
        for a, (dr, dc) in MOVES.items():
            if ch in "#GX":
                P[s][a] = [(1.0, s, 0.0, True)]; continue
            nr, nc = r + dr, c + dc
            ns = nr * C + nc if 0 <= nr < R and 0 <= nc < C and rows[nr][nc] != "#" else s
            t = rows[ns // C][ns % C]
            P[s][a] = [(1.0, ns, 10.0, True)] if t == "G" else [(1.0, ns, -10.0, True)] if t == "X" else [(1.0, ns, -1.0, False)]
    return P

class TestVI(unittest.TestCase):
    def test_grid_policy(self):
        V, pi = S.value_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        self.assertEqual((pi[0], pi[1], pi[2]), (1, 1, 1))
        self.assertEqual(pi[6], 0)

    def test_grid_values(self):
        V, _ = S.value_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        self.assertAlmostEqual(V[2], 10.0)
        self.assertAlmostEqual(V[1], -1 + 0.9 * 10)
        self.assertAlmostEqual(V[0], -1 + 0.9 * (-1 + 9))

    def test_q_from_v(self):
        P = {0: {0: [(1.0, 1, 2.0, False)], 1: [(0.5, 1, 0.0, False), (0.5, 0, 4.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)], 1: [(1.0, 1, 0.0, True)]}}
        Q = S.q_from_v(P, np.array([0.0, 10.0]), 0.5)
        np.testing.assert_allclose(Q, [[7.0, 4.5], [0.0, 0.0]])

    def test_bellman_optimality(self):
        P = grid_P(["S..", ".X.", "..G"])
        V, _ = S.value_iteration(P, gamma=0.95)
        np.testing.assert_allclose(V, S.q_from_v(P, V, 0.95).max(axis=1), atol=1e-8)

    def test_avoids_pit(self):
        _, pi = S.value_iteration(grid_P(["S.X", "...", "..G"]), gamma=0.9)
        self.assertEqual(pi[1], 2)

    def test_ties_lowest(self):
        P = {0: {0: [(1.0, 0, 1.0, True)], 1: [(1.0, 0, 1.0, True)]}}
        self.assertEqual(S.value_iteration(P)[1][0], 0)
''',
"feedback": [
    ("test_grid_values", "V(s) = max_a Σ p[r + γ(1−done)V(s')]."),
    ("test_q_from_v", "Sum over outcomes weighted by probability; terminal outcomes don't bootstrap."),
    ("test_avoids_pit", "The greedy policy uses argmax over actions of Q."),
    ("test_ties_lowest", "np.argmax gives the lowest action on ties."),
],
},
# ---------------------------------------------------------------- mc-first-visit
{
"slug": "mc-first-visit", "title": "First-Visit Monte Carlo Prediction",
"difficulty": "advanced", "prereqs": ["env-interface", "policy-evaluation"], "packages": ["numpy"],
"objectives": ["Estimate values by averaging sampled returns", "Implement the first-visit rule",
               "Compare with every-visit estimates"],
"tags": ["monte-carlo", "prediction", "returns", "sampling"],
"sources": ["S033"], "entry": "mc_prediction(episodes, n_states, gamma, first_visit=True)",
"article": r'''
# Monte Carlo Prediction

## Intuition
Don't know the environment's rules? Play complete episodes, record the return that followed each
visit to a state, and average. With enough episodes the averages approach the true values.

## Precise explanation (Sutton & Barto, §5.1)
An episode is a list of `(state, reward)` pairs: the state at time t and the reward received after
acting there, $R_{t+1}$. Compute returns backwards ([[discounted-return]]). **First-visit MC** averages, for each state,
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
''',
"statement": r'''
Write `mc_prediction(episodes, n_states, gamma, first_visit=True)` returning `(V, counts)` arrays
(`V[s] = 0` and `counts[s] = 0` for unvisited states). Raise `ValueError` for `gamma` outside
`[0, 1]`.

**Example**
```python
eps = [[(0, 1), (1, 0), (0, 2)], [(1, 5)]]
mc_prediction(eps, 2, 1.0)[0]                      # [3. , 3.5]
mc_prediction(eps, 2, 1.0, first_visit=False)[0]   # [2.5, 3.5]
```
''',
"starter": r'''
import numpy as np


def mc_prediction(episodes, n_states, gamma, first_visit=True):
    pass
''',
"hints": [
    "For each episode compute `G_t` for all t with a backward pass.",
    "First visit: find `first = {}` mapping state → earliest t.",
    "Keep `sums[s]` and `counts[s]`; V = sums / counts where counts > 0.",
],
"solution": r'''
import numpy as np


def mc_prediction(episodes, n_states, gamma, first_visit=True):
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be in [0, 1]")
    sums = np.zeros(n_states)
    counts = np.zeros(n_states, dtype=int)
    for ep in episodes:
        G = 0.0
        returns = [0.0] * len(ep)
        for t in range(len(ep) - 1, -1, -1):
            G = ep[t][1] + gamma * G
            returns[t] = G
        seen = set()
        for t, (s, _) in enumerate(ep):
            if first_visit and s in seen:
                continue
            seen.add(s)
            sums[s] += returns[t]
            counts[s] += 1
    V = np.divide(sums, counts, out=np.zeros(n_states), where=counts > 0)
    return V, counts
''',
"explanation": r'''
A backward pass gives the return at every time step. Scanning forward, the first-visit rule skips
repeated states within an episode. Running sums and counts produce averages; unvisited states stay 0.
''',
"tests": r'''
import numpy as np

EPS = [[(0, 1), (1, 0), (0, 2)], [(1, 5)]]

class TestMC(unittest.TestCase):
    def test_first_visit(self):
        V, c = S.mc_prediction(EPS, 2, 1.0)
        np.testing.assert_allclose(V, [3.0, 3.5])
        np.testing.assert_array_equal(c, [1, 2])

    def test_every_visit(self):
        V, c = S.mc_prediction(EPS, 2, 1.0, first_visit=False)
        np.testing.assert_allclose(V, [2.5, 3.5])
        np.testing.assert_array_equal(c, [2, 2])

    def test_discount(self):
        V, _ = S.mc_prediction([[(0, 1), (1, 1), (2, 1)]], 3, 0.5)
        np.testing.assert_allclose(V, [1.75, 1.5, 1.0])

    def test_unvisited(self):
        V, c = S.mc_prediction(EPS, 4, 1.0)
        self.assertEqual((V[3], c[3]), (0.0, 0))

    def test_converges(self):
        rng = np.random.default_rng(0)
        eps = []
        for _ in range(4000):
            eps.append([(0, 0.0), (1, float(rng.random() < 0.3))])
        V, _ = S.mc_prediction(eps, 2, 0.9)
        self.assertAlmostEqual(V[1], 0.3, delta=0.03)
        self.assertAlmostEqual(V[0], 0.27, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.mc_prediction(EPS, 2, 1.1)
''',
"feedback": [
    ("test_first_visit", "Only the first occurrence of each state per episode counts."),
    ("test_discount", "Return at t is R_{t+1} + γG_{t+1}; compute backwards."),
    ("test_every_visit", "With first_visit=False every occurrence adds its return."),
    ("test_unvisited", "Unvisited states keep V = 0 and count 0."),
],
},
# ---------------------------------------------------------------- ucb-bandit
{
"slug": "ucb-bandit", "title": "UCB1 Bandit",
"difficulty": "intermediate", "prereqs": ["bandit-incremental"], "packages": ["numpy"],
"objectives": ["Select actions by optimism in the face of uncertainty", "Implement UCB1 with initial exploration of every arm",
               "Measure cumulative regret"],
"tags": ["bandits", "ucb", "exploration", "regret"],
"sources": ["S033"], "entry": "ucb_select(q, n, t, c=2.0); run_bandit(means, steps, seed, policy='ucb', epsilon=0.1, c=2.0)",
"article": r'''
# Upper Confidence Bound (UCB)

## Intuition
Prefer arms that are either good *or* poorly explored. UCB adds an exploration bonus that shrinks the
more often an arm is tried — "optimism in the face of uncertainty".

## Precise explanation (Sutton & Barto, §2.7)
At time t (1-based count of pulls so far + 1), choose
$$A_t = \arg\max_a \left[Q(a) + c\sqrt{\frac{\ln t}{N(a)}}\right],$$
with any arm having $N(a) = 0$ chosen first (lowest index). Ties → lowest index.
**Regret** after T steps: $T\mu^* - \sum_t \mu_{A_t}$ — reward lost compared with always pulling the
best arm. UCB's regret grows logarithmically; ε-greedy with constant ε grows linearly.

Simulation here: Bernoulli arms with success probabilities `means`; reward = 1 if
`rng.random() < means[a]` else 0 (one draw per step, after choosing the action).

## Worked example
Q = [0.5, 0.4], N = [10, 2], t = 13, c = 2: bonuses 2√(ln13/10) ≈ 1.01 and 2√(ln13/2) ≈ 2.26 →
scores 1.51 vs 2.66 → explore arm 1.

## Common mistakes
* Dividing by zero for untried arms.
* Using ln of the per-arm count instead of total time.
* Forgetting to update counts after pulling.

## Why this matters
UCB ideas power Monte Carlo tree search (AlphaGo) and many recommendation/A-B testing systems.
''',
"statement": r'''
Implement:
* `ucb_select(q, n, t, c=2.0)` → int arm per the rule above.
* `run_bandit(means, steps, seed, policy="ucb", epsilon=0.1, c=2.0)` → dict
  `{"actions": list, "rewards": list, "regret": float}`.
  `rng = np.random.default_rng(seed)`; per step t = 1..steps: choose (UCB uses `t`; "egreedy" uses
  [[epsilon-greedy]]'s recipe with the same rng *before* the reward draw), then reward `float(rng.random() < means[a])`,
  then update sample-average estimates. Regret uses the **true means** of chosen arms.

**Example**
```python
ucb_select(np.array([0.5, 0.4]), np.array([10, 2]), 13)   # 1
r = run_bandit([0.2, 0.8], 1000, seed=0)
r["actions"].count(1) > 900     # True
```
''',
"starter": r'''
import math

import numpy as np


def ucb_select(q, n, t, c=2.0):
    pass


def run_bandit(means, steps, seed, policy="ucb", epsilon=0.1, c=2.0):
    pass
''',
"hints": [
    "Untried arms: `zeros = np.flatnonzero(n == 0)`; return `zeros[0]` if any.",
    "Scores: `q + c * np.sqrt(np.log(t) / n)`; `np.argmax`.",
    "Update: `n[a] += 1; q[a] += (r - q[a]) / n[a]`; regret = `steps*max(means) - sum(means[a])`.",
],
"solution": r'''
import math

import numpy as np


def ucb_select(q, n, t, c=2.0):
    q = np.asarray(q, dtype=float)
    n = np.asarray(n)
    zeros = np.flatnonzero(n == 0)
    if zeros.size:
        return int(zeros[0])
    return int(np.argmax(q + c * np.sqrt(math.log(t) / n)))


def run_bandit(means, steps, seed, policy="ucb", epsilon=0.1, c=2.0):
    if policy not in ("ucb", "egreedy"):
        raise ValueError("policy must be 'ucb' or 'egreedy'")
    means = np.asarray(means, dtype=float)
    k = len(means)
    rng = np.random.default_rng(seed)
    q, n = np.zeros(k), np.zeros(k, dtype=int)
    actions, rewards = [], []
    for t in range(1, steps + 1):
        if policy == "ucb":
            a = ucb_select(q, n, t, c)
        elif rng.random() < epsilon:
            a = int(rng.integers(k))
        else:
            a = int(np.argmax(q))
        r = float(rng.random() < means[a])
        n[a] += 1
        q[a] += (r - q[a]) / n[a]
        actions.append(a)
        rewards.append(r)
    regret = steps * float(means.max()) - float(means[actions].sum())
    return {"actions": actions, "rewards": rewards, "regret": regret}
''',
"explanation": r'''
UCB first tries every arm once, then adds a confidence bonus that is large for rarely tried arms and
grows slowly with time. The simulation draws rewards from one seeded generator, updates sample
averages, and reports regret against the best arm's true mean.
''',
"tests": r'''
import numpy as np

class TestUCB(unittest.TestCase):
    def test_select(self):
        self.assertEqual(S.ucb_select(np.array([0.5, 0.4]), np.array([10, 2]), 13), 1)

    def test_untried_first(self):
        self.assertEqual(S.ucb_select(np.array([9., 0., 0.]), np.array([5, 3, 0]), 9), 2)
        self.assertEqual(S.ucb_select(np.zeros(3), np.zeros(3, int), 1), 0)

    def test_exploit_when_confident(self):
        self.assertEqual(S.ucb_select(np.array([0.9, 0.1]), np.array([1000, 1000]), 2001), 0)

    def test_learns_best(self):
        r = S.run_bandit([0.2, 0.8], 1000, seed=0)
        self.assertGreater(r["actions"].count(1), 900)

    def test_regret_definition(self):
        r = S.run_bandit([0.1, 0.5, 0.3], 200, seed=4)
        means = np.array([0.1, 0.5, 0.3])
        self.assertAlmostEqual(r["regret"], 200 * 0.5 - means[r["actions"]].sum())

    def test_ucb_beats_egreedy(self):
        means = [0.2, 0.8]
        ucb = np.mean([S.run_bandit(means, 3000, s)["regret"] for s in range(5)])
        eg = np.mean([S.run_bandit(means, 3000, s, policy="egreedy", epsilon=0.3)["regret"] for s in range(5)])
        self.assertLess(ucb, eg)

    def test_reproducible(self):
        a = S.run_bandit([0.3, 0.6], 100, 9)
        self.assertEqual(a, S.run_bandit([0.3, 0.6], 100, 9))
''',
"feedback": [
    ("test_untried_first", "Arms with N = 0 must be selected before computing bonuses."),
    ("test_select", "Bonus = c·sqrt(ln t / N(a)) using the total time t."),
    ("test_regret_definition", "Regret uses true means of the chosen arms, not observed rewards."),
    ("test_learns_best", "Update counts and sample averages after every pull."),
],
},
# ---------------------------------------------------------------- td0-prediction
{
"slug": "td0-prediction", "title": "TD(0) Prediction",
"difficulty": "advanced", "prereqs": ["policy-evaluation", "mc-first-visit"], "packages": ["numpy"],
"objectives": ["Update values from single transitions (bootstrapping)", "Implement the TD error",
               "Compare TD(0) with Monte Carlo on the same experience"],
"tags": ["temporal-difference", "td-learning", "bootstrapping", "prediction"],
"sources": ["S033"], "entry": "td_error(V, s, r, s_next, done, gamma); td0(transitions_episodes, n_states, alpha, gamma, sweeps=1)",
"article": r'''
# TD(0): Learning from Every Step

## Intuition
Monte Carlo waits until the end of an episode. TD learning updates immediately after each step, using
its own current estimate of the next state's value as a stand-in for the rest of the return —
"learning a guess from a guess" (bootstrapping).

## Precise explanation (Sutton & Barto, §6.1)
For a transition $(s, r, s', d)$:
$$\delta = r + \gamma(1-d)V(s') - V(s),\qquad V(s) \leftarrow V(s) + \alpha\,\delta.$$
δ is the **TD error**. Transitions are processed in order, updating V in place. With a decaying (or
small) α and enough experience, TD(0) converges to $V^\pi$; on finite batches repeated many times
(batch TD) it converges to the certainty-equivalence estimate, which can differ from the MC average.

## Worked example
V = [0, 0], transition (0, r = 1, s' = 1, not done), then (1, r = 2, terminal), α = 0.5, γ = 1:
δ₁ = 1 + 0 − 0 = 1 → V(0) = 0.5; δ₂ = 2 − 0 = 2 → V(1) = 1.

## Common mistakes
* Bootstrapping from terminal states.
* Updating with the *new* V(s) inside the same δ computation (compute δ first).
* α too large → oscillations.

## Why this matters
TD learning underlies Q-learning, SARSA, actor–critic methods and value learning in modern deep RL.
''',
"statement": r'''
Implement:
* `td_error(V, s, r, s_next, done, gamma)` → float δ.
* `td0(episodes, n_states, alpha, gamma, sweeps=1)` → value array; `episodes` is a list of episodes,
  each a list of `(s, r, s_next, done)`; process all episodes in order, `sweeps` times, updating
  in place from `V = zeros`. Raise `ValueError` unless `0 < alpha <= 1` and `0 <= gamma <= 1`.

**Example**
```python
td0([[(0, 1.0, 1, False), (1, 2.0, 1, True)]], 2, alpha=0.5, gamma=1.0)   # [0.5, 1. ]
```
''',
"starter": r'''
import numpy as np


def td_error(V, s, r, s_next, done, gamma):
    pass


def td0(episodes, n_states, alpha, gamma, sweeps=1):
    pass
''',
"hints": [
    "`target = r + (0 if done else gamma * V[s_next])`.",
    "`delta = target - V[s]`; then `V[s] += alpha * delta`.",
    "Outer loop over sweeps, then episodes, then transitions.",
],
"solution": r'''
import numpy as np


def td_error(V, s, r, s_next, done, gamma):
    target = r + (0.0 if done else gamma * V[s_next])
    return float(target - V[s])


def td0(episodes, n_states, alpha, gamma, sweeps=1):
    if not 0 < alpha <= 1 or not 0 <= gamma <= 1:
        raise ValueError("need 0 < alpha <= 1 and 0 <= gamma <= 1")
    V = np.zeros(n_states)
    for _ in range(sweeps):
        for ep in episodes:
            for s, r, s2, done in ep:
                V[s] += alpha * td_error(V, s, r, s2, done, gamma)
    return V
''',
"explanation": r'''
The TD error compares the one-step bootstrapped target with the current estimate; the value moves a
fraction α towards the target. Processing transitions in order with in-place updates is online TD(0).
''',
"tests": r'''
import numpy as np

class TestTD0(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(S.td0([[(0, 1.0, 1, False), (1, 2.0, 1, True)]], 2, 0.5, 1.0), [0.5, 1.0])

    def test_td_error(self):
        V = np.array([1.0, 3.0])
        self.assertAlmostEqual(S.td_error(V, 0, 0.5, 1, False, 0.9), 0.5 + 2.7 - 1.0)
        self.assertAlmostEqual(S.td_error(V, 0, 0.5, 1, True, 0.9), -0.5)

    def test_order_matters(self):
        ep = [(0, 0.0, 1, False), (1, 1.0, 1, True)]
        V1 = S.td0([ep], 2, 1.0, 1.0)
        np.testing.assert_allclose(V1, [0.0, 1.0])
        V2 = S.td0([ep], 2, 1.0, 1.0, sweeps=2)
        np.testing.assert_allclose(V2, [1.0, 1.0])

    def test_converges_chain(self):
        eps = [[(0, 0.0, 1, False), (1, 0.0, 2, False), (2, 1.0, 2, True)]] * 1
        V = S.td0(eps, 3, 0.1, 0.9, sweeps=2000)
        np.testing.assert_allclose(V, [0.81, 0.9, 1.0], atol=1e-6)

    def test_batch_td_vs_mc(self):
        eps = [[(0, 0.0, 1, False), (1, 0.0, 1, True)]] + [[(1, 1.0, 1, True)]] * 6 + [[(1, 0.0, 1, True)]]
        V = S.td0(eps, 2, 0.01, 1.0, sweeps=3000)
        self.assertAlmostEqual(V[1], 0.75, delta=0.02)
        self.assertAlmostEqual(V[0], 0.75, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.td0([], 2, 0.0, 0.9)
''',
"feedback": [
    ("test_td_error", "Don't bootstrap when done is True."),
    ("test_order_matters", "Update V in place, transition by transition, in order."),
    ("test_converges_chain", "Repeat all episodes `sweeps` times."),
    ("test_batch_td_vs_mc", "Batch TD values A by bootstrapping from B (Sutton & Barto's A/B example idea)."),
],
},
# ---------------------------------------------------------------- q-learning
{
"slug": "q-learning", "title": "Tabular Q-Learning",
"difficulty": "advanced", "prereqs": ["epsilon-greedy", "gridworld-step", "td0-prediction"], "packages": ["numpy"],
"objectives": ["Implement the off-policy Q-learning update", "Train with ε-greedy exploration on a gridworld",
               "Extract and evaluate the learned greedy policy"],
"tags": ["q-learning", "control", "off-policy", "tabular-rl"],
"sources": ["S033", "S034"], "entry": "q_update(Q, s, a, r, s2, done, alpha, gamma); q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)",
"article": r'''
# Q-Learning

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
        a = epsilon_greedy(Q[s], epsilon, rng)      # [[epsilon-greedy]] recipe
        s2, r, done = env_step(s, a)
        q_update(Q, s, a, r, s2, done, alpha, gamma)
        s = s2; stop if done
```
The greedy policy $\arg\max_a Q(s,a)$ converges to optimal with sufficient exploration and a suitable α.

## Worked example
Q(s,·) = [0, 0], action 1 gives r = −1 to s' with max Q = 5, α = 0.5, γ = 0.9:
Q(s,1) = 0 + 0.5(−1 + 4.5 − 0) = 1.75.

## Common mistakes
* Using $Q(s', a_\text{next})$ (that's SARSA, [[sarsa]]).
* Bootstrapping from terminal states.
* Never decaying/limiting episodes → infinite loops; use max_steps.

## Why this matters
Q-learning is the basis of DQN, which learned to play Atari games from pixels.
''',
"statement": r'''
Implement:
* `q_update(Q, s, a, r, s2, done, alpha, gamma)` → updates `Q` in place and returns the TD error.
* `q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)`
  → `(Q, episode_returns)` following the recipe; `env_step(s, a)` returns `(s2, r, done)`;
  `episode_returns` holds the undiscounted reward sum per episode.

**Example**
```python
# 1-D corridor: states 0..3, action 1 moves right, 0 moves left; reaching 3 gives +10 and ends.
Q, rets = q_learning(corridor_step, 0, 4, 2, episodes=300, alpha=0.5, gamma=0.9, epsilon=0.1, seed=0)
Q[:3].argmax(axis=1)     # [1, 1, 1]
```
''',
"starter": r'''
import numpy as np


def q_update(Q, s, a, r, s2, done, alpha, gamma):
    pass


def q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    pass
''',
"hints": [
    "`target = r + (0 if done else gamma * Q[s2].max())`.",
    "ε-greedy: `if rng.random() < epsilon: a = int(rng.integers(n_actions)) else: a = int(np.argmax(Q[s]))`.",
    "Accumulate `total += r` per episode; break when done.",
],
"solution": r'''
import numpy as np


def q_update(Q, s, a, r, s2, done, alpha, gamma):
    target = r + (0.0 if done else gamma * float(np.max(Q[s2])))
    delta = target - Q[s, a]
    Q[s, a] += alpha * delta
    return float(delta)


def q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n_states, n_actions))
    returns = []
    for _ in range(episodes):
        s, total = start, 0.0
        for _ in range(max_steps):
            if rng.random() < epsilon:
                a = int(rng.integers(n_actions))
            else:
                a = int(np.argmax(Q[s]))
            s2, r, done = env_step(s, a)
            q_update(Q, s, a, r, s2, done, alpha, gamma)
            total += r
            s = s2
            if done:
                break
        returns.append(total)
    return Q, returns
''',
"explanation": r'''
The update moves Q(s, a) towards the reward plus the discounted value of the best next action
(off-policy target). The loop explores with ε-greedy behaviour from one seeded generator, applies an
update after every step, and records each episode's total reward.
''',
"tests": r'''
import numpy as np

def corridor_step(s, a):
    s2 = min(s + 1, 3) if a == 1 else max(s - 1, 0)
    return (s2, 10.0, True) if s2 == 3 else (s2, -1.0, False)

MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
ROWS = ["S..", ".X.", "..G"]

def grid_step(s, a):
    r, c = divmod(s, 3); dr, dc = MOVES[a]; nr, nc = r + dr, c + dc
    ns = nr * 3 + nc if 0 <= nr < 3 and 0 <= nc < 3 else s
    ch = ROWS[ns // 3][ns % 3]
    return (ns, 10.0, True) if ch == "G" else (ns, -10.0, True) if ch == "X" else (ns, -1.0, False)

class TestQL(unittest.TestCase):
    def test_update(self):
        Q = np.zeros((2, 2)); Q[1] = [5.0, 2.0]
        d = S.q_update(Q, 0, 1, -1.0, 1, False, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 1], 1.75)
        self.assertAlmostEqual(d, 3.5)

    def test_update_terminal(self):
        Q = np.zeros((2, 2)); Q[1] = [100.0, 100.0]
        S.q_update(Q, 0, 0, 1.0, 1, True, 1.0, 0.9)
        self.assertEqual(Q[0, 0], 1.0)

    def test_corridor_policy(self):
        Q, _ = S.q_learning(corridor_step, 0, 4, 2, 300, 0.5, 0.9, 0.1, 0)
        np.testing.assert_array_equal(Q[:3].argmax(axis=1), [1, 1, 1])

    def test_corridor_values(self):
        Q, _ = S.q_learning(corridor_step, 0, 4, 2, 2000, 0.5, 0.9, 0.2, 1)
        np.testing.assert_allclose(Q[:3, 1], [-1 + 0.9 * (-1 + 9), -1 + 9, 10], atol=1e-3)

    def test_grid_avoids_pit(self):
        Q, rets = S.q_learning(grid_step, 0, 9, 4, 800, 0.5, 0.95, 0.1, 0)
        s, path = 0, []
        for _ in range(10):
            s, r, done = grid_step(s, int(np.argmax(Q[s]))); path.append(s)
            if done:
                break
        self.assertEqual(path[-1], 8)
        self.assertNotIn(4, path)

    def test_returns_improve(self):
        _, rets = S.q_learning(corridor_step, 0, 4, 2, 200, 0.5, 0.9, 0.1, 2)
        self.assertEqual(len(rets), 200)
        self.assertGreater(np.mean(rets[-20:]), np.mean(rets[:5]))

    def test_reproducible(self):
        a = S.q_learning(corridor_step, 0, 4, 2, 50, 0.5, 0.9, 0.3, 7)[0]
        np.testing.assert_array_equal(a, S.q_learning(corridor_step, 0, 4, 2, 50, 0.5, 0.9, 0.3, 7)[0])
''',
"feedback": [
    ("test_update", "Target = r + γ·max_a' Q(s', a'); Q += α·(target − Q)."),
    ("test_update_terminal", "When done, the target is just r."),
    ("test_corridor_values", "Q-learning bootstraps from the greedy max even while exploring."),
    ("test_grid_avoids_pit", "Use one seeded generator for ε-greedy decisions across all episodes."),
],
},
# ---------------------------------------------------------------- sarsa
{
"slug": "sarsa", "title": "SARSA",
"difficulty": "advanced", "prereqs": ["q-learning"], "packages": ["numpy"],
"objectives": ["Implement the on-policy SARSA update", "Choose the next action before updating",
               "Contrast SARSA's safer behaviour with Q-learning on a risky path"],
"tags": ["sarsa", "on-policy", "control", "tabular-rl"],
"sources": ["S033"], "entry": "sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma); sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)",
"article": r'''
# SARSA: On-Policy TD Control

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
(One shared seeded generator; ε-greedy recipe from [[epsilon-greedy]].)

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
''',
"statement": r'''
Implement:
* `sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma)` → updates in place, returns the TD error.
* `sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)`
  → `(Q, episode_returns)` following the recipe.

**Example**
```python
Q = np.zeros((2, 2)); Q[1] = [5., 2.]
sarsa_update(Q, 0, 1, -1.0, 1, 1, False, 0.5, 0.9); Q[0, 1]   # 0.4
```
''',
"starter": r'''
import numpy as np


def sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma):
    pass


def sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    pass
''',
"hints": [
    "`target = r + (0 if done else gamma * Q[s2, a2])`.",
    "Write an inner `eps(state)` using the shared rng.",
    "Choose `a2` before calling `sarsa_update`, then set `s, a = s2, a2`.",
],
"solution": r'''
import numpy as np


def sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma):
    target = r + (0.0 if done else gamma * Q[s2, a2])
    delta = target - Q[s, a]
    Q[s, a] += alpha * delta
    return float(delta)


def sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n_states, n_actions))

    def eps(state):
        if rng.random() < epsilon:
            return int(rng.integers(n_actions))
        return int(np.argmax(Q[state]))

    returns = []
    for _ in range(episodes):
        s, total = start, 0.0
        a = eps(s)
        for _ in range(max_steps):
            s2, r, done = env_step(s, a)
            a2 = eps(s2) if not done else 0
            sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma)
            total += r
            s, a = s2, a2
            if done:
                break
        returns.append(total)
    return Q, returns
''',
"explanation": r'''
The update bootstraps from the value of the next action actually selected by the ε-greedy policy, so
the learned values reflect the behaviour policy including its exploratory mistakes. The next action is
chosen before the update and then executed.
''',
"tests": r'''
import numpy as np

def corridor_step(s, a):
    s2 = min(s + 1, 3) if a == 1 else max(s - 1, 0)
    return (s2, 10.0, True) if s2 == 3 else (s2, -1.0, False)

# Cliff walking (Sutton & Barto Example 6.6, scaled down): 3 x 6 grid, start bottom-left,
# goal bottom-right, the bottom cells between them are a cliff (-100, back to start).
R, C = 3, 6
START, GOAL = (R - 1) * C, R * C - 1
CLIFF = set(range(START + 1, GOAL))
MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
def cliff_step(s, a):
    r, c = divmod(s, C); dr, dc = MOVES[a]; nr, nc = r + dr, c + dc
    if not (0 <= nr < R and 0 <= nc < C):
        nr, nc = r, c
    ns = nr * C + nc
    if ns in CLIFF:
        return START, -100.0, False
    if ns == GOAL:
        return GOAL, 0.0, True
    return ns, -1.0, False

def q_learning_ref(env_step, start, nS, nA, episodes, alpha, gamma, eps, seed, max_steps):
    rng = np.random.default_rng(seed); Q = np.zeros((nS, nA))
    for _ in range(episodes):
        s = start
        for _ in range(max_steps):
            a = int(rng.integers(nA)) if rng.random() < eps else int(np.argmax(Q[s]))
            s2, r, d = env_step(s, a)
            Q[s, a] += alpha * (r + (0 if d else gamma * Q[s2].max()) - Q[s, a]); s = s2
            if d:
                break
    return Q

def greedy_rows(Q):
    s, rows = START, []
    for _ in range(40):
        s, _, d = cliff_step(s, int(np.argmax(Q[s]))); rows.append(s // C)
        if d:
            return rows, True
    return rows, False

class TestSARSA(unittest.TestCase):
    def test_update(self):
        Q = np.zeros((2, 2)); Q[1] = [5., 2.]
        d = S.sarsa_update(Q, 0, 1, -1.0, 1, 1, False, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 1], 0.4)
        self.assertAlmostEqual(d, 0.8)

    def test_update_terminal(self):
        Q = np.ones((2, 2)) * 50
        S.sarsa_update(Q, 0, 0, 2.0, 1, 0, True, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 0], 26.0)

    def test_corridor(self):
        Q, _ = S.sarsa(corridor_step, 0, 4, 2, 400, 0.5, 0.9, 0.1, 0)
        np.testing.assert_array_equal(Q[:3].argmax(axis=1), [1, 1, 1])

    def test_cliff_safe_path_vs_qlearning(self):
        Qs, _ = S.sarsa(cliff_step, START, R * C, 4, 3000, 0.1, 1.0, 0.1, 0, max_steps=500)
        Qq = q_learning_ref(cliff_step, START, R * C, 4, 3000, 0.1, 1.0, 0.1, 0, 500)
        rs, ok_s = greedy_rows(Qs)
        rq, ok_q = greedy_rows(Qq)
        self.assertTrue(ok_s and ok_q)
        self.assertEqual(min(rs), 0)   # SARSA detours through the far (safe) row
        self.assertEqual(min(rq), 1)   # Q-learning walks along the cliff edge

    def test_returns_len(self):
        _, rets = S.sarsa(corridor_step, 0, 4, 2, 37, 0.5, 0.9, 0.1, 1)
        self.assertEqual(len(rets), 37)

    def test_reproducible(self):
        a = S.sarsa(corridor_step, 0, 4, 2, 30, 0.5, 0.9, 0.3, 5)[0]
        np.testing.assert_array_equal(a, S.sarsa(corridor_step, 0, 4, 2, 30, 0.5, 0.9, 0.3, 5)[0])
''',
"feedback": [
    ("test_update", "SARSA's target uses Q(s', a') for the next action actually chosen, not the max."),
    ("test_update_terminal", "No bootstrapping when done."),
    ("test_cliff_safe_path_vs_qlearning", "Choose a' with ε-greedy before updating and carry it forward; SARSA should learn the safe path."),
    ("test_reproducible", "Use one seeded generator for all action choices."),
],
},
# ---------------------------------------------------------------- policy-iteration
{
"slug": "policy-iteration", "title": "Policy Iteration",
"difficulty": "intermediate", "prereqs": ["policy-evaluation", "value-iteration"], "packages": ["numpy"],
"objectives": ["Alternate policy evaluation and greedy improvement", "Detect policy stability",
               "Verify agreement with value iteration"],
"tags": ["policy-iteration", "dynamic-programming", "policy-improvement"],
"sources": ["S033", "S034"], "entry": "policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100)",
"article": r'''
# Policy Iteration

## Intuition
Start with any policy. Work out how good it is (evaluation), then switch every state to the action
that looks best given those values (improvement). Repeat until nothing changes — the policy is then
optimal. It usually needs surprisingly few rounds.

## Precise explanation (Sutton & Barto, §4.3)
1. Initialise deterministic policy π(s) = 0 for all s.
2. **Evaluate** π ([[policy-evaluation]]) with the deterministic policy matrix.
3. **Improve:** π′(s) = argmax_a Q(s, a) from the evaluated V (ties → lowest action).
4. If π′ = π stop, else π ← π′ and repeat.
The policy improvement theorem guarantees each new policy is at least as good; with finitely many
deterministic policies the loop terminates. To avoid flip-flopping between equally good actions, the
lowest-index tie-break makes "unchanged" well defined.

```mermaid
flowchart LR
  P0[π0] --> E[evaluate V^π] --> I[improve: greedy w.r.t. V] --> C{π changed?}
  C -- yes --> E
  C -- no --> O[optimal π*]
```

## Worked example
Corridor with actions left/right: π₀ = all-left; evaluation gives negative values; improvement
switches the state next to the goal to right, then the others — stable after a few iterations.

## Common mistakes
* Comparing policies by values with floating-point noise instead of comparing actions.
* Forgetting to re-evaluate after improvement.
* Ties causing infinite loops.

## Why this matters
Policy iteration is the template for actor–critic methods: a critic evaluates, an actor improves.
''',
"statement": r'''
Write `policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100)` returning `(V, policy, n_improvements)`
where `policy` is an int array and `n_improvements` the number of evaluate-improve cycles performed
(including the final one where the policy did not change). Include your own policy evaluation and
lookahead helpers. Raise `ValueError` if `gamma` not in `[0, 1)`.

**Example**
```python
V, pi, k = policy_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
pi[:3]     # [1, 1, 1]
```
''',
"starter": r'''
import numpy as np


def policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100):
    pass
''',
"hints": [
    "Deterministic policy matrix: `pm = np.zeros((nS, nA)); pm[np.arange(nS), pi] = 1`.",
    "Evaluate synchronously until max change < theta; compute Q from V.",
    "`new_pi = Q.argmax(axis=1)`; stop when `np.array_equal(new_pi, pi)`.",
],
"solution": r'''
import numpy as np


def _q(P, V, gamma):
    nS, nA = len(P), len(P[0])
    Q = np.zeros((nS, nA))
    for s in range(nS):
        for a in range(nA):
            Q[s, a] = sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][a])
    return Q


def _evaluate(P, pi, gamma, theta, max_sweeps=100000):
    nS = len(P)
    V = np.zeros(nS)
    for _ in range(max_sweeps):
        new = np.array([sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][int(pi[s])])
                        for s in range(nS)])
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            break
    return V


def policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100):
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    pi = np.zeros(len(P), dtype=int)
    for k in range(1, max_iter + 1):
        V = _evaluate(P, pi, gamma, theta)
        new_pi = _q(P, V, gamma).argmax(axis=1)
        if np.array_equal(new_pi, pi):
            return V, pi, k
        pi = new_pi
    return V, pi, max_iter
''',
"explanation": r'''
Each cycle evaluates the current deterministic policy to convergence, then acts greedily with respect
to the resulting values. Because ties resolve to the lowest action, an unchanged argmax means the
policy is stable and therefore optimal.
''',
"tests": r'''
import numpy as np

MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

def grid_P(rows):
    R, C = len(rows), len(rows[0]); P = {}
    for s in range(R * C):
        r, c = divmod(s, C); ch = rows[r][c]; P[s] = {}
        for a, (dr, dc) in MOVES.items():
            if ch in "#GX":
                P[s][a] = [(1.0, s, 0.0, True)]; continue
            nr, nc = r + dr, c + dc
            ns = nr * C + nc if 0 <= nr < R and 0 <= nc < C and rows[nr][nc] != "#" else s
            t = rows[ns // C][ns % C]
            P[s][a] = [(1.0, ns, 10.0, True)] if t == "G" else [(1.0, ns, -10.0, True)] if t == "X" else [(1.0, ns, -1.0, False)]
    return P

def value_iteration(P, gamma):
    V = np.zeros(len(P))
    for _ in range(10000):
        Q = np.array([[sum(p * (r + gamma * (0 if d else V[s2])) for p, s2, r, d in P[s][a]) for a in range(len(P[0]))] for s in range(len(P))])
        new = Q.max(1)
        if np.max(np.abs(new - V)) < 1e-12:
            return new
        V = new
    return V

class TestPI(unittest.TestCase):
    def test_grid(self):
        V, pi, k = S.policy_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        np.testing.assert_array_equal(pi[:3], [1, 1, 1])
        self.assertGreaterEqual(k, 2)

    def test_matches_value_iteration(self):
        P = grid_P(["S...", ".#X.", "...G"])
        V, _, _ = S.policy_iteration(P, gamma=0.95)
        np.testing.assert_allclose(V, value_iteration(P, 0.95), atol=1e-7)

    def test_stochastic(self):
        P = {0: {0: [(1.0, 0, 0.0, True)], 1: [(0.8, 1, 0.0, False), (0.2, 0, -1.0, False)]},
             1: {0: [(1.0, 1, 5.0, True)], 1: [(1.0, 1, 1.0, True)]}}
        V, pi, _ = S.policy_iteration(P, gamma=0.9)
        self.assertEqual(pi.tolist(), [1, 0])
        self.assertAlmostEqual(V[0], (0.8 * 0.9 * 5 - 0.2) / (1 - 0.2 * 0.9), places=8)

    def test_already_optimal_one_cycle(self):
        P = {0: {0: [(1.0, 0, 1.0, True)], 1: [(1.0, 0, 0.0, True)]}}
        _, pi, k = S.policy_iteration(P)
        self.assertEqual((pi.tolist(), k), ([0], 1))

    def test_avoid_pit(self):
        _, pi, _ = S.policy_iteration(grid_P(["S.X", "...", "..G"]), gamma=0.9)
        self.assertEqual(pi[1], 2)

    def test_bad_gamma(self):
        with self.assertRaises(ValueError):
            S.policy_iteration(grid_P(["SG"]), gamma=1.0)
''',
"feedback": [
    ("test_matches_value_iteration", "Evaluate the current policy fully before improving."),
    ("test_stochastic", "Lookahead must weight outcomes by probability and stop bootstrapping at done."),
    ("test_already_optimal_one_cycle", "Count the final cycle in which the policy did not change."),
    ("test_grid", "Improvement is argmax over actions of Q computed from V^π."),
],
},
]
