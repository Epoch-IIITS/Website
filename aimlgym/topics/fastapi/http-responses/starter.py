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
