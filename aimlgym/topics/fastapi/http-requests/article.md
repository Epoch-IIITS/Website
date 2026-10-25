# Anatomy of an HTTP Request

## Learning outcomes

After this lesson you can:

- Name the parts of an HTTP/1.1 request: request line, headers, blank line, body
- Parse a raw request into method, target, version, headers and body
- Treat header names case-insensitively and use Content-Length
- Classify methods as safe and idempotent

## Intuition
When a browser or an app talks to a web API, it sends plain text in a fixed format: *what* it
wants to do (the **method**), *to which resource* (the **target**), some metadata (**headers**)
and optionally data (the **body**). The server answers in a similar format. Understanding this
text makes every web framework, including FastAPI, much less mysterious.

## Precise explanation
An HTTP/1.1 request (RFC 9112):
```
POST /items?debug=1 HTTP/1.1\r\n          ← request line: method, target, version
Host: api.example.com\r\n                  ← header fields "Name: value"
Content-Type: application/json\r\n
Content-Length: 15\r\n
\r\n                                       ← empty line ends the headers
{"name": "pen"}                            ← body (exactly Content-Length bytes)
```
* Lines end with **CRLF** (`\r\n`). The request line has exactly three space-separated parts.
* Header names are **case-insensitive** (`content-type` = `Content-Type`); store them lowercased.
  Values have surrounding whitespace removed.
* `Content-Length` gives the body size in **bytes**; a body with a different length is an error.
* Common methods and their meaning (RFC 9110):

| Method | Typical use | Safe | Idempotent |
|---|---|---|---|
| GET, HEAD | read | yes | yes |
| OPTIONS | ask what is allowed | yes | yes |
| PUT | replace a resource | no | yes |
| DELETE | remove a resource | no | yes |
| POST | create / process | no | no |
| PATCH | partial update | no | no |

*Safe* methods should not change server state; *idempotent* methods have the same effect whether
sent once or several times (so clients may retry them).

## Worked example
Parsing the request above gives method `POST`, target `/items?debug=1`, version `HTTP/1.1`,
headers `{"host": "api.example.com", "content-type": "application/json", "content-length": "15"}`
and body `{"name": "pen"}`.

## Common mistakes
* Splitting on `\n` and leaving `\r` at the end of every value.
* Looking up `headers["Content-Type"]` after lowercasing names.
* Measuring the body with `len(str)` instead of its UTF-8 byte length (they differ for "é").
* Using GET to change data — caches and crawlers assume GET is safe.

## Why this matters
FastAPI parses exactly this text for you; when an API misbehaves, reading the raw request is the
fastest way to see what the client really sent.

## Library implementation

The standard library parses header blocks with `http.client.parse_headers(fp)`, which reads from a
binary file object and returns an `HTTPMessage` whose lookups are case-insensitive
(`msg["content-type"]`). `http.server.BaseHTTPRequestHandler` uses it to parse whole requests.
The test below checks your header dictionary against it.

## References

- [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — MDN Web Docs (Mozilla) (`S065`)
- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112) — IETF (Fielding, Nottingham, Reschke) (`S068`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
