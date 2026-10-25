# JSON Request Bodies and Validation

## Learning outcomes

After this lesson you can:

- Check Content-Type before reading a body
- Map body problems to 415, 400 and 422 status codes
- Validate fields by hand and report errors with a location and a message
- Serialise JSON responses consistently

## Intuition
A client that creates an item sends JSON in the body. Before using it, the server must check
three different things — each with its own status code: *is it JSON at all* (the Content-Type
header), *can it be parsed*, and *does it contain valid fields*. Doing this by hand once shows
exactly what Pydantic and FastAPI automate later (FA-10).

## Precise explanation
| Problem | Status |
|---|---|
| `Content-Type` is not `application/json` (parameters such as `; charset=utf-8` allowed, case-insensitive) | 415 Unsupported Media Type |
| body is not valid JSON | 400 Bad Request |
| JSON is valid but the content breaks the rules | 422 Unprocessable Content |

**Error format** (the one FastAPI uses): a list of errors, each with a **location** `loc`
(where the problem is, e.g. `["body", "price"]`) and a human-readable `msg`. Reporting *all*
problems at once saves the client several round trips.

**Validation rules** for an item in this lesson:
* `name`: required string, non-empty after stripping (store it stripped);
* `price`: required number `>= 0` — note `True` is an `int` in Python, so reject `bool`
  explicitly;
* `tags`: optional list of strings, default `[]`;
* unknown fields are errors (`["body", "<field>"]`, "extra field not allowed").

**JSON responses**: `json.dumps(payload, separators=(",", ":"))` gives compact output; send
`Content-Type: application/json`.

## Worked example
Body `{"name": " pen ", "price": -1, "colour": "red"}` → 422 with errors
`[{"loc": ["body", "price"], "msg": "must be >= 0"}, {"loc": ["body", "colour"], "msg": "extra field not allowed"}]`.

## Common mistakes
* Accepting `True` as a price.
* Returning only the first error.
* Using 400 for everything, so clients cannot tell a syntax error from a business-rule error.

## Why this matters
These checks protect every handler from bad input; FastAPI performs them before your function
runs and returns the same kind of 422 error list.

## References

- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html) — Python Software Foundation (`S054`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
- [FastAPI Tutorial: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — FastAPI (Sebastián Ramírez) (`S074`)
