# FA-01 · Anatomy of an HTTP Request

**Topic:** FastAPI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-23 Files, CSV and JSON

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `parse_request(raw)` → dict `{"method", "target", "version", "headers", "body"}`. Raise
   `ValueError` if: there is no `\r\n\r\n` separator; the request line does not have exactly 3
   parts; the method is not all upper-case letters; the version is not `HTTP/1.0` or `HTTP/1.1`;
   a header line has no `:`; or a `content-length` header does not equal the body's UTF-8 byte
   length. Header names are lowercased and values stripped; with no `content-length` the body is
   whatever follows the blank line.
2. `build_request(method, target, headers=None, body="")` → the raw text, with headers in the
   given order, and a `Content-Length` header added (UTF-8 bytes) when the body is non-empty and
   none was supplied.
3. `is_safe(method)` and `is_idempotent(method)` following the table above (case-insensitive;
   unknown methods are neither).

## Hints

<details><summary>Hint 1</summary>

Check `"\r\n\r\n" in raw` first; `lines[0].split(" ")` must give 3 parts; `method.isalpha() and method.isupper()`.

</details>

<details><summary>Hint 2</summary>

For each header line use `name, sep, value = line.partition(":")`; if `sep` is empty raise ValueError.

</details>

<details><summary>Hint 3</summary>

Body length in bytes: `len(body.encode("utf-8"))`. Idempotent methods are the safe ones plus PUT and DELETE.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_parse` | Lowercase header names and strip their values. |
| `test_header_values_with_colons` | Split each header at the first colon only (`str.partition`). |
| `test_rejects_malformed` | Check the blank line, the three-part request line, the method, the version, header colons and Content-Length. |
| `test_length_in_bytes` | Compare Content-Length with `len(body.encode("utf-8"))`. |
| `test_build_round_trip` | Join lines with CRLF, end headers with a blank line, and add Content-Length in bytes for non-empty bodies. |
| `test_methods` | Idempotent = GET, HEAD, OPTIONS, PUT, DELETE; compare in upper case. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The parser splits the message once at the blank line, validates the request line, then reads
headers with `partition(":")` so values containing colons (such as URLs) survive. Lowercased
names make lookups case-insensitive, and the body length is compared in bytes. The builder is the
inverse and adds `Content-Length` only when needed.

## References

- [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — MDN Web Docs (Mozilla) (`S065`)
- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112) — IETF (Fielding, Nottingham, Reschke) (`S068`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
