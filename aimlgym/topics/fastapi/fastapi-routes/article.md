# First FastAPI Routes

## Learning outcomes

After this lesson you can:

- Create a FastAPI application and register path operations with decorators
- Declare typed path parameters and get automatic 422 errors
- Test an app in-process with TestClient
- Relate FastAPI's routing to the router you wrote by hand

## Intuition
Everything from the first seven steps — parsing requests, choosing status codes, routing,
converting path parameters, speaking ASGI — is what FastAPI does for you. You write ordinary
Python functions with type hints; FastAPI turns them into an ASGI application, validates inputs
from the hints and documents the API automatically.

## Precise explanation
```python
from fastapi import FastAPI

app = FastAPI(title="Epoch Learn API")

@app.get("/items/{item_id}")          # method + path pattern, like Router.route
def read_item(item_id: int):           # the hint makes FastAPI convert and validate
    return {"item_id": item_id}       # dicts are returned as JSON with status 200
```
* `@app.get`, `@app.post`, `@app.put`, `@app.delete`, ... register **path operations**.
* `{item_id}` in the path becomes the parameter of the same name; `int` means `/items/abc` gets a
  **422** response with `loc: ["path", "item_id"]` — exactly what FA-05 produced.
* Unknown paths → 404 and wrong methods → 405, automatically.
* Routes are matched in order: declare `/users/me` before `/users/{name}`.
* **Testing**: `TestClient(app)` (from `fastapi.testclient`, built on HTTPX) calls the ASGI app
  in-process: `client.get("/items/3").json()`. No server or network is involved — the same idea as
  FA-07's `call_asgi`.
* `app.openapi()` returns the OpenAPI schema FastAPI generated; a running server shows it as
  interactive docs at `/docs`.
* `app.routes` lists registered routes; path operations are `fastapi.routing.APIRoute` objects
  with `.path` and `.methods`.

To run a real server locally (optional): `pip install "fastapi[standard]"` and
`fastapi dev main.py`, then open `http://127.0.0.1:8000/docs`.

## Worked example
```python
from fastapi.testclient import TestClient
client = TestClient(app)
client.get("/items/21").json()       # {'item_id': 21}
client.get("/items/x").status_code   # 422
client.post("/items/21").status_code # 405
```

## Common mistakes
* Forgetting the type hint, so `item_id` arrives as a string.
* Declaring `/users/{name}` before `/users/me`, so `me` is treated as a name.
* Starting a real server inside tests instead of using `TestClient`.

## Why this matters
The following steps add query parameters, bodies, errors, response models, dependencies and
async endpoints to this same pattern.

## Library implementation

The test below runs the same requests through a copy of the hand-written router from
FA-05 and through your FastAPI app, and checks they produce the same status codes and
bodies. The difference is what you no longer write: segment matching, conversions, 404/405/422
decisions, JSON encoding and documentation.

## References

- [FastAPI Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — FastAPI (Sebastián Ramírez) (`S070`)
- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
