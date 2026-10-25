# PY-27 · Writing Unit Tests

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-26 Inheritance, Special Methods and Dataclasses

Read the lesson first: [article.md](article.md)

## Task

The starter contains a correct `slugify(text)`:

* lowercase ASCII letters and digits are kept;
* every run of other characters becomes a single `-`;
* there are no leading or trailing dashes; an input with no letters or digits gives `""`.

Write `class SlugifyTests(unittest.TestCase)` with **at least five** test methods. Every test
must call the function as `self.slugify(...)` (the grader swaps in other versions through that
attribute).

Your tests are graded by running them against:
* the correct `slugify` — all your tests must pass;
* six broken versions (mutants) — for each one, at least one of your tests must fail.

The mutants: (1) does not lowercase, (2) does not collapse runs of separators, (3) does not strip
leading/trailing dashes, (4) treats digits as separators, (5) only replaces spaces (keeps
punctuation), (6) crashes on an empty string.

## Hints

<details><summary>Hint 1</summary>

Each mutant breaks one rule; write one test per rule from the statement.

</details>

<details><summary>Hint 2</summary>

Examples: `"ABC"`→`"abc"`, `"a,  b"`→`"a-b"`, `"--a--"`→`"a"`, `"r2d2"`→`"r2d2"`.

</details>

<details><summary>Hint 3</summary>

Include `self.assertEqual(self.slugify(""), "")` and a punctuation case such as `"a!b"`→`"a-b"`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_at_least_five_tests` | Add more `test_...` methods to `SlugifyTests`. |
| `test_pass_on_correct_version` | One of your expected values is wrong: check it against the rules in the statement. |
| `test_catches_missing_lowercase` | Add a test with upper-case input. |
| `test_catches_missing_collapse` | Add a test with two or more separators in a row, e.g. `"a,  b"`. |
| `test_catches_missing_strip` | Add a test whose input starts or ends with punctuation or spaces. |
| `test_catches_digit_bug` | Add a test containing digits, which must be kept. |
| `test_catches_punctuation_bug` | Add a test with punctuation between letters, such as `"a!b"`. |
| `test_catches_empty_crash` | Add a test for the empty string. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each test targets one rule of the specification, so each mutant — which breaks exactly one
rule — fails at least one test, while the correct implementation passes them all. The empty
and punctuation-only inputs cover the edge cases that crash naive implementations.

## References

- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html) — Python Software Foundation (`S002`)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html) — Python Software Foundation (`S064`)
