// Started when a problem page opens: it loads Pyodide and the pack's packages in the background,
// then stays alive across Runs. Each Run executes in a fresh namespace.
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.mjs"
// Pyodide ships OpenCV as opencv-python; the executor image uses the headless wheel.
const PYODIDE_PACKAGE = { "opencv-python-headless": "opencv-python" }

const runVisibleTests = String.raw`
import contextlib, io, json, re, sys, textwrap, types, unittest
payload = json.loads(payload_json)
tests = payload["tests"]
code = payload["code"]
total = len(tests)

class LimitedOutput(io.StringIO):
    def write(self, text):
        if self.tell() < 4000:
            super().write(text[:4000 - self.tell()])
        return len(text)

captured = LimitedOutput()
try:
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        def run_program(stdin_text=""):
            """Run a whole-program (script) step from the top with stdin_text as its input."""
            module = types.ModuleType("solution")
            saved_stdin = sys.stdin
            sys.stdin = io.StringIO(stdin_text)
            buffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(buffer):
                    exec(compile(code, "starter.py", "exec"), module.__dict__)
            finally:
                sys.stdin = saved_stdin
            return buffer.getvalue(), module

        S = types.ModuleType("solution")
        if payload.get("kind") != "script":
            exec(compile(code, "starter.py", "exec"), S.__dict__)
        namespace = {"__name__": "tests", "S": S, "unittest": unittest, "run_program": run_program}
        import math, random, statistics, warnings, json, copy, io, os, sys, importlib, contextlib
        namespace.update({"math": math, "random": random, "statistics": statistics, "warnings": warnings, "json": json, "copy": copy, "io": io, "os": os, "sys": sys, "importlib": importlib, "contextlib": contextlib})
        if "numpy" in payload["packages"]:
            import numpy as np
            namespace["np"] = np
        if "pandas" in payload["packages"]:
            import pandas as pd
            namespace["pd"] = pd
        if payload.get("prelude"):
            exec(compile(payload["prelude"], "tests.py", "exec"), namespace)
        # One class per original TestCase, rebuilt with its setUp and helper methods.
        helpers = payload.get("classes") or []
        groups = {}
        for index, test in enumerate(tests):
            if not re.fullmatch(r"test_[A-Za-z0-9_]+", test["name"]):
                raise ValueError("Invalid visible test name")
            groups.setdefault(int(test.get("group", 0)), []).append((index, test))
        source = ""
        for group, items in groups.items():
            source += "class VisibleTests%d(unittest.TestCase):\n" % group
            if group < len(helpers) and helpers[group]:
                source += textwrap.indent(helpers[group], "    ") + "\n"
            for index, test in items:
                source += "    def test_case_%d(self):\n" % index
                source += textwrap.indent(test["code"] or "pass", "        ") + "\n"
        exec(source, namespace)
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(namespace["VisibleTests%d" % group]) for group in groups)
        result = unittest.TestResult()
        suite.run(result)
        failures = {case._testMethodName: detail[-800:] for case, detail in result.failures + result.errors}
        cases = [{"name": test["name"], "passed": "test_case_%d" % index not in failures, "message": failures.get("test_case_%d" % index)} for index, test in enumerate(tests)]
        passed = sum(case["passed"] for case in cases)
        response = {"passed": passed, "total": total, "status": "passed" if passed == total else "failed", "tests": cases, "output": captured.getvalue()[:4000]}
except Exception as error:
    response = {"passed": 0, "total": total, "status": "failed", "tests": [], "output": (type(error).__name__ + ": " + str(error))[:4000]}
json.dumps(response)
`

let ready = null

function prepare(packages) {
  ready ??= (async () => {
    const { loadPyodide } = await import(PYODIDE_URL)
    const pyodide = await loadPyodide()
    const names = [...new Set(packages.map((name) => PYODIDE_PACKAGE[name] ?? name))]
    if (names.length) await pyodide.loadPackage(names)
    return pyodide
  })()
  return ready
}

self.onmessage = async ({ data }) => {
  try {
    const pyodide = await prepare(data.packages)
    if (data.type === "prepare") {
      self.postMessage({ type: "ready" })
      return
    }
    // A fresh globals dict per Run, so names from earlier attempts never leak into this one.
    const globals = pyodide.toPy({ payload_json: JSON.stringify(data) })
    try {
      const result = JSON.parse(await pyodide.runPythonAsync(runVisibleTests, { globals }))
      self.postMessage({ type: "result", id: data.id, result })
    } finally {
      globals.destroy()
    }
  } catch (error) {
    ready = null
    self.postMessage({ type: data.type === "prepare" ? "ready" : "result", id: data.id, unavailable: true, message: String(error).slice(0, 300) })
  }
}
