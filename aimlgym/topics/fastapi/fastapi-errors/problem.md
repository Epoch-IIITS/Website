# FA-11 · Handling Errors in FastAPI

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** fastapi

**Builds on:** FA-10 Request Bodies with Pydantic

Read the lesson first: [article.md](article.md)

## Task

Define `class OutOfStock(Exception)` storing `item`, `requested` and `available`, and
`create_app()` returning a new `FastAPI` app with its own stock dict
`{1: {"name": "pen", "stock": 3}, 2: {"name": "ink", "stock": 0}}`:

* `GET /items/{item_id}` (int) → `{"id", "name", "stock"}`; unknown id → `HTTPException(404,
  detail="Item not found", headers={"X-Error": "missing"})`.
* `POST /items/{item_id}/buy` with query `qty` (int, ≥ 1, default 1): unknown id → same 404;
  `qty` larger than the stock → raise `OutOfStock`; otherwise subtract and return
  `{"item": name, "remaining": stock}`.
* Handler for `OutOfStock` → 409 `{"error": "out_of_stock", "item", "requested", "available"}`.
* Handler for `RequestValidationError` → 422 `{"error": "validation_error", "fields": [...]}` where
  each field is the error's `loc` joined with `"."` (e.g. `"path.item_id"`), in FastAPI's order.

## Hints

<details><summary>Hint 1</summary>

`if item_id not in stock: raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "missing"})`.

</details>

<details><summary>Hint 2</summary>

Declare `qty: Annotated[int, Query(ge=1)] = 1`; raise `OutOfStock(name, qty, available)` when `qty > available`.

</details>

<details><summary>Hint 3</summary>

`@app.exception_handler(RequestValidationError)` with `fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_read_ok_and_404` | Raise HTTPException(404, detail=..., headers={"X-Error": "missing"}) for unknown ids. |
| `test_buy_reduces_stock` | Subtract qty from the stored stock and default qty to 1. |
| `test_out_of_stock_409` | Raise OutOfStock before changing stock and map it to 409 in an exception handler. |
| `test_validation_format` | Register a RequestValidationError handler that joins each loc with '.'. |
| `test_fresh_state_per_app` | Create the stock dict inside create_app, not at module level. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A shared `find` helper raises the 404 in one place. The purchase logic raises a domain exception
that knows nothing about HTTP, and the handler maps it to 409 with a structured body. Overriding
the validation handler changes every 422 in the app. Because the stock dict lives inside the
factory, each `create_app()` call starts from the same state.

## References

- [FastAPI Tutorial: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — FastAPI (Sebastián Ramírez) (`S074`)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
