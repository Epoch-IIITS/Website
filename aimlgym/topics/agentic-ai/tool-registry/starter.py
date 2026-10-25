class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, fn, schema, description=""):
        pass

    def dispatch(self, call):
        pass

    def describe(self):
        return []
