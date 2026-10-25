r"""Reference solution for FA-05 A Router by Hand.

Matching compares segment by segment, so prefixes never match. Collecting all path matches first
makes the 404/405 decision correct and lets the 405 response list every allowed method. Only the
chosen route's parameters are converted, so a type error yields 422 instead of a crash, and the
handler receives typed keyword arguments plus the query dict.
"""
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
