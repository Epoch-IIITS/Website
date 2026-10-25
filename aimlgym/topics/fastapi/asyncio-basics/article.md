# async and await with asyncio

## Learning outcomes

After this lesson you can:

- Define coroutines with async def and run them with asyncio.run
- Run coroutines concurrently with asyncio.gather and see how await yields control
- Limit concurrency with a Semaphore
- Stop slow work with asyncio.wait_for

## Intuition
A web server spends most of its time **waiting** — for a database, another API, a file. While one
request waits, the server could work on another. `async`/`await` lets one thread juggle many
waiting tasks: at every `await`, a task says "I am waiting; run someone else", and the
**event loop** switches to another ready task.

## Precise explanation
```python
import asyncio

async def worker(name, log):        # a coroutine function
    log.append(f"{name} start")
    await asyncio.sleep(0)           # yield control to the event loop
    log.append(f"{name} end")
    return name.upper()

asyncio.run(worker("a", []))         # run a coroutine from normal code
```
* Calling `worker(...)` does **not** run it; it creates a coroutine object. It runs when awaited
  or scheduled.
* `await a(); await b()` runs them **one after the other**.
* `await asyncio.gather(a(), b())` runs them **concurrently** and returns results in argument
  order, regardless of which finished first. With the `worker` above the log becomes
  `a start, b start, a end, b end` — each `await` let the other task proceed.
* `asyncio.Semaphore(n)` limits how many tasks enter a block at once:
  `async with sem: ...`.
* `await asyncio.wait_for(coro, timeout)` raises `TimeoutError` (`asyncio.TimeoutError`, the same
  class since Python 3.11) if it takes too long and cancels the work.
* **Blocking** calls such as `time.sleep` freeze the whole loop; use `await asyncio.sleep` and
  async libraries inside coroutines.

## Worked example
Three downloads of 1 s each: sequential awaits take about 3 s; `gather` takes about 1 s, because
the waits overlap. (Tests in this site avoid real time and check the order of events instead.)

## Common mistakes
* Forgetting `await`, so the coroutine never runs (Python warns "coroutine was never awaited").
* Calling `asyncio.run` inside code that is already running in an event loop.
* Expecting `async` to speed up CPU-heavy work — it only overlaps *waiting*.

## Why this matters
FastAPI runs `async def` endpoints on an event loop (FA-14), and ASGI applications
(FA-07) are coroutines.

## References

- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
