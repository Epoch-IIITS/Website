# FA-02 · HTTP Responses and Status Codes

**Topic:** FastAPI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** FA-01 Anatomy of an HTTP Request

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `status_class(code)` → `"informational"`, `"success"`, `"redirection"`, `"client error"` or
   `"server error"`; raise `ValueError` outside 100–599.
2. `reason(code)` → reason phrase from your own dict `REASONS` containing at least: 200 OK,
   201 Created, 204 No Content, 301 Moved Permanently, 304 Not Modified, 400 Bad Request,
   401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 409 Conflict,
   415 Unsupported Media Type, 422 Unprocessable Content, 500 Internal Server Error,
   502 Bad Gateway, 504 Gateway Timeout. Unknown codes → `"Unknown"`.
3. `build_response(status, body="", content_type="text/plain; charset=utf-8")` → raw response
   text as in the worked example. For 204, omit `Content-Type` and `Content-Length` and raise
   `ValueError` if a body is given.
4. `parse_response(raw)` → `{"status": int, "reason": str, "headers": dict (lowercased names),
   "body": str}`. The reason phrase may contain spaces.

## Hints

<details><summary>Hint 1</summary>

`status_class` can index a list with `code // 100 - 1` after checking the range.

</details>

<details><summary>Hint 2</summary>

Content-Length is `len(body.encode("utf-8"))`; for 204 the head is only the status line.

</details>

<details><summary>Hint 3</summary>

Status line: `version, code, phrase = line.split(" ", 2)` keeps spaces inside the phrase.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_classes` | Map `code // 100` to the five classes and reject codes outside 100–599. |
| `test_reasons` | Fill `REASONS` with every code listed in the task. |
| `test_build_bytes_and_type` | Content-Length counts UTF-8 bytes, and Content-Type uses the given value. |
| `test_no_content` | 204 responses have only the status line; reject a body. |
| `test_parse_round_trip` | Split the status line with `split(" ", 2)` and lowercase header names. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Integer division by 100 maps a code to its class. The response builder mirrors the request
builder from the previous step, with the special case that 204 carries neither a body nor body
headers. `split(" ", 2)` splits the status line into exactly three parts so multi-word phrases
stay intact.

## References

- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
- [http — HTTP modules (HTTPStatus)](https://docs.python.org/3/library/http.html) — Python Software Foundation (`S062`)
