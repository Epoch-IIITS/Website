import asyncio
import json
from urllib.parse import parse_qs


async def send_json(send, status, payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": body})


async def app(scope, receive, send):
    # TODO: route on scope["method"] and scope["path"]
    await send_json(send, 200, {"message": "hello"})


def call_asgi(app, method, path, query_string=b"", body=b"", headers=None):
    # TODO: build scope, receive and send; run with asyncio.run
    return 0, {}, b""
