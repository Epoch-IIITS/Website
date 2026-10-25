r"""Reference solution for AG-11 BFS Planner.

BFS dequeues states in order of distance from the start, so the first goal dequeued is reached by a
shortest plan. Parent pointers recorded at enqueue time make each state's discovery unique and allow
plan reconstruction.
"""
from collections import deque


def bfs_plan(start, goal_test, successors):
    queue = deque([start])
    parent = {start: None}
    expanded = 0
    while queue:
        state = queue.popleft()
        expanded += 1
        if goal_test(state):
            actions, states = [], [state]
            while parent[state] is not None:
                prev, act = parent[state]
                actions.append(act)
                states.append(prev)
                state = prev
            return {"actions": actions[::-1], "states": states[::-1], "expanded": expanded}
        for action, nxt in successors(state):
            if nxt not in parent:
                parent[nxt] = (state, action)
                queue.append(nxt)
    return None
