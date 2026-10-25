r"""Reference solution for PY-10 Greeting Formatter.

The function normalises its input first (strip), handles the empty case by falling back to the
default, and only then formats. Doing validation before formatting keeps each step simple and
means the f-string always receives a clean, non-empty name. `str.title()` is applied inside the
f-string so the stored value stays as the user typed it (minus whitespace).
"""
def greet(name="World"):
    name = name.strip()
    if not name:
        name = "World"
    return f"Hello, {name.title()}!"
