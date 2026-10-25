# FA-14 · Async Endpoints and External Services

**Topic:** FastAPI · **Difficulty:** advanced · **Allowed packages:** fastapi

**Builds on:** FA-13 Dependencies and Dependency Overrides, FA-06 async and await with asyncio

Read the lesson first: [article.md](article.md)

## Task

Implement:

* `class WeatherService` with `async def temperature(self, city)` that raises
  `RuntimeError("network access is disabled in this course")` (it stands for a real client).
* `class Settings` with attribute `timeout = 1.0`; `get_settings()` returns `Settings()`;
  `get_weather()` returns `WeatherService()`.
* `create_app()` with:
  * `GET /weather/{city}` exactly as in the lesson (504, 404, 502 mapping);
  * `GET /weather` with repeated query parameter `city` (at least one; `Query(min_length=1)`)
    → list, in request order, of `{"city": c, "temperature": t}` or `{"city": c, "error":
    "timeout" | "unknown city" | "service error"}`. Fetch all cities **concurrently** with
    `asyncio.gather(..., return_exceptions=True)`, each wrapped in `asyncio.wait_for` with the
    settings timeout.

## Hints

<details><summary>Hint 1</summary>

Order the `except` clauses: `asyncio.TimeoutError`, then `LookupError`, then `Exception`.

</details>

<details><summary>Hint 2</summary>

For the list endpoint: `coros = [asyncio.wait_for(service.temperature(c), settings.timeout) for c in city]` then `await asyncio.gather(*coros, return_exceptions=True)`.

</details>

<details><summary>Hint 3</summary>

Map each result: `isinstance(r, asyncio.TimeoutError)` → "timeout", `isinstance(r, LookupError)` → "unknown city", other exceptions → "service error".

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_single_errors` | Wrap the call in asyncio.wait_for and catch TimeoutError (504), LookupError (404), then Exception (502). |
| `test_many_in_order` | Return one entry per requested city, in request order. |
| `test_many_runs_concurrently` | Start all calls together with asyncio.gather instead of awaiting them in a loop. |
| `test_many_partial_failures` | Use `return_exceptions=True` and turn each exception into an error entry. |
| `test_requires_city` | Declare `city: Annotated[list[str], Query(min_length=1)]`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Both endpoints await the service through `asyncio.wait_for`, so a hung upstream cannot hang the
API. The single-city endpoint maps each failure type to its status code, most specific first. The
multi-city endpoint starts every call at once and uses `return_exceptions=True` so each city's
outcome is reported separately, in request order.

## References

- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
