r"""Reference solution for FA-01 Anatomy of an HTTP Request.

The parser splits the message once at the blank line, validates the request line, then reads
headers with `partition(":")` so values containing colons (such as URLs) survive. Lowercased
names make lookups case-insensitive, and the body length is compared in bytes. The builder is the
inverse and adds `Content-Length` only when needed.
"""
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
