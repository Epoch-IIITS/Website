# FA-09 · Query and Path Parameters with Validation

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** fastapi

**Builds on:** FA-08 First FastAPI Routes

Read the lesson first: [article.md](article.md)

## Task

The starter defines `BOOKS`, a list of six dicts with `id`, `title`, `year` and `tags`, and
`app = FastAPI()`. Implement:

1. `GET /books` with parameters `q` (optional, 2–50 characters), `limit` (1–5, default 3),
   `offset` (≥ 0, default 0) and `order` (`asc`/`desc` Enum, default `asc`). Filter by
   case-insensitive substring `q` in the title, sort by `(year, id)` ascending or descending,
   and return `{"count": <number of matches>, "items": <the page of matching books>}`.
2. `GET /books/by-year/{year}` with `year` between 1900 and 2100 (`Path`) → list of titles from
   that year in id order (possibly empty).
3. `GET /books/tagged` with a repeated query parameter `tag` (default empty list) → ids of books
   that have **all** the given tags, in id order.

## Hints

<details><summary>Hint 1</summary>

`class Order(str, Enum): asc = "asc"; desc = "desc"` and the parameter `order: Order = Order.asc`.

</details>

<details><summary>Hint 2</summary>

`limit: Annotated[int, Query(ge=1, le=5)] = 3`; `year: Annotated[int, Path(ge=1900, le=2100)]`.

</details>

<details><summary>Hint 3</summary>

`sorted(matches, key=lambda b: (b["year"], b["id"]), reverse=order == Order.desc)`; tags: `tag: Annotated[list[str], Query()] = []` and `set(tag) <= set(b["tags"])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_defaults` | Sort by (year, id) ascending by default and return 3 items. |
| `test_filter_sort_page` | Filter case-insensitively, reverse the sort for desc, then slice `[offset:offset + limit]`. |
| `test_limits_validated` | Declare the constraints with `Annotated[..., Query(...)]` and use an Enum for order. |
| `test_by_year` | Use `Annotated[int, Path(ge=1900, le=2100)]` for the year. |
| `test_tagged` | Declare `tag: Annotated[list[str], Query()] = []` and keep books whose tags include all of them. |
| `test_documented_in_openapi` | Constraints declared with Query appear in the OpenAPI schema. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All validation is declared in the signatures, so the bodies only filter, sort and slice. The Enum
restricts `order` to two strings, `Path` bounds the year, and the list-typed query parameter
collects repeated `tag` values. FastAPI produces 422 responses for every rule violation before the
function runs.

## References

- [FastAPI Tutorial: Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) — FastAPI (Sebastián Ramírez) (`S072`)
- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [FastAPI Tutorial: Testing](https://fastapi.tiangolo.com/tutorial/testing/) — FastAPI (Sebastián Ramírez) (`S078`)
