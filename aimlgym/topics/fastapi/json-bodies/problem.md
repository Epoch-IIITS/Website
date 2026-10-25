# FA-04 · JSON Request Bodies and Validation

**Topic:** FastAPI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** FA-03 URLs, Paths and Query Strings

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `read_json(headers, body)` → `(status, value)`: `headers` is a dict with lowercase names.
   Return `(415, {"detail": "Content-Type must be application/json"})` unless the media type
   (before any `;`, stripped, lowercased) is `application/json`; `(400, {"detail": "Invalid
   JSON"})` if `json.loads` fails; otherwise `(200, parsed_value)`.
2. `validate_item(data)` → `(item, errors)`. If `data` is not a dict: `(None, [{"loc": ["body"],
   "msg": "must be an object"}])`. Otherwise check the rules above in this order: `name`, `price`,
   `tags`, then extra fields (sorted). Messages: `"field required"`, `"must be a non-empty
   string"`, `"must be a number"`, `"must be >= 0"`, `"must be a list of strings"`,
   `"extra field not allowed"`. With no errors return the cleaned item
   `{"name", "price", "tags"}` and `[]`; otherwise `None` and the errors.
3. `json_response(status, payload)` → `(status, {"content-type": "application/json"},
   compact_json_text)`.

## Hints

<details><summary>Hint 1</summary>

`media = headers.get("content-type", "").split(";")[0].strip().lower()`; catch `json.JSONDecodeError`.

</details>

<details><summary>Hint 2</summary>

A number check: `isinstance(x, (int, float)) and not isinstance(x, bool)`.

</details>

<details><summary>Hint 3</summary>

Extra fields: `sorted(set(data) - {"name", "price", "tags"})`; append one error per field.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_read_ok_with_charset` | Compare only the media type before ';', lowercased and stripped. |
| `test_read_415` | A missing or non-JSON Content-Type gives 415. |
| `test_read_400` | Catch `json.JSONDecodeError` and return 400. |
| `test_all_errors_reported` | Collect every error in the order name, price, tags, then sorted extra fields. |
| `test_required_and_bool` | Report missing fields as 'field required' and reject booleans as numbers. |
| `test_json_response` | Use `separators=(",", ":")` for compact JSON. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The three checks run from the cheapest and most general (media type) to the most specific (field
rules), each with its own status code. Validation collects every error with a location instead of
stopping at the first, rejects booleans explicitly, and returns a cleaned copy rather than the
caller's dict.

## References

- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html) — Python Software Foundation (`S054`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
- [FastAPI Tutorial: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) — FastAPI (Sebastián Ramírez) (`S074`)
