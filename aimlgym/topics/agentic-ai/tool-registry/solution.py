r"""Reference solution for AG-01 Tool Registry and Dispatch.

Dispatch validates in a fixed order — tool exists, required args present, no extras, correct types —
and only then runs the tool inside a try/except so that any failure is reported as a structured error
the model can read. Floats accept ints; bools are rejected for numeric types.
"""
class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, fn, schema, description=""):
        if name in self._tools:
            raise ValueError(f"tool '{name}' already registered")
        self._tools[name] = (fn, dict(schema), description)

    @staticmethod
    def _type_ok(value, typ):
        if typ in (int, float) and isinstance(value, bool):
            return False
        if typ is float:
            return isinstance(value, (int, float))
        return isinstance(value, typ)

    def dispatch(self, call):
        name = call.get("tool")
        args = call.get("args", {}) or {}
        if name not in self._tools:
            return {"ok": False, "error": f"unknown tool '{name}'"}
        fn, schema, _ = self._tools[name]
        for a in sorted(set(schema) - set(args)):
            return {"ok": False, "error": f"missing argument '{a}'"}
        for a in sorted(set(args) - set(schema)):
            return {"ok": False, "error": f"unexpected argument '{a}'"}
        for a in sorted(schema):
            if not self._type_ok(args[a], schema[a]):
                return {"ok": False, "error": f"argument '{a}' must be {schema[a].__name__}"}
        try:
            return {"ok": True, "result": fn(**args)}
        except Exception as e:  # tool failures become data for the agent
            return {"ok": False, "error": f"tool error: {type(e).__name__}: {e}"}

    def describe(self):
        return [{"name": n, "description": d, "args": {a: t.__name__ for a, t in s.items()}}
                for n, (_, s, d) in sorted(self._tools.items())]
