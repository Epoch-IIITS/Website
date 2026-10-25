# Async Endpoints and External Services

## Learning outcomes

After this lesson you can:

- Write async def endpoints that await an external service
- Call several services concurrently with asyncio.gather
- Map timeouts and upstream failures to 504 and 502
- Test with fake async services injected as dependencies — no network

## Intuition
Many APIs call *other* APIs: a weather service, a payment provider, a language model. Those calls
mostly wait on the network. With `async def` endpoints, FastAPI's event loop serves other
requests during the wait, and `asyncio.gather` lets one request wait for several services at once
(FA-06). Because the external service is a dependency, tests replace it with a fake
that answers instantly — or never — so every failure path is testable offline.

## Precise explanation
```python
@app.get("/weather/{city}")
async def weather(city: str,
                  service: Annotated[WeatherService, Depends(get_weather)],
                  settings: Annotated[Settings, Depends(get_settings)]):
    try:
        temp = await asyncio.wait_for(service.temperature(city), settings.timeout)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Weather service timed out")
    except LookupError:
        raise HTTPException(404, "Unknown city")
    except Exception:
        raise HTTPException(502, "Weather service error")
    return {"city": city, "temperature": temp}
```
* **def vs async def**: FastAPI runs plain `def` endpoints in a thread pool and `async def`
  endpoints on the event loop. Inside `async def`, never call blocking functions such as
  `time.sleep` or a synchronous HTTP client — they freeze every request.
* **502 Bad Gateway**: the upstream service failed. **504 Gateway Timeout**: it did not answer in
  time. Both are server-side (5xx) because the client did nothing wrong.
* `asyncio.gather(*coros, return_exceptions=True)` returns exceptions as values instead of
  raising the first one, so one failing city does not fail the whole response.
* **Fakes** implement the same async method as the real service. Overriding `get_weather` and
  `get_settings` (a short timeout) makes tests fast and deterministic. A real implementation would
  use an async HTTP client such as `httpx.AsyncClient`.

## Worked example
With a fake returning `{"paris": 18.5}`, `GET /weather/paris` → `{"city": "paris",
"temperature": 18.5}`; a fake that never answers plus a 0.01 s timeout → 504.

## Common mistakes
* `await`ing services one after another in a loop when they could run concurrently.
* Catching `Exception` before `asyncio.TimeoutError`/`LookupError`, so every failure becomes 502.
* Testing against the real service — slow, flaky and possibly paid.

## Why this matters
LLM applications and agents spend most of their time awaiting model and tool calls; the same
timeout, error-mapping and fake-service patterns keep them reliable.

## References

- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI Advanced: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) — FastAPI (Sebastián Ramírez) (`S079`)
