# A* Search

## Learning outcomes

After this lesson you can:

- Search with path cost plus an admissible heuristic
- Use a priority queue with deterministic tie-breaking
- Compare node expansions with uniform-cost search

## Intuition
BFS explores in rings and ignores where the goal is. A* prefers states that are cheap to reach *and*
look close to the goal, guided by a heuristic — like a hiker who keeps track of distance walked and
checks the summit's bearing.

## Precise explanation (AIMA, ch. 3)
Priority $f(n) = g(n) + h(n)$: g = cost so far, h = heuristic estimate to the goal.
* Pop the lowest f from a heap (ties: lower h, then insertion order via a counter).
* Skip stale entries (a cheaper g was already recorded).
* Relax neighbours: if `g + cost < best_g[nbr]`, record it and push.
* Stop when the goal is **popped** (not when first generated).
If h is **admissible** (never overestimates) and consistent, A* returns an optimal path. With h = 0 it
is uniform-cost search (Dijkstra). On a 4-connected grid with unit costs, Manhattan distance is
admissible.

## Worked example
Open 5×5 grid from (0,0) to (4,4): optimal cost 8 both ways, but A* with Manhattan expands far fewer
states than h = 0.

## Common mistakes
* Stopping when the goal is generated (can return a suboptimal path).
* Inadmissible heuristics (e.g. Manhattan × 2) losing optimality.
* Comparing non-comparable states in the heap — always include a counter.

## Why this matters
A* is the workhorse of game AI, robot navigation and route planning; heuristics are an early form of
"intuition" guiding search, a theme that returns in LLM-guided planning.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
