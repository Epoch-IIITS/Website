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
