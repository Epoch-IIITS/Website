r"""Reference solution for FA-02 HTTP Responses and Status Codes.

Integer division by 100 maps a code to its class. The response builder mirrors the request
builder from the previous step, with the special case that 204 carries neither a body nor body
headers. `split(" ", 2)` splits the status line into exactly three parts so multi-word phrases
stay intact.
"""
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
