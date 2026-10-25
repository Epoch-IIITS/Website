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
