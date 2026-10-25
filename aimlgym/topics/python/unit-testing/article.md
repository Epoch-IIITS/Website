# Writing Unit Tests

## Learning outcomes

After this lesson you can:

- Write unittest.TestCase classes with assertEqual and assertRaises
- Choose test cases that cover normal, edge and error behaviour
- Explain how tests catch bugs, using deliberately broken versions (mutants)
- Know when to replace slow or external dependencies with fakes or mocks

## Intuition
Every exercise so far was checked by tests someone else wrote. A **unit test** is a small
program that calls your code with chosen inputs and checks the outputs. Good tests are like a
safety net: when you change code later, they tell you immediately if you broke something.

## Precise explanation
```python
import unittest

def add(a, b):
    return a + b

class AddTests(unittest.TestCase):
    def test_small_numbers(self):            # methods starting with test_ are tests
        self.assertEqual(add(2, 3), 5)

    def test_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            add(1, "x")
```
Run with `python -m unittest -v`. Useful assertions: `assertEqual`, `assertTrue`, `assertIn`,
`assertIsNone`, `assertAlmostEqual` (floats), `assertRaises`. `setUp(self)` runs before every
test.

**What to test**
* The normal case from the specification.
* **Edge cases**: empty input, one element, boundaries, repeated or unusual characters.
* **Error cases**: inputs that must raise.
* One idea per test, with a descriptive name, so a failure tells you what broke.

**How good are my tests?** Make a deliberately broken copy of the code — a **mutant** (for
example, forget to lowercase). If every test still passes, the tests missed that bug. This
exercise grades your tests exactly this way.

**Fakes and mocks.** Code that calls a web service, a clock or a language model is tested by
replacing that dependency with a predictable stand-in: a small fake function or class, or
`unittest.mock.Mock` / `patch`. Later topics use scripted models (AG-06) and fake
services (FA-13) this way, so tests never need the network.

## Worked example
For `slugify("  Hello, World!  ")` → `"hello-world"`, good tests include:
`"ABC" → "abc"` (case), `"a b" → "a-b"` (spaces), `"a, b" → "a-b"` (punctuation runs collapse),
`"--a--" → "a"` (no leading/trailing dashes), `"" → ""` (empty), `"r2d2" → "r2d2"` (digits kept).

## Common mistakes
* Testing only the example from the statement.
* Asserting on `print` output instead of return values.
* Tests that depend on each other's order or on shared mutable state.
* Asserting floats with `assertEqual` instead of `assertAlmostEqual`.

## Why this matters
Every pack in this curriculum is graded by unit tests, and the FastAPI topic ends with
FA-15, where you test a web API the same way.

## References

- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html) — Python Software Foundation (`S064`)
