# FA-06 · async and await with asyncio

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** FA-05 A Router by Hand

Read the lesson first: [article.md](article.md)

## Task

The starter defines `step(name, log)`: it appends `f"{name}1"`, awaits `asyncio.sleep(0)`, appends
`f"{name}2"` and returns `name`. Implement (each returns normally — call `asyncio.run` inside):

1. `run_in_order(log)` → run `step("a", log)` then `step("b", log)` sequentially; return
   `["a", "b"]`. The log becomes `["a1", "a2", "b1", "b2"]`.
2. `run_together(log)` → run both with `asyncio.gather`; return the results. The log becomes
   `["a1", "b1", "a2", "b2"]`.
3. `gather_in_order(values)` → each value `v` is handled by a coroutine that awaits
   `asyncio.sleep(0)` **v times** and then returns `v * 10`; run them all concurrently and return
   the list of results in the input order (values are non-negative ints).
4. `limited(factories, limit)` → `factories` are zero-argument functions returning coroutines;
   run all of them concurrently but with at most `limit` running at once (`asyncio.Semaphore`);
   return their results in order.
5. `with_timeout(coro, seconds)` → `("ok", result)` or `("timeout", None)`.

## Hints

<details><summary>Hint 1</summary>

`async def main(): return list(await asyncio.gather(step("a", log), step("b", log)))`.

</details>

<details><summary>Hint 2</summary>

Inside `gather_in_order`, define `async def handle(v): for _ in range(v): await asyncio.sleep(0)` then `return v * 10`.

</details>

<details><summary>Hint 3</summary>

In `limited`, create the semaphore inside the async main; wrap each call as `async with sem: return await f()`. For the timeout, catch `asyncio.TimeoutError`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_concurrent` | Use `asyncio.gather` so both coroutines start before either finishes. |
| `test_gather_keeps_input_order` | gather returns results in the order the coroutines were passed. |
| `test_limited` | Guard each call with `async with sem:` where `sem = asyncio.Semaphore(limit)`. |
| `test_limited_unbounded` | Start all guarded coroutines together with gather; don't await them one by one. |
| `test_timeout` | Wrap the coroutine in `asyncio.wait_for` and catch `asyncio.TimeoutError`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Sequential awaits finish one coroutine before starting the next, while `gather` schedules both so
each `await asyncio.sleep(0)` hands control to the other — visible in the log order. `gather`
always returns results in argument order. The semaphore is created inside the running loop and
caps how many guarded coroutines are active, and `wait_for` turns a slow coroutine into a
`TimeoutError` that is reported as a value.

## References

- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
