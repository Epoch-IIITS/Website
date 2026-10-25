r"""Reference solution for RL-02 Gridworld Transition Function.

States are flattened grid coordinates. A move is applied unless it leaves the grid or hits a wall;
the destination cell determines reward and termination. The transition table enumerates `step` for
every state–action pair and makes walls and terminal states absorbing with zero reward.
"""
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
