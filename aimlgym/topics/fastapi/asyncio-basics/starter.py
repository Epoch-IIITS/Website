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
    # TODO: asyncio.gather
    return run_in_order(log)


def gather_in_order(values):
    # TODO
    return []


def limited(factories, limit):
    # TODO: Semaphore
    return []


def with_timeout(coro, seconds):
    # TODO: asyncio.wait_for
    return ("ok", None)
