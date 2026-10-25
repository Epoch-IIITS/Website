"""FastAPI topic, part 1 (standard library only): HTTP messages, status codes, URLs, JSON
bodies, a hand-made router, asyncio and a minimal ASGI application."""

PROBLEMS = [
# ---------------------------------------------------------------- http-requests
{
"slug": "http-requests", "title": "Anatomy of an HTTP Request",
"difficulty": "beginner", "prereqs": ["files-and-json"], "packages": [],
"objectives": ["Name the parts of an HTTP/1.1 request: request line, headers, blank line, body",
               "Parse a raw request into method, target, version, headers and body",
               "Treat header names case-insensitively and use Content-Length",
               "Classify methods as safe and idempotent"],
"tags": ["http", "requests", "headers", "methods", "parsing"],
"sources": ["S065", "S068", "S067"], "entry": "parse_request(raw); build_request(method, target, headers=None, body=''); is_safe(method); is_idempotent(method)",
"article": r'''
# Anatomy of an HTTP Request

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
''',
"statement": r'''
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
''',
"starter": r'''
SAFE = {"GET", "HEAD", "OPTIONS"}


def parse_request(raw):
    head, _, body = raw.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, target, version = lines[0].split(" ")
    # TODO: validation and headers
    return {"method": method, "target": target, "version": version, "headers": {}, "body": body}


def build_request(method, target, headers=None, body=""):
    # TODO
    return ""


def is_safe(method):
    return method.upper() in SAFE


def is_idempotent(method):
    # TODO
    return False
''',
"hints": [
    "Check `\"\\r\\n\\r\\n\" in raw` first; `lines[0].split(\" \")` must give 3 parts; `method.isalpha() and method.isupper()`.",
    "For each header line use `name, sep, value = line.partition(\":\")`; if `sep` is empty raise ValueError.",
    "Body length in bytes: `len(body.encode(\"utf-8\"))`. Idempotent methods are the safe ones plus PUT and DELETE.",
],
"solution": r'''
SAFE = {"GET", "HEAD", "OPTIONS"}
IDEMPOTENT = SAFE | {"PUT", "DELETE"}


def parse_request(raw):
    if "\r\n\r\n" not in raw:
        raise ValueError("missing blank line after headers")
    head, _, body = raw.partition("\r\n\r\n")
    lines = head.split("\r\n")
    parts = lines[0].split(" ")
    if len(parts) != 3:
        raise ValueError("bad request line")
    method, target, version = parts
    if not (method.isalpha() and method.isupper()):
        raise ValueError("bad method")
    if version not in ("HTTP/1.0", "HTTP/1.1"):
        raise ValueError("unsupported version")
    headers = {}
    for line in lines[1:]:
        name, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"bad header line {line!r}")
        headers[name.strip().lower()] = value.strip()
    if "content-length" in headers and int(headers["content-length"]) != len(body.encode("utf-8")):
        raise ValueError("Content-Length does not match body")
    return {"method": method, "target": target, "version": version, "headers": headers, "body": body}


def build_request(method, target, headers=None, body=""):
    headers = dict(headers or {})
    if body and not any(k.lower() == "content-length" for k in headers):
        headers["Content-Length"] = str(len(body.encode("utf-8")))
    lines = [f"{method} {target} HTTP/1.1"] + [f"{k}: {v}" for k, v in headers.items()]
    return "\r\n".join(lines) + "\r\n\r\n" + body


def is_safe(method):
    return method.upper() in SAFE


def is_idempotent(method):
    return method.upper() in IDEMPOTENT
''',
"explanation": r'''
The parser splits the message once at the blank line, validates the request line, then reads
headers with `partition(":")` so values containing colons (such as URLs) survive. Lowercased
names make lookups case-insensitive, and the body length is compared in bytes. The builder is the
inverse and adds `Content-Length` only when needed.
''',
"tests": r'''
RAW = ('POST /items?debug=1 HTTP/1.1\r\nHost: api.example.com\r\nContent-Type: application/json\r\n'
       'Content-Length: 15\r\n\r\n{"name": "pen"}')


class TestHttpRequest(unittest.TestCase):
    def test_parse(self):
        r = S.parse_request(RAW)
        self.assertEqual((r["method"], r["target"], r["version"]), ("POST", "/items?debug=1", "HTTP/1.1"))
        self.assertEqual(r["headers"], {"host": "api.example.com", "content-type": "application/json",
                                        "content-length": "15"})
        self.assertEqual(r["body"], '{"name": "pen"}')

    def test_header_values_with_colons(self):
        r = S.parse_request("GET / HTTP/1.1\r\nReferer:  http://x.org:8080/a \r\n\r\n")
        self.assertEqual(r["headers"]["referer"], "http://x.org:8080/a")
        self.assertEqual(r["body"], "")

    def test_rejects_malformed(self):
        bad = ["GET / HTTP/1.1\r\nHost: x\r\n",
               "GET /  HTTP/1.1\r\n\r\n",
               "get / HTTP/1.1\r\n\r\n",
               "GET / HTTP/2\r\n\r\n",
               "GET / HTTP/1.1\r\nNoColonHere\r\n\r\n",
               "POST / HTTP/1.1\r\nContent-Length: 3\r\n\r\nab"]
        for raw in bad:
            with self.assertRaises(ValueError, msg=raw):
                S.parse_request(raw)

    def test_length_in_bytes(self):
        r = S.parse_request("POST / HTTP/1.1\r\nContent-Length: 6\r\n\r\ncafé!")
        self.assertEqual(r["body"], "café!")

    def test_build_round_trip(self):
        raw = S.build_request("PUT", "/items/3", {"Host": "x", "Content-Type": "text/plain"}, "héllo")
        self.assertEqual(raw, "PUT /items/3 HTTP/1.1\r\nHost: x\r\nContent-Type: text/plain\r\nContent-Length: 6\r\n\r\nhéllo")
        self.assertEqual(S.parse_request(raw)["body"], "héllo")
        self.assertEqual(S.build_request("GET", "/"), "GET / HTTP/1.1\r\n\r\n")

    def test_methods(self):
        self.assertEqual([S.is_safe(m) for m in ("GET", "head", "POST", "DELETE")], [True, True, False, False])
        self.assertEqual([S.is_idempotent(m) for m in ("GET", "PUT", "delete", "POST", "PATCH", "BREW")],
                         [True, True, True, False, False, False])
''',
"feedback": [
    ("test_parse", "Lowercase header names and strip their values."),
    ("test_header_values_with_colons", "Split each header at the first colon only (`str.partition`)."),
    ("test_rejects_malformed", "Check the blank line, the three-part request line, the method, the version, header colons and Content-Length."),
    ("test_length_in_bytes", "Compare Content-Length with `len(body.encode(\"utf-8\"))`."),
    ("test_build_round_trip", "Join lines with CRLF, end headers with a blank line, and add Content-Length in bytes for non-empty bodies."),
    ("test_methods", "Idempotent = GET, HEAD, OPTIONS, PUT, DELETE; compare in upper case."),
],
"library": {
"text": r'''
The standard library parses header blocks with `http.client.parse_headers(fp)`, which reads from a
binary file object and returns an `HTTPMessage` whose lookups are case-insensitive
(`msg["content-type"]`). `http.server.BaseHTTPRequestHandler` uses it to parse whole requests.
The test below checks your header dictionary against it.
''',
"tests": r'''
import http.client
import io


class TestAgainstLibrary(unittest.TestCase):
    def test_headers_match_http_client(self):
        head = RAW.split("\r\n\r\n")[0].split("\r\n", 1)[1] + "\r\n\r\n"
        msg = http.client.parse_headers(io.BytesIO(head.encode()))
        ours = S.parse_request(RAW)["headers"]
        self.assertEqual(ours, {k.lower(): v for k, v in msg.items()})
''',
},
},
# ---------------------------------------------------------------- http-responses
{
"slug": "http-responses", "title": "HTTP Responses and Status Codes",
"difficulty": "beginner", "prereqs": ["http-requests"], "packages": [],
"objectives": ["Read and write the status line, headers and body of a response",
               "Choose status codes by class: 1xx–5xx", "Know the common codes an API returns",
               "Compare a hand-written table with http.HTTPStatus"],
"tags": ["http", "responses", "status-codes", "content-type"],
"sources": ["S066", "S067", "S062"], "entry": "status_class(code); reason(code); build_response(status, body='', content_type='text/plain; charset=utf-8'); parse_response(raw)",
"article": r'''
# HTTP Responses and Status Codes

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
''',
"statement": r'''
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
''',
"starter": r'''
REASONS = {200: "OK", 404: "Not Found"}


def status_class(code):
    # TODO
    return "success"


def reason(code):
    return REASONS.get(code, "Unknown")


def build_response(status, body="", content_type="text/plain; charset=utf-8"):
    # TODO
    return f"HTTP/1.1 {status} {reason(status)}\r\n\r\n{body}"


def parse_response(raw):
    # TODO
    return {}
''',
"hints": [
    "`status_class` can index a list with `code // 100 - 1` after checking the range.",
    "Content-Length is `len(body.encode(\"utf-8\"))`; for 204 the head is only the status line.",
    "Status line: `version, code, phrase = line.split(\" \", 2)` keeps spaces inside the phrase.",
],
"solution": r'''
REASONS = {
    200: "OK", 201: "Created", 204: "No Content", 301: "Moved Permanently", 304: "Not Modified",
    400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found",
    405: "Method Not Allowed", 409: "Conflict", 415: "Unsupported Media Type",
    422: "Unprocessable Content", 500: "Internal Server Error", 502: "Bad Gateway",
    504: "Gateway Timeout",
}
CLASSES = ["informational", "success", "redirection", "client error", "server error"]


def status_class(code):
    if not 100 <= code <= 599:
        raise ValueError("status codes are 100-599")
    return CLASSES[code // 100 - 1]


def reason(code):
    return REASONS.get(code, "Unknown")


def build_response(status, body="", content_type="text/plain; charset=utf-8"):
    lines = [f"HTTP/1.1 {status} {reason(status)}"]
    if status == 204:
        if body:
            raise ValueError("204 responses have no body")
    else:
        lines += [f"Content-Type: {content_type}", f"Content-Length: {len(body.encode('utf-8'))}"]
    return "\r\n".join(lines) + "\r\n\r\n" + body


def parse_response(raw):
    head, _, body = raw.partition("\r\n\r\n")
    lines = head.split("\r\n")
    _, code, phrase = lines[0].split(" ", 2)
    headers = {}
    for line in lines[1:]:
        name, _, value = line.partition(":")
        headers[name.strip().lower()] = value.strip()
    return {"status": int(code), "reason": phrase, "headers": headers, "body": body}
''',
"explanation": r'''
Integer division by 100 maps a code to its class. The response builder mirrors the request
builder from the previous step, with the special case that 204 carries neither a body nor body
headers. `split(" ", 2)` splits the status line into exactly three parts so multi-word phrases
stay intact.
''',
"tests": r'''
class TestHttpResponses(unittest.TestCase):
    def test_classes(self):
        self.assertEqual([S.status_class(c) for c in (101, 200, 204, 301, 404, 422, 503)],
                         ["informational", "success", "success", "redirection", "client error",
                          "client error", "server error"])
        for bad in (99, 600):
            with self.assertRaises(ValueError):
                S.status_class(bad)

    def test_reasons(self):
        self.assertEqual(S.reason(201), "Created")
        self.assertEqual(S.reason(422), "Unprocessable Content")
        self.assertEqual(S.reason(415), "Unsupported Media Type")
        self.assertEqual(S.reason(299), "Unknown")

    def test_build(self):
        self.assertEqual(S.build_response(404, "not found"),
                         "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 9\r\n\r\nnot found")

    def test_build_bytes_and_type(self):
        raw = S.build_response(201, '{"name": "café"}', "application/json")
        self.assertIn("Content-Length: 17\r\n", raw)
        self.assertTrue(raw.startswith("HTTP/1.1 201 Created\r\nContent-Type: application/json\r\n"))

    def test_no_content(self):
        self.assertEqual(S.build_response(204), "HTTP/1.1 204 No Content\r\n\r\n")
        with self.assertRaises(ValueError):
            S.build_response(204, "oops")

    def test_parse_round_trip(self):
        r = S.parse_response(S.build_response(500, "boom"))
        self.assertEqual(r, {"status": 500, "reason": "Internal Server Error",
                             "headers": {"content-type": "text/plain; charset=utf-8", "content-length": "4"},
                             "body": "boom"})
''',
"feedback": [
    ("test_classes", "Map `code // 100` to the five classes and reject codes outside 100–599."),
    ("test_reasons", "Fill `REASONS` with every code listed in the task."),
    ("test_build_bytes_and_type", "Content-Length counts UTF-8 bytes, and Content-Type uses the given value."),
    ("test_no_content", "204 responses have only the status line; reject a body."),
    ("test_parse_round_trip", "Split the status line with `split(\" \", 2)` and lowercase header names."),
],
"library": {
"text": r'''
`http.HTTPStatus` is the standard library's table of every registered status code:
`HTTPStatus(404).phrase` is `'Not Found'` and `HTTPStatus.NOT_FOUND == 404`. FastAPI re-exports
named constants as `fastapi.status.HTTP_404_NOT_FOUND`. The test checks your hand-written table
against `HTTPStatus`.
''',
"tests": r'''
from http import HTTPStatus


class TestAgainstLibrary(unittest.TestCase):
    def test_reasons_match_httpstatus(self):
        for code in S.REASONS:
            self.assertEqual(S.reason(code), HTTPStatus(code).phrase, code)
''',
},
},
# ---------------------------------------------------------------- urls-query
{
"slug": "urls-query", "title": "URLs, Paths and Query Strings",
"difficulty": "beginner", "prereqs": ["http-responses"], "packages": [],
"objectives": ["Split a URL into scheme, host, port, path, query and fragment",
               "Decode percent-encoding and '+' in query strings",
               "Represent repeated query parameters as lists",
               "Compare a manual parser with urllib.parse"],
"tags": ["urls", "query-strings", "percent-encoding", "parsing"],
"sources": ["S065", "S063", "S067"], "entry": "split_url(url); percent_decode(text, plus_as_space=True); parse_query(qs); build_query(params)",
"article": r'''
# URLs, Paths and Query Strings

## Intuition
`https://api.example.com:8443/search?q=deep+learning&tag=ml&tag=ai#top` packs a lot into one
line: *how* to connect (scheme), *where* (host and port), *which resource* (path), *options*
(query) and a client-side bookmark (fragment). APIs read the path and query to decide what to do.

## Precise explanation
```
https :// api.example.com : 8443 /search ? q=deep+learning&tag=ml&tag=ai # top
scheme    host               port path     query                           fragment
```
* Default ports: 80 for `http`, 443 for `https`. A missing path means `/`.
* The **query** is `key=value` pairs joined by `&`. A key may repeat (`tag=ml&tag=ai`), so the
  natural representation is a dict of **lists**. A key without `=` has value `""`.
* **Percent-encoding** writes bytes that are not allowed literally as `%XX` (hex): space is
  `%20`, `é` is the two UTF-8 bytes `%C3%A9`. In query strings `+` also means space.
  Decode by collecting bytes and decoding them as UTF-8 at the end.
* The fragment is never sent to the server.

## Worked example
`parse_query("q=deep+learning&tag=ml&tag=ai&empty")` →
`{"q": ["deep learning"], "tag": ["ml", "ai"], "empty": [""]}`.
`percent_decode("caf%C3%A9")` → `"café"`.

## Common mistakes
* Decoding `%C3` and `%A9` separately into two characters instead of one `é`.
* Splitting on `=` more than once (`a=b=c` has key `a` and value `b=c`).
* Keeping only the last value of a repeated key.
* Treating `+` as a space in the path (it is literal there).

## Why this matters
FastAPI turns `?q=...&limit=...` into typed function arguments ([[fastapi-params]]); knowing the
raw format explains how lists and missing values arrive.
''',
"statement": r'''
Without `urllib`, implement:

1. `split_url(url)` → dict `scheme, host, port (int), path, query (str), fragment` for `http` and
   `https` URLs (raise `ValueError` for other schemes or a missing `://`). Use the default port when
   none is given and `/` for an empty path. `query` and `fragment` are raw strings (`""` if absent).
2. `percent_decode(text, plus_as_space=True)` → decoded text (`%XX` → byte, `+` → space when
   `plus_as_space`); raise `ValueError` for a `%` not followed by two hex digits.
3. `parse_query(qs)` → dict of lists, in first-appearance order of keys; skip empty pieces
   (e.g. from `a=1&&b=2`). Decode keys and values.
4. `build_query(params)` → the inverse for a dict of lists (or single string values): encode
   letters, digits and `-._~` literally, spaces as `+`, every other byte as `%XX` (upper-case hex).
''',
"starter": r'''
SAFE_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~")
DEFAULT_PORTS = {"http": 80, "https": 443}


def split_url(url):
    # TODO
    return {}


def percent_decode(text, plus_as_space=True):
    # TODO: collect bytes, decode UTF-8 at the end
    return text


def parse_query(qs):
    # TODO
    return {}


def build_query(params):
    # TODO
    return ""
''',
"hints": [
    "`scheme, sep, rest = url.partition(\"://\")`; then split off `#fragment`, then `?query`, then the first `/` separates host[:port] from the path.",
    "Build a `bytearray`: for `%` append `int(text[i+1:i+3], 16)`, for `+` append a space, otherwise `out += ch.encode(\"utf-8\")`; finally `out.decode(\"utf-8\")`.",
    "In `build_query`, encode each value with `.encode(\"utf-8\")` and loop over the bytes: `chr(b) in SAFE_CHARS` → literal, `b == 32` → `+`, else `f\"%{b:02X}\"`.",
],
"solution": r'''
SAFE_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~")
DEFAULT_PORTS = {"http": 80, "https": 443}
HEX = set("0123456789abcdefABCDEF")


def split_url(url):
    scheme, sep, rest = url.partition("://")
    if not sep or scheme not in DEFAULT_PORTS:
        raise ValueError("only http(s) URLs are supported")
    rest, _, fragment = rest.partition("#")
    rest, _, query = rest.partition("?")
    slash = rest.find("/")
    authority, path = (rest, "/") if slash == -1 else (rest[:slash], rest[slash:])
    host, colon, port = authority.partition(":")
    return {"scheme": scheme, "host": host, "port": int(port) if colon else DEFAULT_PORTS[scheme],
            "path": path or "/", "query": query, "fragment": fragment}


def percent_decode(text, plus_as_space=True):
    out = bytearray()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "%":
            pair = text[i + 1:i + 3]
            if len(pair) != 2 or not set(pair) <= HEX:
                raise ValueError("bad percent escape")
            out.append(int(pair, 16))
            i += 3
            continue
        if ch == "+" and plus_as_space:
            out.append(32)
        else:
            out += ch.encode("utf-8")
        i += 1
    return out.decode("utf-8")


def parse_query(qs):
    result = {}
    for piece in qs.split("&"):
        if not piece:
            continue
        key, _, value = piece.partition("=")
        result.setdefault(percent_decode(key), []).append(percent_decode(value))
    return result


def _encode(text):
    out = []
    for b in str(text).encode("utf-8"):
        if chr(b) in SAFE_CHARS:
            out.append(chr(b))
        elif b == 32:
            out.append("+")
        else:
            out.append(f"%{b:02X}")
    return "".join(out)


def build_query(params):
    pairs = []
    for key, values in params.items():
        if isinstance(values, str):
            values = [values]
        pairs += [f"{_encode(key)}={_encode(v)}" for v in values]
    return "&".join(pairs)
''',
"explanation": r'''
The URL is peeled from the outside in: fragment, query, then the first slash separates the
authority from the path. Percent-decoding works on bytes so multi-byte UTF-8 characters are
rebuilt correctly. Queries become a dict of lists with `setdefault`, and the encoder is the exact
inverse for the characters it escapes.
''',
"tests": r'''
class TestUrls(unittest.TestCase):
    def test_split_full(self):
        self.assertEqual(S.split_url("https://api.example.com:8443/search?q=deep+learning&tag=ml#top"),
                         {"scheme": "https", "host": "api.example.com", "port": 8443, "path": "/search",
                          "query": "q=deep+learning&tag=ml", "fragment": "top"})

    def test_split_defaults(self):
        u = S.split_url("http://localhost")
        self.assertEqual((u["port"], u["path"], u["query"], u["fragment"]), (80, "/", "", ""))
        self.assertEqual(S.split_url("https://x.org?a=1")["path"], "/")
        with self.assertRaises(ValueError):
            S.split_url("ftp://x.org/file")

    def test_percent_decode(self):
        self.assertEqual(S.percent_decode("caf%C3%A9+au+lait"), "café au lait")
        self.assertEqual(S.percent_decode("a+b", plus_as_space=False), "a+b")
        with self.assertRaises(ValueError):
            S.percent_decode("100%")

    def test_parse_query(self):
        self.assertEqual(S.parse_query("q=deep+learning&tag=ml&tag=ai&empty&&x=a%3Db"),
                         {"q": ["deep learning"], "tag": ["ml", "ai"], "empty": [""], "x": ["a=b"]})
        self.assertEqual(S.parse_query(""), {})

    def test_value_with_equals(self):
        self.assertEqual(S.parse_query("expr=a=b"), {"expr": ["a=b"]})

    def test_build_round_trip(self):
        params = {"q": ["café au lait"], "tag": ["ml", "a&b"], "x": "1/2"}
        qs = S.build_query(params)
        self.assertEqual(qs, "q=caf%C3%A9+au+lait&tag=ml&tag=a%26b&x=1%2F2")
        self.assertEqual(S.parse_query(qs), {"q": ["café au lait"], "tag": ["ml", "a&b"], "x": ["1/2"]})
''',
"feedback": [
    ("test_split_full", "Remove the fragment first, then the query, then split host and port at ':'."),
    ("test_split_defaults", "Use port 80/443 when missing and '/' for an empty path; reject other schemes."),
    ("test_percent_decode", "Collect raw bytes and decode them together with UTF-8; reject a lone '%'."),
    ("test_parse_query", "Skip empty pieces, keep every value of repeated keys in a list, and decode both sides."),
    ("test_value_with_equals", "Split each pair at the first '=' only."),
    ("test_build_round_trip", "Encode spaces as '+', unsafe bytes as upper-case %XX."),
],
"library": {
"text": r'''
`urllib.parse` implements all of this: `urlsplit(url)` returns scheme, netloc, path, query and
fragment (`.hostname` and `.port` split the netloc), `unquote_plus` decodes, `parse_qs(qs,
keep_blank_values=True)` returns the same dict of lists, and `urlencode(params, doseq=True)`
builds queries. The tests check your functions agree with them.
''',
"tests": r'''
from urllib.parse import parse_qs, unquote_plus, urlencode, urlsplit


class TestAgainstLibrary(unittest.TestCase):
    def test_split_matches_urlsplit(self):
        url = "https://api.example.com:8443/a/b?x=1#frag"
        ours, theirs = S.split_url(url), urlsplit(url)
        self.assertEqual((ours["host"], ours["port"], ours["path"], ours["query"], ours["fragment"]),
                         (theirs.hostname, theirs.port, theirs.path, theirs.query, theirs.fragment))

    def test_query_matches_parse_qs(self):
        qs = "q=deep+learning&tag=ml&tag=ai&empty=&z=%E2%82%AC"
        self.assertEqual(S.parse_query(qs), parse_qs(qs, keep_blank_values=True))
        self.assertEqual(S.percent_decode("%E2%82%AC+5"), unquote_plus("%E2%82%AC+5"))

    def test_build_matches_urlencode(self):
        params = {"q": ["café au lait"], "n": ["1", "2"]}
        self.assertEqual(S.build_query(params), urlencode(params, doseq=True))
''',
},
},
# ---------------------------------------------------------------- json-bodies
{
"slug": "json-bodies", "title": "JSON Request Bodies and Validation",
"difficulty": "intermediate", "prereqs": ["urls-query"], "packages": [],
"objectives": ["Check Content-Type before reading a body",
               "Map body problems to 415, 400 and 422 status codes",
               "Validate fields by hand and report errors with a location and a message",
               "Serialise JSON responses consistently"],
"tags": ["json", "validation", "content-type", "error-format"],
"sources": ["S054", "S067", "S074"], "entry": "read_json(headers, body); validate_item(data); json_response(status, payload)",
"article": r'''
# JSON Request Bodies and Validation

## Intuition
A client that creates an item sends JSON in the body. Before using it, the server must check
three different things — each with its own status code: *is it JSON at all* (the Content-Type
header), *can it be parsed*, and *does it contain valid fields*. Doing this by hand once shows
exactly what Pydantic and FastAPI automate later ([[pydantic-bodies]]).

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
''',
"statement": r'''
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
''',
"starter": r'''
import json


def read_json(headers, body):
    # TODO: 415, 400 or 200
    return 200, json.loads(body)


def validate_item(data):
    errors = []
    # TODO
    return data, errors


def json_response(status, payload):
    # TODO
    return status, {}, json.dumps(payload)
''',
"hints": [
    "`media = headers.get(\"content-type\", \"\").split(\";\")[0].strip().lower()`; catch `json.JSONDecodeError`.",
    "A number check: `isinstance(x, (int, float)) and not isinstance(x, bool)`.",
    "Extra fields: `sorted(set(data) - {\"name\", \"price\", \"tags\"})`; append one error per field.",
],
"solution": r'''
import json

FIELDS = {"name", "price", "tags"}


def read_json(headers, body):
    media = headers.get("content-type", "").split(";")[0].strip().lower()
    if media != "application/json":
        return 415, {"detail": "Content-Type must be application/json"}
    try:
        return 200, json.loads(body)
    except json.JSONDecodeError:
        return 400, {"detail": "Invalid JSON"}


def _err(field, msg):
    return {"loc": ["body", field], "msg": msg}


def validate_item(data):
    if not isinstance(data, dict):
        return None, [{"loc": ["body"], "msg": "must be an object"}]
    errors = []
    name = data.get("name")
    if "name" not in data:
        errors.append(_err("name", "field required"))
    elif not isinstance(name, str) or not name.strip():
        errors.append(_err("name", "must be a non-empty string"))
    price = data.get("price")
    if "price" not in data:
        errors.append(_err("price", "field required"))
    elif not isinstance(price, (int, float)) or isinstance(price, bool):
        errors.append(_err("price", "must be a number"))
    elif price < 0:
        errors.append(_err("price", "must be >= 0"))
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        errors.append(_err("tags", "must be a list of strings"))
    for extra in sorted(set(data) - FIELDS):
        errors.append(_err(extra, "extra field not allowed"))
    if errors:
        return None, errors
    return {"name": name.strip(), "price": price, "tags": list(tags)}, []


def json_response(status, payload):
    return status, {"content-type": "application/json"}, json.dumps(payload, separators=(",", ":"))
''',
"explanation": r'''
The three checks run from the cheapest and most general (media type) to the most specific (field
rules), each with its own status code. Validation collects every error with a location instead of
stopping at the first, rejects booleans explicitly, and returns a cleaned copy rather than the
caller's dict.
''',
"tests": r'''
import json

JSON = {"content-type": "application/json"}


class TestJsonBodies(unittest.TestCase):
    def test_read_ok_with_charset(self):
        self.assertEqual(S.read_json({"content-type": "Application/JSON; charset=utf-8"}, '{"a": 1}'), (200, {"a": 1}))

    def test_read_415(self):
        self.assertEqual(S.read_json({"content-type": "text/plain"}, "{}")[0], 415)
        self.assertEqual(S.read_json({}, "{}")[0], 415)

    def test_read_400(self):
        self.assertEqual(S.read_json(JSON, "{'a': 1}"), (400, {"detail": "Invalid JSON"}))

    def test_valid_item(self):
        self.assertEqual(S.validate_item({"name": " pen ", "price": 2}), ({"name": "pen", "price": 2, "tags": []}, []))
        item, errs = S.validate_item({"name": "ink", "price": 0.5, "tags": ["blue"]})
        self.assertEqual((item["tags"], errs), (["blue"], []))

    def test_all_errors_reported(self):
        item, errs = S.validate_item({"name": "  ", "price": -1, "tags": ["ok", 3], "zeta": 1, "alpha": 2})
        self.assertIsNone(item)
        self.assertEqual(errs, [
            {"loc": ["body", "name"], "msg": "must be a non-empty string"},
            {"loc": ["body", "price"], "msg": "must be >= 0"},
            {"loc": ["body", "tags"], "msg": "must be a list of strings"},
            {"loc": ["body", "alpha"], "msg": "extra field not allowed"},
            {"loc": ["body", "zeta"], "msg": "extra field not allowed"}])

    def test_required_and_bool(self):
        self.assertEqual(S.validate_item({})[1], [{"loc": ["body", "name"], "msg": "field required"},
                                                  {"loc": ["body", "price"], "msg": "field required"}])
        self.assertEqual(S.validate_item({"name": "x", "price": True})[1], [{"loc": ["body", "price"], "msg": "must be a number"}])
        self.assertEqual(S.validate_item([1, 2]), (None, [{"loc": ["body"], "msg": "must be an object"}]))

    def test_json_response(self):
        status, headers, text = S.json_response(201, {"id": 1, "tags": ["a"]})
        self.assertEqual((status, headers, text), (201, {"content-type": "application/json"}, '{"id":1,"tags":["a"]}'))
        self.assertEqual(json.loads(text), {"id": 1, "tags": ["a"]})
''',
"feedback": [
    ("test_read_ok_with_charset", "Compare only the media type before ';', lowercased and stripped."),
    ("test_read_415", "A missing or non-JSON Content-Type gives 415."),
    ("test_read_400", "Catch `json.JSONDecodeError` and return 400."),
    ("test_all_errors_reported", "Collect every error in the order name, price, tags, then sorted extra fields."),
    ("test_required_and_bool", "Report missing fields as 'field required' and reject booleans as numbers."),
    ("test_json_response", "Use `separators=(\",\", \":\")` for compact JSON."),
],
},
# ---------------------------------------------------------------- manual-router
{
"slug": "manual-router", "title": "A Router by Hand",
"difficulty": "intermediate", "prereqs": ["json-bodies"], "packages": [],
"objectives": ["Match request paths against patterns with path parameters",
               "Convert typed parameters such as {item_id:int}",
               "Return 404, 405 (with Allow) and 422 at the right times",
               "Register handlers with a decorator"],
"tags": ["routing", "path-parameters", "decorators", "http-status"],
"sources": ["S071", "S067"], "entry": "class Router; Router.route(method, pattern); Router.dispatch(method, path, query=None)",
"article": r'''
# A Router by Hand

## Intuition
A web framework's first job is **routing**: given `GET /items/42`, find the function that
handles it and call it with `item_id=42`. Writing a small router yourself shows what
`@app.get("/items/{item_id}")` does in FastAPI ([[fastapi-routes]]).

## Precise explanation
* A **pattern** is a path split into segments; `{name}` captures a segment as a string and
  `{name:int}` converts it to an int: `"/items/{item_id:int}"`.
* A path **matches** a pattern when both have the same number of segments and every literal
  segment is equal.
* Dispatch rules (in this order):
  1. No pattern matches the path → **404 Not Found**.
  2. Patterns match, but none for this method → **405 Method Not Allowed**, with an `allow`
     header listing the allowed methods (sorted, comma-separated).
  3. A parameter fails conversion (e.g. `abc` for `:int`) → **422** with an error located at
     `["path", "item_id"]` (FastAPI's behaviour).
  4. Otherwise call the handler with the converted path parameters as keyword arguments, plus
     `query=` the query dict. A handler returns a dict (status 200) or a `(status, dict)` tuple.
* Routes are tried in **registration order**; the first match wins, so register `/users/me`
  before `/users/{name}`.
* **Decorator registration** ([[functions-as-values]]): `@router.route("GET", "/items")` stores
  the function and returns it unchanged.

## Worked example
```python
router = Router()
@router.route("GET", "/items/{item_id:int}")
def get_item(item_id, query):
    return {"item_id": item_id}
router.dispatch("GET", "/items/42")     # (200, {}, {"item_id": 42})
router.dispatch("DELETE", "/items/42")  # (405, {"allow": "GET"}, {"detail": "Method Not Allowed"})
router.dispatch("GET", "/items/abc")    # (422, {}, {"detail": [{"loc": ["path", "item_id"], ...}]})
```

## Common mistakes
* Returning 404 when the path exists but the method does not (that is 405).
* Matching `/items/42/extra` against `/items/{id}` because of a prefix check.
* Converting parameters before knowing the method is allowed.

## Why this matters
FastAPI performs exactly these steps, plus validation of query parameters and bodies, before your
function runs.
''',
"statement": r'''
Write `class Router` with:

* `add(method, pattern, handler)` and the decorator `route(method, pattern)`.
* `dispatch(method, path, query=None)` → `(status, headers, body)` following the four rules
  above. `query` defaults to `{}`; trailing slashes are not special (`/items/` has an empty last
  segment). Bodies: 404 → `{"detail": "Not Found"}`; 405 → `{"detail": "Method Not Allowed"}`
  with headers `{"allow": "GET, POST"}`; 422 → `{"detail": [{"loc": ["path", name], "msg":
  "value is not a valid integer"}]}`. Successful calls return headers `{}`.

Only `str` (default) and `int` converters are needed. Method names are compared in upper case.
''',
"starter": r'''
class Router:
    def __init__(self):
        self.routes = []   # (method, pattern segments, handler)

    def add(self, method, pattern, handler):
        self.routes.append((method.upper(), pattern.strip("/").split("/"), handler))

    def route(self, method, pattern):
        # TODO: decorator
        def register(func):
            return func
        return register

    def dispatch(self, method, path, query=None):
        # TODO: 404, 405, 422, call handler
        return 404, {}, {"detail": "Not Found"}
''',
"hints": [
    "Write `_match(segments, parts)` returning a dict of raw params or None: lengths equal, literal segments equal, `{...}` segments captured.",
    "First collect every route whose pattern matches the path; none → 404; none with this method → 405 with `\", \".join(sorted(methods))`.",
    "For `{name:int}`, `int(raw)` inside try/except ValueError → 422; the handler result is a dict or a `(status, dict)` tuple.",
],
"solution": r'''
class Router:
    def __init__(self):
        self.routes = []   # (method, pattern segments, handler)

    def add(self, method, pattern, handler):
        self.routes.append((method.upper(), pattern.strip("/").split("/"), handler))

    def route(self, method, pattern):
        def register(func):
            self.add(method, pattern, func)
            return func
        return register

    @staticmethod
    def _match(segments, parts):
        if len(segments) != len(parts):
            return None
        params = {}
        for seg, part in zip(segments, parts):
            if seg.startswith("{") and seg.endswith("}"):
                name, _, conv = seg[1:-1].partition(":")
                params[name] = (conv or "str", part)
            elif seg != part:
                return None
        return params

    def dispatch(self, method, path, query=None):
        parts = path.strip("/").split("/")
        matches = [(m, h, p) for m, segs, h in self.routes
                   if (p := self._match(segs, parts)) is not None]
        if not matches:
            return 404, {}, {"detail": "Not Found"}
        method = method.upper()
        chosen = [(h, p) for m, h, p in matches if m == method]
        if not chosen:
            allow = ", ".join(sorted({m for m, _, _ in matches}))
            return 405, {"allow": allow}, {"detail": "Method Not Allowed"}
        handler, raw = chosen[0]
        kwargs = {}
        for name, (conv, value) in raw.items():
            if conv == "int":
                try:
                    value = int(value)
                except ValueError:
                    return 422, {}, {"detail": [{"loc": ["path", name], "msg": "value is not a valid integer"}]}
            kwargs[name] = value
        result = handler(query=query or {}, **kwargs)
        if isinstance(result, tuple):
            status, body = result
            return status, {}, body
        return 200, {}, result
''',
"explanation": r'''
Matching compares segment by segment, so prefixes never match. Collecting all path matches first
makes the 404/405 decision correct and lets the 405 response list every allowed method. Only the
chosen route's parameters are converted, so a type error yields 422 instead of a crash, and the
handler receives typed keyword arguments plus the query dict.
''',
"tests": r'''
def make_router():
    r = S.Router()

    @r.route("GET", "/items/{item_id:int}")
    def get_item(item_id, query):
        return {"item_id": item_id, "q": query.get("q")}

    @r.route("delete", "/items/{item_id:int}")
    def delete_item(item_id, query):
        return 204, {}

    @r.route("GET", "/users/me")
    def me(query):
        return {"user": "current"}

    @r.route("GET", "/users/{name}")
    def user(name, query):
        return {"user": name}

    r.add("POST", "/items", lambda query: (201, {"created": True}))
    return r


class TestRouter(unittest.TestCase):
    def test_typed_param_and_query(self):
        self.assertEqual(make_router().dispatch("GET", "/items/42", {"q": "x"}), (200, {}, {"item_id": 42, "q": "x"}))

    def test_status_tuple(self):
        self.assertEqual(make_router().dispatch("POST", "/items"), (201, {}, {"created": True}))
        self.assertEqual(make_router().dispatch("DELETE", "/items/1"), (204, {}, {}))

    def test_404(self):
        r = make_router()
        for path in ("/nothing", "/items/1/extra", "/"):
            self.assertEqual(r.dispatch("GET", path), (404, {}, {"detail": "Not Found"}))

    def test_405_allow(self):
        self.assertEqual(make_router().dispatch("PUT", "/items/3"),
                         (405, {"allow": "DELETE, GET"}, {"detail": "Method Not Allowed"}))
        self.assertEqual(make_router().dispatch("GET", "/items")[1], {"allow": "POST"})

    def test_422(self):
        self.assertEqual(make_router().dispatch("GET", "/items/abc"),
                         (422, {}, {"detail": [{"loc": ["path", "item_id"], "msg": "value is not a valid integer"}]}))

    def test_order_and_str_param(self):
        r = make_router()
        self.assertEqual(r.dispatch("GET", "/users/me")[2], {"user": "current"})
        self.assertEqual(r.dispatch("get", "/users/ada")[2], {"user": "ada"})

    def test_decorator_returns_function(self):
        r = S.Router()

        @r.route("GET", "/ping")
        def ping(query):
            return {"pong": True}
        self.assertEqual(ping(query={}), {"pong": True})
        self.assertEqual(len(r.routes), 1)
''',
"feedback": [
    ("test_typed_param_and_query", "Convert `{item_id:int}` with int() and pass `query=` to the handler."),
    ("test_404", "A path matches only when it has the same number of segments and equal literals."),
    ("test_405_allow", "If the path matches but the method does not, return 405 with the sorted allowed methods."),
    ("test_422", "Catch the int() conversion error and return 422 with loc ['path', name]."),
    ("test_order_and_str_param", "Try routes in registration order and compare methods in upper case."),
    ("test_decorator_returns_function", "The decorator must register the function and return it unchanged."),
],
},
# ---------------------------------------------------------------- asyncio-basics
{
"slug": "asyncio-basics", "title": "async and await with asyncio",
"difficulty": "intermediate", "prereqs": ["manual-router"], "packages": [],
"objectives": ["Define coroutines with async def and run them with asyncio.run",
               "Run coroutines concurrently with asyncio.gather and see how await yields control",
               "Limit concurrency with a Semaphore", "Stop slow work with asyncio.wait_for"],
"tags": ["asyncio", "async-await", "concurrency", "timeouts", "semaphore"],
"sources": ["S061", "S077"], "entry": "run_in_order(log); run_together(log); gather_in_order(values); limited(factories, limit); with_timeout(coro, seconds)",
"article": r'''
# async and await with asyncio

## Intuition
A web server spends most of its time **waiting** — for a database, another API, a file. While one
request waits, the server could work on another. `async`/`await` lets one thread juggle many
waiting tasks: at every `await`, a task says "I am waiting; run someone else", and the
**event loop** switches to another ready task.

## Precise explanation
```python
import asyncio

async def worker(name, log):        # a coroutine function
    log.append(f"{name} start")
    await asyncio.sleep(0)           # yield control to the event loop
    log.append(f"{name} end")
    return name.upper()

asyncio.run(worker("a", []))         # run a coroutine from normal code
```
* Calling `worker(...)` does **not** run it; it creates a coroutine object. It runs when awaited
  or scheduled.
* `await a(); await b()` runs them **one after the other**.
* `await asyncio.gather(a(), b())` runs them **concurrently** and returns results in argument
  order, regardless of which finished first. With the `worker` above the log becomes
  `a start, b start, a end, b end` — each `await` let the other task proceed.
* `asyncio.Semaphore(n)` limits how many tasks enter a block at once:
  `async with sem: ...`.
* `await asyncio.wait_for(coro, timeout)` raises `TimeoutError` (`asyncio.TimeoutError`, the same
  class since Python 3.11) if it takes too long and cancels the work.
* **Blocking** calls such as `time.sleep` freeze the whole loop; use `await asyncio.sleep` and
  async libraries inside coroutines.

## Worked example
Three downloads of 1 s each: sequential awaits take about 3 s; `gather` takes about 1 s, because
the waits overlap. (Tests in this site avoid real time and check the order of events instead.)

## Common mistakes
* Forgetting `await`, so the coroutine never runs (Python warns "coroutine was never awaited").
* Calling `asyncio.run` inside code that is already running in an event loop.
* Expecting `async` to speed up CPU-heavy work — it only overlaps *waiting*.

## Why this matters
FastAPI runs `async def` endpoints on an event loop ([[fastapi-async]]), and ASGI applications
([[asgi-app]]) are coroutines.
''',
"statement": r'''
The starter defines `step(name, log)`: it appends `f"{name}1"`, awaits `asyncio.sleep(0)`, appends
`f"{name}2"` and returns `name`. Implement (each returns normally — call `asyncio.run` inside):

1. `run_in_order(log)` → run `step("a", log)` then `step("b", log)` sequentially; return
   `["a", "b"]`. The log becomes `["a1", "a2", "b1", "b2"]`.
2. `run_together(log)` → run both with `asyncio.gather`; return the results. The log becomes
   `["a1", "b1", "a2", "b2"]`.
3. `gather_in_order(values)` → each value `v` is handled by a coroutine that awaits
   `asyncio.sleep(0)` **v times** and then returns `v * 10`; run them all concurrently and return
   the list of results in the input order (values are non-negative ints).
4. `limited(factories, limit)` → `factories` are zero-argument functions returning coroutines;
   run all of them concurrently but with at most `limit` running at once (`asyncio.Semaphore`);
   return their results in order.
5. `with_timeout(coro, seconds)` → `("ok", result)` or `("timeout", None)`.
''',
"starter": r'''
import asyncio


async def step(name, log):
    log.append(f"{name}1")
    await asyncio.sleep(0)
    log.append(f"{name}2")
    return name


def run_in_order(log):
    async def main():
        a = await step("a", log)
        b = await step("b", log)
        return [a, b]
    return asyncio.run(main())


def run_together(log):
    # TODO: asyncio.gather
    return run_in_order(log)


def gather_in_order(values):
    # TODO
    return []


def limited(factories, limit):
    # TODO: Semaphore
    return []


def with_timeout(coro, seconds):
    # TODO: asyncio.wait_for
    return ("ok", None)
''',
"hints": [
    "`async def main(): return list(await asyncio.gather(step(\"a\", log), step(\"b\", log)))`.",
    "Inside `gather_in_order`, define `async def handle(v): for _ in range(v): await asyncio.sleep(0)` then `return v * 10`.",
    "In `limited`, create the semaphore inside the async main; wrap each call as `async with sem: return await f()`. For the timeout, catch `asyncio.TimeoutError`.",
],
"solution": r'''
import asyncio


async def step(name, log):
    log.append(f"{name}1")
    await asyncio.sleep(0)
    log.append(f"{name}2")
    return name


def run_in_order(log):
    async def main():
        a = await step("a", log)
        b = await step("b", log)
        return [a, b]
    return asyncio.run(main())


def run_together(log):
    async def main():
        return list(await asyncio.gather(step("a", log), step("b", log)))
    return asyncio.run(main())


def gather_in_order(values):
    async def handle(v):
        for _ in range(v):
            await asyncio.sleep(0)
        return v * 10

    async def main():
        return list(await asyncio.gather(*(handle(v) for v in values)))
    return asyncio.run(main())


def limited(factories, limit):
    async def main():
        sem = asyncio.Semaphore(limit)

        async def guarded(f):
            async with sem:
                return await f()
        return list(await asyncio.gather(*(guarded(f) for f in factories)))
    return asyncio.run(main())


def with_timeout(coro, seconds):
    async def main():
        try:
            return ("ok", await asyncio.wait_for(coro, seconds))
        except asyncio.TimeoutError:
            return ("timeout", None)
    return asyncio.run(main())
''',
"explanation": r'''
Sequential awaits finish one coroutine before starting the next, while `gather` schedules both so
each `await asyncio.sleep(0)` hands control to the other — visible in the log order. `gather`
always returns results in argument order. The semaphore is created inside the running loop and
caps how many guarded coroutines are active, and `wait_for` turns a slow coroutine into a
`TimeoutError` that is reported as a value.
''',
"tests": r'''
import asyncio


class TestAsyncio(unittest.TestCase):
    def test_sequential(self):
        log = []
        self.assertEqual(S.run_in_order(log), ["a", "b"])
        self.assertEqual(log, ["a1", "a2", "b1", "b2"])

    def test_concurrent(self):
        log = []
        self.assertEqual(S.run_together(log), ["a", "b"])
        self.assertEqual(log, ["a1", "b1", "a2", "b2"])

    def test_gather_keeps_input_order(self):
        self.assertEqual(S.gather_in_order([3, 0, 2, 1]), [30, 0, 20, 10])
        self.assertEqual(S.gather_in_order([]), [])

    def test_limited(self):
        state = {"active": 0, "peak": 0}

        def make(i):
            async def job():
                state["active"] += 1
                state["peak"] = max(state["peak"], state["active"])
                await asyncio.sleep(0)
                await asyncio.sleep(0)
                state["active"] -= 1
                return i * i
            return job
        self.assertEqual(S.limited([make(i) for i in range(6)], 2), [0, 1, 4, 9, 16, 25])
        self.assertEqual(state["peak"], 2)

    def test_limited_unbounded(self):
        state = {"active": 0, "peak": 0}

        def make():
            async def job():
                state["active"] += 1
                state["peak"] = max(state["peak"], state["active"])
                await asyncio.sleep(0)
                state["active"] -= 1
                return True
            return job
        S.limited([make() for _ in range(5)], 10)
        self.assertEqual(state["peak"], 5)

    def test_timeout(self):
        async def never():
            await asyncio.Event().wait()

        async def quick():
            return 42
        self.assertEqual(S.with_timeout(never(), 0.01), ("timeout", None))
        self.assertEqual(S.with_timeout(quick(), 1.0), ("ok", 42))
''',
"feedback": [
    ("test_concurrent", "Use `asyncio.gather` so both coroutines start before either finishes."),
    ("test_gather_keeps_input_order", "gather returns results in the order the coroutines were passed."),
    ("test_limited", "Guard each call with `async with sem:` where `sem = asyncio.Semaphore(limit)`."),
    ("test_limited_unbounded", "Start all guarded coroutines together with gather; don't await them one by one."),
    ("test_timeout", "Wrap the coroutine in `asyncio.wait_for` and catch `asyncio.TimeoutError`."),
],
},
# ---------------------------------------------------------------- asgi-app
{
"slug": "asgi-app", "title": "A Minimal ASGI Application",
"difficulty": "intermediate", "prereqs": ["asyncio-basics"], "packages": [],
"objectives": ["Describe the ASGI interface: scope, receive and send",
               "Write an async application that sends a start message and a body message",
               "Read a request body from receive() events",
               "Call an ASGI app in-process, as a test client does"],
"tags": ["asgi", "async", "http", "test-client", "frameworks"],
"sources": ["S069", "S061", "S077"], "entry": "async app(scope, receive, send); call_asgi(app, method, path, query_string=b'', body=b'', headers=None)",
"article": r'''
# A Minimal ASGI Application

## Intuition
FastAPI is built on **ASGI** (Asynchronous Server Gateway Interface): a tiny contract between a
server (such as Uvicorn) and an application. The server turns network bytes into a dict and two
async functions; the app answers by calling one of them. Writing an ASGI app by hand — and a small
in-process caller like FastAPI's test client — removes the last bit of magic.

## Precise explanation
An ASGI application is `async def app(scope, receive, send)`.
* `scope` (dict) describes the request: `scope["type"] == "http"`, `"method"`, `"path"`,
  `"query_string"` (bytes, without `?`), `"headers"` (list of `(name, value)` byte pairs with
  lower-case names).
* `await receive()` returns events `{"type": "http.request", "body": b"...", "more_body":
  bool}`; keep reading while `more_body` is true and join the chunks.
* `await send(event)` sends the response in two kinds of event:
  1. `{"type": "http.response.start", "status": 200, "headers": [(b"content-type",
     b"application/json")]}`
  2. `{"type": "http.response.body", "body": b"..."}`
* **Calling an app in tests**: build the scope, give it a `receive` that returns the body, and a
  `send` that records events; run with `asyncio.run`. No network, no server. FastAPI's
  `TestClient` does this (through HTTPX) for you.

## Worked example
For `GET /`, the app below sends start(200, JSON) then body `b'{"message":"hello"}'`;
`call_asgi(app, "GET", "/")` returns `(200, {"content-type": "application/json"},
b'{"message":"hello"}')`.

## Common mistakes
* Sending the body before the start event, or sending two start events.
* Reading only the first `receive()` chunk when `more_body` is true.
* Treating headers as a dict of strings — in ASGI they are lists of byte pairs.

## Why this matters
Every FastAPI app *is* an ASGI app (`app(scope, receive, send)`), which is why the same test
client technique works in [[fastapi-routes]].
''',
"statement": r'''
Implement:

1. `async def app(scope, receive, send)` handling `scope["type"] == "http"`:
   * `GET /` → 200 `{"message": "hello"}`;
   * `GET /echo` → 200 `{"params": <dict of first values from the query string, decoded with
     urllib.parse.parse_qs>}` — you may use `urllib.parse.parse_qs` here;
   * `POST /sum` → read the whole body (all chunks), parse JSON `{"numbers": [...]}` and return
     200 `{"sum": total}`; invalid JSON or a missing/non-list `numbers` → 400 `{"detail": "bad
     body"}`;
   * known path, wrong method → 405 `{"detail": "Method Not Allowed"}`; unknown path → 404
     `{"detail": "Not Found"}`.
   Every response uses `content-type: application/json` and compact JSON
   (`separators=(",", ":")`), sent as one start and one body event.
2. `call_asgi(app, method, path, query_string=b"", body=b"", headers=None)` → `(status, headers
   dict with str names/values, body bytes)` by running the app with `asyncio.run`. `receive`
   returns the whole body in one event (`more_body` false).
''',
"starter": r'''
import asyncio
import json
from urllib.parse import parse_qs


async def send_json(send, status, payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": body})


async def app(scope, receive, send):
    # TODO: route on scope["method"] and scope["path"]
    await send_json(send, 200, {"message": "hello"})


def call_asgi(app, method, path, query_string=b"", body=b"", headers=None):
    # TODO: build scope, receive and send; run with asyncio.run
    return 0, {}, b""
''',
"hints": [
    "Read the body with a loop: `chunks = []; more = True; while more: event = await receive(); chunks.append(event.get(\"body\", b\"\")); more = event.get(\"more_body\", False)`.",
    "Keep a dict of path → allowed methods to decide between 404 and 405.",
    "In `call_asgi`, define `async def receive(): return {\"type\": \"http.request\", \"body\": body, \"more_body\": False}` and a `send` that appends events to a list.",
],
"solution": r'''
import asyncio
import json
from urllib.parse import parse_qs

ROUTES = {"/": "GET", "/echo": "GET", "/sum": "POST"}


async def send_json(send, status, payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    await send({"type": "http.response.start", "status": status,
                "headers": [(b"content-type", b"application/json")]})
    await send({"type": "http.response.body", "body": body})


async def read_body(receive):
    chunks, more = [], True
    while more:
        event = await receive()
        chunks.append(event.get("body", b""))
        more = event.get("more_body", False)
    return b"".join(chunks)


async def app(scope, receive, send):
    path, method = scope["path"], scope["method"]
    if path not in ROUTES:
        return await send_json(send, 404, {"detail": "Not Found"})
    if method != ROUTES[path]:
        return await send_json(send, 405, {"detail": "Method Not Allowed"})
    if path == "/":
        return await send_json(send, 200, {"message": "hello"})
    if path == "/echo":
        params = parse_qs(scope.get("query_string", b"").decode())
        return await send_json(send, 200, {"params": {k: v[0] for k, v in params.items()}})
    try:
        data = json.loads(await read_body(receive))
        numbers = data["numbers"]
        if not isinstance(numbers, list):
            raise ValueError
        total = sum(numbers)
    except (ValueError, KeyError, TypeError):
        return await send_json(send, 400, {"detail": "bad body"})
    await send_json(send, 200, {"sum": total})


def call_asgi(app, method, path, query_string=b"", body=b"", headers=None):
    scope = {"type": "http", "method": method, "path": path, "query_string": query_string,
             "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]}
    events = []

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(event):
        events.append(event)

    asyncio.run(app(scope, receive, send))
    start = next(e for e in events if e["type"] == "http.response.start")
    body_out = b"".join(e.get("body", b"") for e in events if e["type"] == "http.response.body")
    hdrs = {k.decode(): v.decode() for k, v in start["headers"]}
    return start["status"], hdrs, body_out
''',
"explanation": r'''
The app inspects the scope, decides between 404, 405 and a handler, and always replies with one
start and one body event through a shared helper. The body reader honours `more_body`, so chunked
uploads work. `call_asgi` is a miniature test client: it fabricates the scope and `receive`,
records everything passed to `send`, and converts the recorded events back into a status,
headers and body.
''',
"tests": r'''
import asyncio
import json


def run_raw(scope, chunks):
    """Independent harness: feeds the body in several chunks and records events."""
    events, queue = [], list(chunks)

    async def receive():
        body = queue.pop(0) if queue else b""
        return {"type": "http.request", "body": body, "more_body": bool(queue)}

    async def send(event):
        events.append(event)
    asyncio.run(S.app(scope, receive, send))
    return events


def scope(method, path, qs=b""):
    return {"type": "http", "method": method, "path": path, "query_string": qs, "headers": []}


class TestAsgi(unittest.TestCase):
    def test_root_events(self):
        events = run_raw(scope("GET", "/"), [b""])
        self.assertEqual([e["type"] for e in events], ["http.response.start", "http.response.body"])
        self.assertEqual(events[0]["status"], 200)
        self.assertIn((b"content-type", b"application/json"), events[0]["headers"])
        self.assertEqual(events[1]["body"], b'{"message":"hello"}')

    def test_echo_query(self):
        events = run_raw(scope("GET", "/echo", b"name=ada&n=3"), [b""])
        self.assertEqual(json.loads(events[1]["body"]), {"params": {"name": "ada", "n": "3"}})

    def test_sum_chunked(self):
        events = run_raw(scope("POST", "/sum"), [b'{"numbers": [1,', b' 2, 3.5]}'])
        self.assertEqual((events[0]["status"], json.loads(events[1]["body"])), (200, {"sum": 6.5}))

    def test_errors(self):
        self.assertEqual(run_raw(scope("GET", "/nope"), [b""])[0]["status"], 404)
        self.assertEqual(run_raw(scope("GET", "/sum"), [b""])[0]["status"], 405)
        for body in (b"not json", b'{"nums": []}', b'{"numbers": 5}', b'{"numbers": ["a", 1]}'):
            events = run_raw(scope("POST", "/sum"), [body])
            self.assertEqual((events[0]["status"], events[1]["body"]), (400, b'{"detail":"bad body"}'), body)

    def test_call_asgi_client(self):
        self.assertEqual(S.call_asgi(S.app, "GET", "/"), (200, {"content-type": "application/json"}, b'{"message":"hello"}'))
        status, _, body = S.call_asgi(S.app, "POST", "/sum", body=b'{"numbers": [2, 2]}')
        self.assertEqual((status, body), (200, b'{"sum":4}'))

    def test_call_asgi_with_other_app(self):
        async def teapot(scope, receive, send):
            await send({"type": "http.response.start", "status": 418, "headers": [(b"x-kind", b"tea")]})
            await send({"type": "http.response.body", "body": b"short and "})
            await send({"type": "http.response.body", "body": b"stout"})
        self.assertEqual(S.call_asgi(teapot, "GET", "/"), (418, {"x-kind": "tea"}, b"short and stout"))
''',
"feedback": [
    ("test_root_events", "Send exactly one start event (status + headers) and then one body event."),
    ("test_sum_chunked", "Keep calling `receive()` while `more_body` is true and join the chunks."),
    ("test_errors", "Unknown path → 404; known path with the wrong method → 405; bad bodies → 400."),
    ("test_call_asgi_client", "Build the scope, run the app with asyncio.run, and decode the recorded events."),
    ("test_call_asgi_with_other_app", "Join every body event, and decode header byte pairs into strings."),
],
},
]
