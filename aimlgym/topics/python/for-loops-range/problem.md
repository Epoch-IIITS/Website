# PY-09 · For Loops and range: FizzBuzz

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-08 While Loops: Read Until Done

Read the lesson first: [article.md](article.md)

## Task

Read an integer `n` (0 ≤ n ≤ 1000). For each `i` from 1 to `n` print one line:
* `FizzBuzz` if `i` is divisible by both 3 and 5,
* `Fizz` if divisible by 3 only,
* `Buzz` if divisible by 5 only,
* otherwise the number itself.

Finally print `sum=<sum of all i from 1 to n divisible by 3 or 5>`.

**Example** for `n = 5`:
```
1
2
Fizz
4
Buzz
sum=8
```

## Hints

<details><summary>Hint 1</summary>

`for i in range(1, n + 1):` includes n.

</details>

<details><summary>Hint 2</summary>

Check `i % 15 == 0` (or `i % 3 == 0 and i % 5 == 0`) before the single cases.

</details>

<details><summary>Hint 3</summary>

Add to `total` inside `if i % 3 == 0 or i % 5 == 0:`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_fifteen_line` | Test divisibility by both 3 and 5 before testing 3 alone. |
| `test_five` | Use `range(1, n + 1)` so n itself is included. |
| `test_zero` | With n = 0 the loop runs zero times; only the sum line is printed. |
| `test_fifteen_sum` | Add i to the total when it is divisible by 3 **or** 5. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`range(1, n + 1)` visits every number once. The combined case is tested first because a number
divisible by 15 also passes the single tests. The sum is a separate condition inside the same
loop, so no second pass is needed.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
