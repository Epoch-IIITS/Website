# PY-15 · Importing the Standard Library

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-14 Fibonacci Sequence

Read the lesson first: [article.md](article.md)

## Task

Implement six small functions, each using the named module:

1. `hypotenuse(a, b)` → length of the hypotenuse, using `math.hypot` (or `math.sqrt`).
2. `pages_needed(items, per_page)` → how many pages are needed to show `items` items,
   using `math.ceil`. `pages_needed(0, 10) == 0`.
3. `most_common_letter(text)` → the most frequent **letter** (case-insensitive, ignore
   non-letters, use `collections.Counter`); break ties by alphabetical order; return `None` if
   there are no letters.
4. `dice_rolls(seed, n)` → a list of `n` die rolls from `rng = random.Random(seed)`, each
   `int(rng.random() * 6) + 1`.
5. `smallest_k(nums, k)` → the `k` smallest numbers in ascending order, using `heapq.nsmallest`.
6. `all_pairs(items)` → a list of all unordered pairs (as tuples) in input order, using
   `itertools.combinations`.

**Examples**
```python
hypotenuse(3, 4)                 # 5.0
pages_needed(21, 10)             # 3
most_common_letter("Hello, World")  # 'l'
smallest_k([5, 1, 4, 1], 2)      # [1, 1]
all_pairs(["a", "b", "c"])       # [('a', 'b'), ('a', 'c'), ('b', 'c')]
```

## Hints

<details><summary>Hint 1</summary>

`math.ceil(items / per_page)` rounds up; `Counter(ch for ch in text.lower() if ch.isalpha())` counts letters.

</details>

<details><summary>Hint 2</summary>

For ties, find the highest count, then return `min` of the letters that have it.

</details>

<details><summary>Hint 3</summary>

`[int(rng.random() * 6) + 1 for _ in range(n)]`, `heapq.nsmallest(k, nums)`, `list(itertools.combinations(items, 2))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pages_needed` | Use `math.ceil(items / per_page)`; integer `//` rounds down. |
| `test_most_common_tie_and_case` | Lowercase first, keep only `ch.isalpha()`, break ties with `min`, and return None when nothing is left. |
| `test_dice_reproducible` | Create `random.Random(seed)` inside the function and use only `rng.random()`. |
| `test_smallest_k` | `heapq.nsmallest(k, nums)` already returns ascending order. |
| `test_all_pairs` | Convert the combinations iterator to a list of tuples. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each function delegates the core work to a standard-library tool: `math.hypot` and `math.ceil`
for numerics, `Counter` for counting (with an explicit alphabetical tie-break, which
`most_common` does not provide), a seeded `random.Random` for reproducible rolls, `heapq` for a
partial sort and `itertools.combinations` for pairs.

## References

- [The Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html) — Python Software Foundation (`S045`)
- [The Python Tutorial: Brief Tour of the Standard Library](https://docs.python.org/3/tutorial/stdlib.html) — Python Software Foundation (`S047`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
- [collections — Container datatypes](https://docs.python.org/3/library/collections.html) — Python Software Foundation (`S051`)
- [heapq — Heap queue algorithm](https://docs.python.org/3/library/heapq.html) — Python Software Foundation (`S052`)
- [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html) — Python Software Foundation (`S053`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
