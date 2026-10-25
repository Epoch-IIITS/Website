# Handling Errors in FastAPI

## Learning outcomes

After this lesson you can:

- Raise HTTPException with a status code, detail and headers
- Turn domain exceptions into responses with exception handlers
- Customise the validation-error response
- Build apps with a factory so every test starts from fresh state

## Intuition
A good API fails *predictably*: the client gets the right status code and a body it can act on.
FastAPI gives you two tools — raise `HTTPException` where the problem is detected, or raise your
own domain exception and convert it to a response in one central **exception handler**.

## Precise explanation
```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "missing"})
# → 404 {"detail": "Item not found"} with the extra header

class OutOfStock(Exception):            # a domain error, independent of HTTP
    def __init__(self, item, requested, available): ...

@app.exception_handler(OutOfStock)
async def out_of_stock(request: Request, exc: OutOfStock):
    return JSONResponse(status_code=409, content={"error": "out_of_stock", ...})
```
* Business code raises `OutOfStock`; only the handler knows it means 409. The same exception can
  be reused outside the web layer.
* `RequestValidationError` is what FastAPI raises for 422s. Registering a handler for it changes
  the error format for the whole app; `exc.errors()` gives the usual list of `loc`/`msg`.
* Handlers are `async def` functions taking `(request, exc)` (FA-06).
* **App factory**: `def create_app(): app = FastAPI(); ... return app`. State such as stock
  levels lives inside the factory, so each test builds a fresh app and tests cannot affect each
  other.

## Worked example
Stock `{1: pen (3 left), 2: ink (0 left)}`: `POST /items/2/buy?qty=1` raises `OutOfStock` → 409
`{"error": "out_of_stock", "item": "ink", "requested": 1, "available": 0}`.
`POST /items/1/buy?qty=0` → 422 `{"error": "validation_error", "fields": ["query.qty"]}`.

## Common mistakes
* Returning `{"error": ...}` with status 200.
* Catching every `Exception` in a handler and hiding programming errors as 400s.
* Using module-level state, so the order of tests changes the results.

## Why this matters
Consistent error bodies let clients (and agents calling your API as a tool) recover
automatically, as in AG-15.

## References

- [FastAPI Tutorial: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — FastAPI (Sebastián Ramírez) (`S074`)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
