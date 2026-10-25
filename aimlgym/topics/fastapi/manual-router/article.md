# A Router by Hand

## Learning outcomes

After this lesson you can:

- Match request paths against patterns with path parameters
- Convert typed parameters such as {item_id:int}
- Return 404, 405 (with Allow) and 422 at the right times
- Register handlers with a decorator

## Intuition
A web framework's first job is **routing**: given `GET /items/42`, find the function that
handles it and call it with `item_id=42`. Writing a small router yourself shows what
`@app.get("/items/{item_id}")` does in FastAPI (FA-08).

## Precise explanation
* A **pattern** is a path split into segments; `{name}` captures a segment as a string and
  `{name:int}` converts it to an int: `"/items/{item_id:int}"`.
* A path **matches** a pattern when both have the same number of segments and every literal
  segment is equal.
* Dispatch rules (in this order):
  1. No pattern matches the path → **404 Not Found**.
  2. Patterns match, but none for this method → **405 Method Not Allowed**, with an `allow`
     header listing the allowed methods (sorted, comma-separated).
  3. A parameter fails conversion (e.g. `abc` for `:int`) → **422** with an error located at
     `["path", "item_id"]` (FastAPI's behaviour).
  4. Otherwise call the handler with the converted path parameters as keyword arguments, plus
     `query=` the query dict. A handler returns a dict (status 200) or a `(status, dict)` tuple.
* Routes are tried in **registration order**; the first match wins, so register `/users/me`
  before `/users/{name}`.
* **Decorator registration** (PY-17): `@router.route("GET", "/items")` stores
  the function and returns it unchanged.

## Worked example
```python
router = Router()
@router.route("GET", "/items/{item_id:int}")
def get_item(item_id, query):
    return {"item_id": item_id}
router.dispatch("GET", "/items/42")     # (200, {}, {"item_id": 42})
router.dispatch("DELETE", "/items/42")  # (405, {"allow": "GET"}, {"detail": "Method Not Allowed"})
router.dispatch("GET", "/items/abc")    # (422, {}, {"detail": [{"loc": ["path", "item_id"], ...}]})
```

## Common mistakes
* Returning 404 when the path exists but the method does not (that is 405).
* Matching `/items/42/extra` against `/items/{id}` because of a prefix check.
* Converting parameters before knowing the method is allowed.

## Why this matters
FastAPI performs exactly these steps, plus validation of query parameters and bodies, before your
function runs.

## References

- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
