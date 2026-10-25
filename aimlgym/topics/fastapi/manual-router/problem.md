# FA-05 · A Router by Hand

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** FA-04 JSON Request Bodies and Validation

Read the lesson first: [article.md](article.md)

## Task

Write `class Router` with:

* `add(method, pattern, handler)` and the decorator `route(method, pattern)`.
* `dispatch(method, path, query=None)` → `(status, headers, body)` following the four rules
  above. `query` defaults to `{}`; trailing slashes are not special (`/items/` has an empty last
  segment). Bodies: 404 → `{"detail": "Not Found"}`; 405 → `{"detail": "Method Not Allowed"}`
  with headers `{"allow": "GET, POST"}`; 422 → `{"detail": [{"loc": ["path", name], "msg":
  "value is not a valid integer"}]}`. Successful calls return headers `{}`.

Only `str` (default) and `int` converters are needed. Method names are compared in upper case.

## Hints

<details><summary>Hint 1</summary>

Write `_match(segments, parts)` returning a dict of raw params or None: lengths equal, literal segments equal, `{...}` segments captured.

</details>

<details><summary>Hint 2</summary>

First collect every route whose pattern matches the path; none → 404; none with this method → 405 with `", ".join(sorted(methods))`.

</details>

<details><summary>Hint 3</summary>

For `{name:int}`, `int(raw)` inside try/except ValueError → 422; the handler result is a dict or a `(status, dict)` tuple.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_typed_param_and_query` | Convert `{item_id:int}` with int() and pass `query=` to the handler. |
| `test_404` | A path matches only when it has the same number of segments and equal literals. |
| `test_405_allow` | If the path matches but the method does not, return 405 with the sorted allowed methods. |
| `test_422` | Catch the int() conversion error and return 422 with loc ['path', name]. |
| `test_order_and_str_param` | Try routes in registration order and compare methods in upper case. |
| `test_decorator_returns_function` | The decorator must register the function and return it unchanged. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Matching compares segment by segment, so prefixes never match. Collecting all path matches first
makes the 404/405 decision correct and lets the 405 response list every allowed method. Only the
chosen route's parameters are converted, so a type error yields 422 instead of a crash, and the
handler receives typed keyword arguments plus the query dict.

## References

- [FastAPI Tutorial: Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) — FastAPI (Sebastián Ramírez) (`S071`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
