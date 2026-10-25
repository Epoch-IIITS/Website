# URLs, Paths and Query Strings

## Learning outcomes

After this lesson you can:

- Split a URL into scheme, host, port, path, query and fragment
- Decode percent-encoding and '+' in query strings
- Represent repeated query parameters as lists
- Compare a manual parser with urllib.parse

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
FastAPI turns `?q=...&limit=...` into typed function arguments (FA-09); knowing the
raw format explains how lists and missing values arrive.

## Library implementation

`urllib.parse` implements all of this: `urlsplit(url)` returns scheme, netloc, path, query and
fragment (`.hostname` and `.port` split the netloc), `unquote_plus` decodes, `parse_qs(qs,
keep_blank_values=True)` returns the same dict of lists, and `urlencode(params, doseq=True)`
builds queries. The tests check your functions agree with them.

## References

- [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — MDN Web Docs (Mozilla) (`S065`)
- [urllib.parse — Parse URLs into components](https://docs.python.org/3/library/urllib.parse.html) — Python Software Foundation (`S063`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
