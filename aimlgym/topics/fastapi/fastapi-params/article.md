# Query and Path Parameters with Validation

## Learning outcomes

After this lesson you can:

- Declare optional and required query parameters with defaults
- Add constraints with Annotated, Query and Path
- Restrict a parameter to fixed choices with an Enum
- Accept repeated query parameters as a list

## Intuition
`GET /books?q=learning&limit=2&order=desc` asks for a filtered, sorted page of results. In
FA-03 you decoded such strings by hand; FastAPI reads each function parameter that is not
in the path from the query string, converts it using its type hint, and enforces any limits you
declare.

## Precise explanation
```python
from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path, Query

class Order(str, Enum):              # allowed values only: "asc" or "desc"
    asc = "asc"
    desc = "desc"

@app.get("/books")
def list_books(
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,  # optional
    limit: Annotated[int, Query(ge=1, le=5)] = 3,                          # default 3, 1..5
    offset: Annotated[int, Query(ge=0)] = 0,
    order: Order = Order.asc,
): ...
```
* A parameter **with a default** is optional; one without a default is required (missing → 422).
* `Annotated[type, Query(...)]` attaches validation (`ge`, `le`, `gt`, `lt` for numbers;
  `min_length`, `max_length`, `pattern` for strings). `Path(...)` does the same for path
  parameters. `Annotated` comes from `typing` and keeps the plain type visible.
* `str | None` means "a string or nothing".
* An `Enum` subclass of `str` limits values to its members; `order.value` is the string.
* `tag: Annotated[list[str], Query()] = []` collects `?tag=a&tag=b` into `["a", "b"]`.
* Every violation produces 422 with `loc` such as `["query", "limit"]`.

## Worked example
`GET /books?limit=9` → 422 because 9 > 5; `GET /books?order=random` → 422 (not an Order);
`GET /books?q=deep&order=desc` → books whose title contains "deep", newest first.

## Common mistakes
* Using a mutable default list outside `Query` in older styles; with `Annotated` the default
  `[]` is safe because FastAPI copies it.
* Forgetting that query values arrive as strings and relying on manual `int()` calls.
* Validating limits inside the function instead of declaring them, which hides them from the docs.

## Why this matters
Declared constraints appear in the OpenAPI schema, so clients can see the rules, and invalid
requests never reach your code.

## References

- [FastAPI Tutorial: Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) — FastAPI (Sebastián Ramírez) (`S072`)
- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
