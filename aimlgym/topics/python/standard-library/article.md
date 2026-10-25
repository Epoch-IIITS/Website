# Importing the Standard Library

## Learning outcomes

After this lesson you can:

- Import modules with import, from ... import and as
- Use math, random, collections, heapq and itertools for common tasks
- Make random results reproducible with random.Random(seed)
- Explain what each library function replaces

## Intuition
Python ships with a large **standard library**: modules of tested code for maths, randomness,
counting, queues and combinations. Importing a module is like taking a toolbox off the shelf.
You already know how to write many of these tools as loops; now you can choose the shorter,
well-tested version and know what it does for you.

## Precise explanation
```python
import math                       # use as math.sqrt(...)
from collections import Counter   # use the name directly: Counter(...)
import itertools as it            # an alias: it.combinations(...)
```
* `import` runs the module once and binds its name. `dir(math)` lists what it contains and
  `help(math.ceil)` shows documentation.
* Avoid `from math import *`: it hides where names come from.

| Module / function | What it gives you | The loop it replaces |
|---|---|---|
| `math.sqrt`, `math.hypot`, `math.ceil`, `math.pi` | exact, fast numeric functions | `x ** 0.5`, `-(-a // b)` |
| `random.Random(seed)` | an independent random generator with its own seed | — |
| `collections.Counter(text)` | counts of each item; `.most_common()` | a dict of counts (PY-13) |
| `collections.defaultdict(list)` | a dict that creates missing values | `d.setdefault(k, [])` |
| `collections.deque` | a queue with fast `append` and `popleft` | `list.pop(0)` (slow) |
| `heapq.nsmallest(k, nums)` | the k smallest items without sorting everything | `sorted(nums)[:k]` |
| `itertools.combinations(items, 2)` | every unordered pair, in order | two nested `for` loops |

**Reproducible randomness.** `rng = random.Random(42)` creates a generator; calling
`rng.random()` gives floats in `[0, 1)` and the sequence is the same every time for the same seed.
Python documents that `random()` output is reproducible across versions; other methods such as
`randint` may change between versions, so graded tasks build integers from `random()`:
`int(rng.random() * 6) + 1` is a die roll from 1 to 6.

## Worked example
```python
from collections import Counter
Counter("banana").most_common(1)      # [('a', 3)]
import heapq
heapq.nsmallest(2, [5, 1, 4, 1])      # [1, 1]
import itertools
list(itertools.combinations("abc", 2))  # [('a','b'), ('a','c'), ('b','c')]
```

## Common mistakes
* Naming your own file `random.py` or `math.py`: `import random` then imports *your* file.
* Using the global `random.random()` in code that must be reproducible; create `Random(seed)`.
* Expecting `Counter.most_common` to break ties alphabetically — it keeps first-seen order, so
  sort yourself when ties must be deterministic.
* Forgetting that `itertools.combinations` returns an iterator; wrap it in `list(...)`.

## Why this matters
Later topics use `collections.Counter` for word counts, `deque` for breadth-first search,
`heapq` for planners and top-k results, and `itertools` for Shapley value subsets.

## References

- [The Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html) — Python Software Foundation (`S045`)
- [The Python Tutorial: Brief Tour of the Standard Library](https://docs.python.org/3/tutorial/stdlib.html) — Python Software Foundation (`S047`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
- [collections — Container datatypes](https://docs.python.org/3/library/collections.html) — Python Software Foundation (`S051`)
- [heapq — Heap queue algorithm](https://docs.python.org/3/library/heapq.html) — Python Software Foundation (`S052`)
- [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html) — Python Software Foundation (`S053`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
