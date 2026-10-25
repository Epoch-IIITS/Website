# FA-03 · URLs, Paths and Query Strings

**Topic:** FastAPI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** FA-02 HTTP Responses and Status Codes

Read the lesson first: [article.md](article.md)

## Task

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

## Hints

<details><summary>Hint 1</summary>

`scheme, sep, rest = url.partition("://")`; then split off `#fragment`, then `?query`, then the first `/` separates host[:port] from the path.

</details>

<details><summary>Hint 2</summary>

Build a `bytearray`: for `%` append `int(text[i+1:i+3], 16)`, for `+` append a space, otherwise `out += ch.encode("utf-8")`; finally `out.decode("utf-8")`.

</details>

<details><summary>Hint 3</summary>

In `build_query`, encode each value with `.encode("utf-8")` and loop over the bytes: `chr(b) in SAFE_CHARS` → literal, `b == 32` → `+`, else `f"%{b:02X}"`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_split_full` | Remove the fragment first, then the query, then split host and port at ':'. |
| `test_split_defaults` | Use port 80/443 when missing and '/' for an empty path; reject other schemes. |
| `test_percent_decode` | Collect raw bytes and decode them together with UTF-8; reject a lone '%'. |
| `test_parse_query` | Skip empty pieces, keep every value of repeated keys in a list, and decode both sides. |
| `test_value_with_equals` | Split each pair at the first '=' only. |
| `test_build_round_trip` | Encode spaces as '+', unsafe bytes as upper-case %XX. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The URL is peeled from the outside in: fragment, query, then the first slash separates the
authority from the path. Percent-decoding works on bytes so multi-byte UTF-8 characters are
rebuilt correctly. Queries become a dict of lists with `setdefault`, and the encoder is the exact
inverse for the characters it escapes.

## References

- [Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — MDN Web Docs (Mozilla) (`S065`)
- [urllib.parse — Parse URLs into components](https://docs.python.org/3/library/urllib.parse.html) — Python Software Foundation (`S063`)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — IETF (Fielding, Nottingham, Reschke) (`S067`)
