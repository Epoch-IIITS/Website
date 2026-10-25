# HTTP Responses and Status Codes

## Learning outcomes

After this lesson you can:

- Read and write the status line, headers and body of a response
- Choose status codes by class: 1xx–5xx
- Know the common codes an API returns
- Compare a hand-written table with http.HTTPStatus

## Intuition
Every response starts with a three-digit **status code** that tells the client, before it reads
anything else, whether the request worked. The first digit gives the category; the exact number
gives the detail. Getting status codes right is how an API communicates clearly with programs.

## Precise explanation
```
HTTP/1.1 201 Created\r\n
Content-Type: application/json\r\n
Content-Length: 11\r\n
\r\n
{"id": 7}
```
| Class | Meaning | Codes you will use |
|---|---|---|
| 1xx | informational | (rare in APIs) |
| 2xx | success | 200 OK, 201 Created, 204 No Content |
| 3xx | redirection | 301 Moved Permanently, 304 Not Modified |
| 4xx | client error — the request is wrong | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 409 Conflict, 415 Unsupported Media Type, 422 Unprocessable Content |
| 5xx | server error — the server failed | 500 Internal Server Error, 502 Bad Gateway, 504 Gateway Timeout |

* **401 vs 403**: 401 means "who are you?" (missing or invalid credentials); 403 means "I know who
  you are, and you may not".
* **400 vs 422**: 400 for unreadable requests (malformed JSON); 422 when the request is readable
  but its content fails validation — FastAPI's default for validation errors.
* `Content-Type` tells the client how to read the body; `Content-Length` is its size in bytes.
* A 204 response has no body.

## Worked example
`build_response(404, "not found")` →
`"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 9\r\n\r\nnot found"`.

## Common mistakes
* Returning 200 with `{"error": ...}` in the body; clients and monitoring then think it worked.
* Using 500 for invalid input (that is the client's error, 4xx).
* Forgetting that `Content-Length` counts bytes, not characters.

## Why this matters
FastAPI chooses many codes for you (422 for validation, 405 for wrong methods) and lets you set
others (`status_code=201`, `HTTPException(404)`); you need to know which one is right.

## Library implementation

`http.HTTPStatus` is the standard library's table of every registered status code:
`HTTPStatus(404).phrase` is `'Not Found'` and `HTTPStatus.NOT_FOUND == 404`. FastAPI re-exports
named constants as `fastapi.status.HTTP_404_NOT_FOUND`. The test checks your hand-written table
against `HTTPStatus`.

## References

- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — MDN Web Docs (Mozilla) (`S066`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
- [http — HTTP modules (HTTPStatus)](https://docs.python.org/3/library/http.html) — Python Software Foundation (`S062`)
