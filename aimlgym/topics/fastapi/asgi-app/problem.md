# FA-07 · A Minimal ASGI Application

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** FA-06 async and await with asyncio

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `async def app(scope, receive, send)` handling `scope["type"] == "http"`:
   * `GET /` → 200 `{"message": "hello"}`;
   * `GET /echo` → 200 `{"params": <dict of first values from the query string, decoded with
     urllib.parse.parse_qs>}` — you may use `urllib.parse.parse_qs` here;
   * `POST /sum` → read the whole body (all chunks), parse JSON `{"numbers": [...]}` and return
     200 `{"sum": total}`; invalid JSON or a missing/non-list `numbers` → 400 `{"detail": "bad
     body"}`;
   * known path, wrong method → 405 `{"detail": "Method Not Allowed"}`; unknown path → 404
     `{"detail": "Not Found"}`.
   Every response uses `content-type: application/json` and compact JSON
   (`separators=(",", ":")`), sent as one start and one body event.
2. `call_asgi(app, method, path, query_string=b"", body=b"", headers=None)` → `(status, headers
   dict with str names/values, body bytes)` by running the app with `asyncio.run`. `receive`
   returns the whole body in one event (`more_body` false).

## Hints

<details><summary>Hint 1</summary>

Read the body with a loop: `chunks = []; more = True; while more: event = await receive(); chunks.append(event.get("body", b"")); more = event.get("more_body", False)`.

</details>

<details><summary>Hint 2</summary>

Keep a dict of path → allowed methods to decide between 404 and 405.

</details>

<details><summary>Hint 3</summary>

In `call_asgi`, define `async def receive(): return {"type": "http.request", "body": body, "more_body": False}` and a `send` that appends events to a list.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_root_events` | Send exactly one start event (status + headers) and then one body event. |
| `test_sum_chunked` | Keep calling `receive()` while `more_body` is true and join the chunks. |
| `test_errors` | Unknown path → 404; known path with the wrong method → 405; bad bodies → 400. |
| `test_call_asgi_client` | Build the scope, run the app with asyncio.run, and decode the recorded events. |
| `test_call_asgi_with_other_app` | Join every body event, and decode header byte pairs into strings. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The app inspects the scope, decides between 404, 405 and a handler, and always replies with one
start and one body event through a shared helper. The body reader honours `more_body`, so chunked
uploads work. `call_asgi` is a miniature test client: it fabricates the scope and `receive`,
records everything passed to `send`, and converts the recorded events back into a status,
headers and body.

## References

- [ASGI (Asynchronous Server Gateway Interface) Specification](https://asgi.readthedocs.io/en/latest/specs/main.html) — ASGI project (`S069`)
- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
