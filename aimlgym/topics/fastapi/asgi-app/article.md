# A Minimal ASGI Application

## Learning outcomes

After this lesson you can:

- Describe the ASGI interface: scope, receive and send
- Write an async application that sends a start message and a body message
- Read a request body from receive() events
- Call an ASGI app in-process, as a test client does

## Intuition
FastAPI is built on **ASGI** (Asynchronous Server Gateway Interface): a tiny contract between a
server (such as Uvicorn) and an application. The server turns network bytes into a dict and two
async functions; the app answers by calling one of them. Writing an ASGI app by hand — and a small
in-process caller like FastAPI's test client — removes the last bit of magic.

## Precise explanation
An ASGI application is `async def app(scope, receive, send)`.
* `scope` (dict) describes the request: `scope["type"] == "http"`, `"method"`, `"path"`,
  `"query_string"` (bytes, without `?`), `"headers"` (list of `(name, value)` byte pairs with
  lower-case names).
* `await receive()` returns events `{"type": "http.request", "body": b"...", "more_body":
  bool}`; keep reading while `more_body` is true and join the chunks.
* `await send(event)` sends the response in two kinds of event:
  1. `{"type": "http.response.start", "status": 200, "headers": [(b"content-type",
     b"application/json")]}`
  2. `{"type": "http.response.body", "body": b"..."}`
* **Calling an app in tests**: build the scope, give it a `receive` that returns the body, and a
  `send` that records events; run with `asyncio.run`. No network, no server. FastAPI's
  `TestClient` does this (through HTTPX) for you.

## Worked example
For `GET /`, the app below sends start(200, JSON) then body `b'{"message":"hello"}'`;
`call_asgi(app, "GET", "/")` returns `(200, {"content-type": "application/json"},
b'{"message":"hello"}')`.

## Common mistakes
* Sending the body before the start event, or sending two start events.
* Reading only the first `receive()` chunk when `more_body` is true.
* Treating headers as a dict of strings — in ASGI they are lists of byte pairs.

## Why this matters
Every FastAPI app *is* an ASGI app (`app(scope, receive, send)`), which is why the same test
client technique works in FA-08.

## References

- [ASGI (Asynchronous Server Gateway Interface) Specification](https://asgi.readthedocs.io/en/latest/specs/main.html) — ASGI project (`S069`)
- [Coroutines and Tasks (asyncio)](https://docs.python.org/3/library/asyncio-task.html) — Python Software Foundation (`S061`)
- [FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/) — FastAPI (Sebastián Ramírez) (`S077`)
