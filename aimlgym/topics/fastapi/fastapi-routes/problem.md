# FA-08 · First FastAPI Routes

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** fastapi

**Builds on:** FA-07 A Minimal ASGI Application

Read the lesson first: [article.md](article.md)

## Task

Create a module-level `app = FastAPI(title="Epoch Learn API")` with:

| Method | Path | Response |
|---|---|---|
| GET | `/` | `{"message": "Hello, Epoch Learn"}` |
| GET | `/health` | `{"status": "ok"}` |
| GET | `/users/me` | `{"user": "current"}` |
| GET | `/users/{name}` | `{"user": name}` |
| GET | `/items/{item_id}` (int) | `{"item_id": item_id, "double": 2 * item_id}` |
| DELETE | `/items/{item_id}` (int) | `{"deleted": item_id}` |

Also write `route_table(app)` → sorted list of `(method, path)` tuples for every `APIRoute`
in `app.routes` (one tuple per method).

## Hints

<details><summary>Hint 1</summary>

`@app.get("/items/{item_id}")` above `def read_item(item_id: int):`.

</details>

<details><summary>Hint 2</summary>

Register `/users/me` before `/users/{name}`.

</details>

<details><summary>Hint 3</summary>

`sorted((m, r.path) for r in app.routes if isinstance(r, APIRoute) for m in r.methods)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_typed_path_param` | Annotate `item_id: int` so FastAPI converts it. |
| `test_validation_422` | With an `int` hint, FastAPI rejects 'abc' with 422 automatically — check the hint. |
| `test_404_and_405` | Register GET and DELETE for /items/{item_id}; FastAPI answers other methods with 405. |
| `test_route_order` | Declare `/users/me` before `/users/{name}`. |
| `test_route_table_and_openapi` | Collect `(method, route.path)` for APIRoute objects and sort the list; set the app title. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each decorator registers one path operation; type hints drive conversion and validation, so the
handlers contain only the response logic. Declaring the fixed `/users/me` route first keeps it
from being captured by the parameterised route. `route_table` reads the same registry FastAPI
uses for routing and for the OpenAPI schema.

## References

- [FastAPI Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — FastAPI (Sebastián Ramírez) (`S070`)
- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
