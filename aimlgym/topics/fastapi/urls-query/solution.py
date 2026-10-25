r"""Reference solution for FA-03 URLs, Paths and Query Strings.

The URL is peeled from the outside in: fragment, query, then the first slash separates the
authority from the path. Percent-decoding works on bytes so multi-byte UTF-8 characters are
rebuilt correctly. Queries become a dict of lists with `setdefault`, and the encoder is the exact
inverse for the characters it escapes.
"""
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
