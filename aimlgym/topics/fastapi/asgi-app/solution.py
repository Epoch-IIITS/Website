r"""Reference solution for FA-07 A Minimal ASGI Application.

The app inspects the scope, decides between 404, 405 and a handler, and always replies with one
start and one body event through a shared helper. The body reader honours `more_body`, so chunked
uploads work. `call_asgi` is a miniature test client: it fabricates the scope and `receive`,
records everything passed to `send`, and converts the recorded events back into a status,
headers and body.
"""
import asyncio
import json
from urllib.parse import parse_qs

ROUTES = {"/": "GET", "/echo": "GET", "/sum": "POST"}


async def send_json(send, status, payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": body})


async def read_body(receive):
    chunks, more = [], True
    while more:
        event = await receive()
        chunks.append(event.get("body", b""))
        more = event.get("more_body", False)
    return b"".join(chunks)


async def app(scope, receive, send):
    path, method = scope["path"], scope["method"]
    if path not in ROUTES:
        return await send_json(send, 404, {"detail": "Not Found"})
    if method != ROUTES[path]:
        return await send_json(send, 405, {"detail": "Method Not Allowed"})
    if path == "/":
        return await send_json(send, 200, {"message": "hello"})
    if path == "/echo":
        params = parse_qs(scope.get("query_string", b"").decode())
        return await send_json(send, 200, {"params": {k: v[0] for k, v in params.items()}})
    try:
        data = json.loads(await read_body(receive))
        numbers = data["numbers"]
        if not isinstance(numbers, list):
            raise ValueError
        total = sum(numbers)
    except (ValueError, KeyError, TypeError):
        return await send_json(send, 400, {"detail": "bad body"})
    await send_json(send, 200, {"sum": total})


def call_asgi(app, method, path, query_string=b"", body=b"", headers=None):
    scope = {"type": "http", "method": method, "path": path, "query_string": query_string,
             "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]}
    events = []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(event):
        events.append(event)

    asyncio.run(app(scope, receive, send))
    start = next(e for e in events if e["type"] == "http.response.start")
    body_out = b"".join(e.get("body", b"") for e in events if e["type"] == "http.response.body")
    hdrs = {k.decode(): v.decode() for k, v in start["headers"]}
    return start["status"], hdrs, body_out
