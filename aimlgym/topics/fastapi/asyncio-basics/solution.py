r"""Reference solution for FA-06 async and await with asyncio.

Sequential awaits finish one coroutine before starting the next, while `gather` schedules both so
each `await asyncio.sleep(0)` hands control to the other — visible in the log order. `gather`
always returns results in argument order. The semaphore is created inside the running loop and
caps how many guarded coroutines are active, and `wait_for` turns a slow coroutine into a
`TimeoutError` that is reported as a value.
"""
import asyncio


async def step(name, log):
    log.append(f"{name}1")
    await asyncio.sleep(0)
    log.append(f"{name}2")
    return name


def run_in_order(log):
    async def main():
        a = await step("a", log)
        b = await step("b", log)
        return [a, b]
    return asyncio.run(main())


def run_together(log):
    async def main():
        return list(await asyncio.gather(step("a", log), step("b", log)))
    return asyncio.run(main())


def gather_in_order(values):
    async def handle(v):
        for _ in range(v):
            await asyncio.sleep(0)
        return v * 10

    async def main():
        return list(await asyncio.gather(*(handle(v) for v in values)))
    return asyncio.run(main())


def limited(factories, limit):
    async def main():
        sem = asyncio.Semaphore(limit)

        async def guarded(f):
            async with sem:
                return await f()
        return list(await asyncio.gather(*(guarded(f) for f in factories)))
    return asyncio.run(main())


def with_timeout(coro, seconds):
    async def main():
        try:
            return ("ok", await asyncio.wait_for(coro, seconds))
        except asyncio.TimeoutError:
            return ("timeout", None)
    return asyncio.run(main())
