"""Python part 1: programs written before functions are introduced.

These packs use kind="script": the learner's file runs top to bottom, and the tests re-run it
with a given standard input (via run_program in the test header) and compare what it prints.
"""

PROBLEMS = [
# ---------------------------------------------------------------- hello-print
{
"slug": "hello-print", "title": "Hello, print()", "kind": "script",
"difficulty": "beginner", "prereqs": [], "packages": [],
"objectives": ["Run a Python program that prints text", "Write string literals with single and double quotes",
               "Control print's separator and line ending with sep and end", "Write comments"],
"tags": ["print", "strings", "comments", "sep-end"],
"sources": ["S040", "S041"], "entry": "program (prints to stdout)",
"article": r'''
# Your First Program: print()

## Intuition
A Python program is a text file of instructions that run from the top line to the bottom line.
The first instruction most people learn is `print`, which shows text on the screen (the
*standard output*). Everything you print here is checked by the tests, character by character.

## Precise explanation
```python
# A comment starts with # and is ignored by Python.
print("Hello, world!")        # text in double quotes is a *string*
print('Single quotes work too')
print("Python", "is", "fun")  # several values are joined with a space: Python is fun
print("2026", "10", "24", sep="-")   # sep replaces the space: 2026-10-24
print()                        # an empty line
print("Loading", end="...")   # end replaces the newline normally printed at the end
print("done")                  # continues on the same line: Loading...done
```
* A **string** is text between matching quotes. Use double quotes when the text contains a
  single quote (`"It's"`) and single quotes when it contains double quotes (`'She said "hi"'`).
* `print(a, b, c)` prints its arguments separated by `sep` (default `" "`) and then prints
  `end` (default `"\n"`, a newline).
* Python runs lines in order; a typo such as `Print(...)` stops the program with a `NameError`.

## Worked example
```python
print("Score", "10", sep=": ", end="!\n")
```
prints `Score: 10!` followed by a newline.

## Common mistakes
* Missing quotes: `print(Hello)` makes Python look for a variable called `Hello`.
* Mismatched quotes: `print("Hi')` is a `SyntaxError`.
* Extra spaces: `print("a ", "b")` prints `a  b` (two spaces) because `sep` adds one more.
* Forgetting that `end=""` removes the newline, so the next print continues on the same line.

## Why this matters
Every later program reports results through `print` or through return values. Getting output
exactly right is also how automatic graders and command-line tools communicate.
''',
"statement": r'''
Write a program that prints **exactly** these six lines (no extra spaces):

```
Hello, world!
Python is fun
2026-10-24
                         <- this line is empty
Loading...done
She said "hi"
```

**Requirements**
* Line 2 must come from one `print` call with three arguments: `"Python"`, `"is"`, `"fun"`.
* Line 3 must come from one `print` call with the arguments `"2026"`, `"10"`, `"24"` and `sep`.
* Line 5 must come from two `print` calls, the first using `end`.
* Line 6 contains double quotes, so write it with single quotes around it.

The tests run your file and compare everything it prints.
''',
"starter": r'''
# Print six lines. The first one is done for you.
print("Hello, world!")
# TODO: line 2 - print three words with one print call
# TODO: line 3 - use sep="-"
# TODO: line 4 - an empty line
# TODO: line 5 - two print calls, the first with end="..."
# TODO: line 6 - She said "hi"
''',
"hints": [
    "`print(\"Python\", \"is\", \"fun\")` already puts one space between the words.",
    "`print()` with no arguments prints an empty line; `sep=\"-\"` changes the separator.",
    "`print(\"Loading\", end=\"...\")` then `print(\"done\")`; finally `print('She said \"hi\"')`.",
],
"solution": r'''
# Line 1: a plain string
print("Hello, world!")
# Line 2: three arguments joined by the default separator " "
print("Python", "is", "fun")
# Line 3: a custom separator
print("2026", "10", "24", sep="-")
# Line 4: an empty line
print()
# Line 5: end="..." keeps the next print on the same line
print("Loading", end="...")
print("done")
# Line 6: single quotes around text that contains double quotes
print('She said "hi"')
''',
"explanation": r'''
Each `print` call writes its arguments joined by `sep` and then writes `end`. Changing `sep`
produces the date, an empty call produces the blank line, and `end="..."` replaces the newline
so that `done` continues the fifth line. Single quotes let the last string contain double quotes.
''',
"tests": r'''
EXPECTED = 'Hello, world!\nPython is fun\n2026-10-24\n\nLoading...done\nShe said "hi"\n'


class TestHelloPrint(unittest.TestCase):
    def test_exact_output(self):
        out, _ = run_program()
        self.assertEqual(out, EXPECTED)

    def test_first_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[0], "Hello, world!")

    def test_words_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[1:2], ["Python is fun"])

    def test_date_with_sep(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[2:3], ["2026-10-24"])

    def test_blank_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[3:4], [""])

    def test_end_joins_lines(self):
        out, _ = run_program()
        self.assertIn("Loading...done\n", out)

    def test_quotes(self):
        out, _ = run_program()
        self.assertTrue(out.endswith('She said "hi"\n'))

    def test_line_count(self):
        out, _ = run_program()
        self.assertEqual(len(out.splitlines()), 6)
''',
"feedback": [
    ("test_exact_output", "Compare your output with the six expected lines; look for extra spaces or missing lines."),
    ("test_words_line", "Use one print with three arguments; print adds the spaces for you."),
    ("test_date_with_sep", "Pass `sep=\"-\"` so the parts are joined by dashes, not spaces."),
    ("test_blank_line", "Line 4 must be empty: call `print()` with no arguments."),
    ("test_end_joins_lines", "The first call needs `end=\"...\"` so `done` continues the same line."),
    ("test_quotes", "Wrap the last string in single quotes so it can contain double quotes."),
],
},
# ---------------------------------------------------------------- variables
{
"slug": "variables", "title": "Variables and f-strings", "kind": "script",
"difficulty": "beginner", "prereqs": ["hello-print"], "packages": [],
"objectives": ["Create and reassign variables", "Choose readable snake_case names",
               "Do simple arithmetic with + - * /", "Insert values into text with f-strings"],
"tags": ["variables", "assignment", "f-strings", "naming"],
"sources": ["S040", "S041"], "entry": "program (module-level variables + stdout)",
"article": r'''
# Variables and f-strings

## Intuition
A variable is a name tag attached to a value. `age = 19` means "from now on, `age` refers to
19". You can later move the tag to a different value: `age = 20`.

## Precise explanation
```python
name = "Ada"          # a string
age = 19              # a whole number (int)
height_m = 1.68       # a decimal number (float)
is_student = True     # a truth value (bool): True or False
next_age = age + 1    # the right side is computed first, then stored: 20
```
* `=` is **assignment**, not "equals". The right-hand side is evaluated, then the name on the
  left is bound to the result.
* Names may contain letters, digits and `_`, cannot start with a digit, and are case-sensitive
  (`Age` and `age` are different). Python style uses `snake_case`.
* Python works as a calculator: `+ - * /` add, subtract, multiply and divide. `/` always gives
  a float: `7 / 2` is `3.5`. (More operators come in [[arithmetic-operators]].)
* An **f-string** inserts values into text: `f"Name: {name}"` → `Name: Ada`. Any expression can
  go inside the braces: `f"{age + 1}"` → `20`.

## Worked example
```python
price = 4
count = 3
total = price * count
print(f"{count} items cost {total}")   # 3 items cost 12
count = 5                              # reassignment
print(f"{count} items cost {total}")   # 5 items cost 12 — total was computed earlier!
```

## Common mistakes
* Using a variable before assigning it → `NameError`.
* Expecting `total` to update automatically when `count` changes; it stores a value, not a formula.
* Forgetting the `f` before the quotes: `"Name: {name}"` prints the braces literally.
* Writing `"Age: " + age` — you cannot add a string and an int (see [[types-conversion]]).

## Why this matters
Every model, dataset and hyperparameter in later topics lives in a variable. Clear names such as
`learning_rate` instead of `x` make code readable.
''',
"statement": r'''
Write a program that creates these variables with exactly these values and types:

| Variable | Value |
|---|---|
| `name` | `"Ada"` |
| `age` | `19` |
| `height_m` | `1.68` |
| `is_student` | `True` |
| `next_age` | `age + 1` (compute it; do not type 20) |

Then print exactly four lines using f-strings:

```
Name: Ada
Age next year: 20
Height: 1.68 m
Student: True
```

The tests read your variables after the program runs and compare its output.
''',
"starter": r'''
name = "Ada"
# TODO: create age, height_m, is_student and next_age

print(f"Name: {name}")
# TODO: print the other three lines
''',
"hints": [
    "Numbers are written without quotes: `age = 19`, `height_m = 1.68`.",
    "`True` has a capital T and no quotes; `next_age = age + 1`.",
    "`print(f\"Age next year: {next_age}\")` inserts the value into the text.",
],
"solution": r'''
name = "Ada"
age = 19
height_m = 1.68
is_student = True
next_age = age + 1

print(f"Name: {name}")
print(f"Age next year: {next_age}")
print(f"Height: {height_m} m")
print(f"Student: {is_student}")
''',
"explanation": r'''
Four assignments create the variables with the requested types; `next_age` is computed from
`age`, so changing `age` and re-running the program would update it. Each f-string inserts one
variable into a fixed label.
''',
"tests": r'''
class TestVariables(unittest.TestCase):
    def test_name(self):
        _, m = run_program()
        self.assertEqual(m.name, "Ada")

    def test_age_is_int(self):
        _, m = run_program()
        self.assertEqual(m.age, 19)
        self.assertIsInstance(m.age, int)

    def test_height_is_float(self):
        _, m = run_program()
        self.assertIsInstance(m.height_m, float)
        self.assertAlmostEqual(m.height_m, 1.68)

    def test_is_student_bool(self):
        _, m = run_program()
        self.assertIs(m.is_student, True)

    def test_next_age(self):
        _, m = run_program()
        self.assertEqual(m.next_age, 20)

    def test_output(self):
        out, _ = run_program()
        self.assertEqual(out, "Name: Ada\nAge next year: 20\nHeight: 1.68 m\nStudent: True\n")
''',
"feedback": [
    ("test_age_is_int", "Write `age = 19` without quotes; `\"19\"` is a string."),
    ("test_height_is_float", "Use `1.68` (a float), not `\"1.68\"`."),
    ("test_is_student_bool", "Use the keyword `True` (capital T, no quotes)."),
    ("test_next_age", "Compute `next_age = age + 1` after creating `age`."),
    ("test_output", "Your printed lines must match the expected output exactly: check each label, the ` m` after the height, and that you used f-strings with braces around the variable names."),
],
},
# ---------------------------------------------------------------- types-conversion
{
"slug": "types-conversion", "title": "Types and Conversion", "kind": "script",
"difficulty": "beginner", "prereqs": ["variables"], "packages": [],
"objectives": ["Recognise int, float, str and bool values", "Inspect a value with type()",
               "Convert between types with int(), float(), str() and round()"],
"tags": ["types", "int", "float", "str", "bool", "conversion"],
"sources": ["S040", "S048", "S049"], "entry": "program (module-level variables + stdout)",
"article": r'''
# Types and Conversion

## Intuition
`"3"` and `3` look alike on screen but are different kinds of value: one is text, the other a
number. Python must know the **type** of a value to know what operations mean: `"3" + "3"` is
`"33"`, while `3 + 3` is `6`.

## Precise explanation
| Type | Examples | Notes |
|---|---|---|
| `int` | `0`, `-7`, `2026` | whole numbers, any size |
| `float` | `3.5`, `0.1`, `2.0` | decimals, stored approximately |
| `str` | `"hi"`, `"19.99"` | text |
| `bool` | `True`, `False` | truth values |

* `type(x)` returns the type; `type(x).__name__` is its name as text, e.g. `"float"`.
* Conversions create a **new** value: `int("3")` → `3`, `float("19.99")` → `19.99`,
  `str(3)` → `"3"`, `int(3.9)` → `3` (truncates toward zero), `bool(0)` → `False`.
* `round(x, 2)` rounds to two decimal places.
* Mixing types: `int + float` gives a float; `str + int` is a `TypeError` — convert first.

## Worked example
```python
quantity_text = "3"
quantity = int(quantity_text)   # 3
label = str(quantity) + " items" # "3 items"
print(type(quantity).__name__)  # int
print(0.1 + 0.2)                # 0.30000000000000004  (floats are approximate)
print(round(0.1 + 0.2, 2))      # 0.3
```

## Common mistakes
* `int("19.99")` raises `ValueError`; use `float("19.99")` first.
* Comparing floats exactly; `0.1 + 0.2 == 0.3` is `False`. Round or compare with a tolerance.
* Expecting `int(2.7)` to round to 3 — it truncates to 2.

## Why this matters
Data read from files, forms and the keyboard always arrives as text. Converting it correctly is
the first step of every data pipeline, and dtype mistakes are a common source of ML bugs.
''',
"statement": r'''
The starter defines three text values that came from a form:

```python
price_text = "19.99"
quantity_text = "3"
discount_text = "0.1"
```

Create:
* `price` — `price_text` as a `float`
* `quantity` — `quantity_text` as an `int`
* `discount` — `discount_text` as a `float`
* `total` — `price * quantity * (1 - discount)`
* `total_rounded` — `total` rounded to 2 decimal places
* `label` — the text `"3 items"`, built with `str(quantity) + " items"`

Then print exactly:
```
Total: 53.97
price is float
quantity is int
3 items
```
Use `type(...).__name__` for lines 2 and 3.
''',
"starter": r'''
price_text = "19.99"
quantity_text = "3"
discount_text = "0.1"

# TODO: convert the three texts, compute total, total_rounded and label
# TODO: print the four lines
''',
"hints": [
    "`price = float(price_text)` and `quantity = int(quantity_text)`.",
    "`total_rounded = round(total, 2)`; print it with an f-string.",
    "`print(f\"price is {type(price).__name__}\")` prints the type's name.",
],
"solution": r'''
price_text = "19.99"
quantity_text = "3"
discount_text = "0.1"

price = float(price_text)
quantity = int(quantity_text)
discount = float(discount_text)
total = price * quantity * (1 - discount)
total_rounded = round(total, 2)
label = str(quantity) + " items"

print(f"Total: {total_rounded}")
print(f"price is {type(price).__name__}")
print(f"quantity is {type(quantity).__name__}")
print(label)
''',
"explanation": r'''
Each text is converted with the function for its target type. The total is computed with
floats, then rounded only for display, so `total` keeps full precision. `str(quantity)` turns
the number back into text before it is joined with `" items"`.
''',
"tests": r'''
class TestTypes(unittest.TestCase):
    def test_price_float(self):
        _, m = run_program()
        self.assertIsInstance(m.price, float)
        self.assertAlmostEqual(m.price, 19.99)

    def test_quantity_int(self):
        _, m = run_program()
        self.assertIsInstance(m.quantity, int)
        self.assertEqual(m.quantity, 3)

    def test_discount_float(self):
        _, m = run_program()
        self.assertIsInstance(m.discount, float)
        self.assertAlmostEqual(m.discount, 0.1)

    def test_total(self):
        _, m = run_program()
        self.assertAlmostEqual(m.total, 19.99 * 3 * 0.9, places=9)
        self.assertEqual(m.total_rounded, 53.97)

    def test_label(self):
        _, m = run_program()
        self.assertEqual(m.label, "3 items")

    def test_output(self):
        out, _ = run_program()
        self.assertEqual(out, "Total: 53.97\nprice is float\nquantity is int\n3 items\n")
''',
"feedback": [
    ("test_price_float", "Use `float(price_text)`; `int` cannot parse `\"19.99\"`."),
    ("test_quantity_int", "Use `int(quantity_text)` so quantity is a whole number."),
    ("test_total", "Multiply by `(1 - discount)` and round only `total_rounded`, not `total`."),
    ("test_label", "Convert with `str(quantity)` before adding `\" items\"`."),
    ("test_output", "Print `total_rounded`, then the two type names from `type(x).__name__`, then the label."),
],
},
# ---------------------------------------------------------------- input-output
{
"slug": "input-output", "title": "Reading Input", "kind": "script",
"difficulty": "beginner", "prereqs": ["types-conversion"], "packages": [],
"objectives": ["Read a line of text with input()", "Remember that input() always returns a str",
               "Clean input with strip() and convert it to a number"],
"tags": ["input", "stdin", "conversion", "strip"],
"sources": ["S041", "S048"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# Reading Input

## Intuition
`print` sends text out; `input` brings text in. When a program reaches `input()` it waits for
one line from the keyboard (or from whatever is connected to *standard input*, such as a file or
an automatic grader) and gives it to you as a string.

## Precise explanation
```python
name = input()                 # one line, without the trailing newline, always a str
year = int(input())            # convert when you need a number
city = input("City? ")         # an optional prompt is printed first (not used in graded tasks)
```
* `input()` returns a `str`, even if the user typed digits. `input() + 1` is a `TypeError`.
* `text.strip()` removes spaces, tabs and newlines from both ends. `int()` and `float()`
  already ignore surrounding whitespace, but names and words do not.
* Each call reads the **next** line. If there is no line left, Python raises `EOFError`.

## Worked example
Input:
```
  Grace
1990
```
```python
name = input().strip()     # "Grace"
birth_year = int(input())  # 1990
print(f"Hello, {name}! In 2030 you will turn {2030 - birth_year}.")
```
Output: `Hello, Grace! In 2030 you will turn 40.`

## Common mistakes
* Forgetting `int(...)`, then subtracting a string.
* Printing a prompt in graded tasks: the prompt becomes part of your output and breaks exact
  comparisons. Tests in this site supply input directly, so call `input()` with no prompt.
* Calling `input()` more times than there are lines.

## Why this matters
Reading and validating outside data is where most real programs start: command-line tools,
web forms ([[http-requests]] later) and dataset files all deliver text you must parse.
''',
"statement": r'''
Read two lines from standard input:
1. a name (it may have spaces around it — remove them with `strip()`),
2. a birth year (an integer).

Print exactly two lines:
```
Hello, <name>!
In 2030 you will turn <2030 - year>.
```

Call `input()` **without** a prompt.

**Example**
```
input:  Ada
        2006
output: Hello, Ada!
        In 2030 you will turn 24.
```
''',
"starter": r'''
name = input()
# TODO: clean the name, read and convert the year, print two lines
''',
"hints": [
    "`name = input().strip()` removes surrounding spaces.",
    "`year = int(input())` reads the second line as a number.",
    "Compute `2030 - year` inside an f-string.",
],
"solution": r'''
name = input().strip()
year = int(input())
print(f"Hello, {name}!")
print(f"In 2030 you will turn {2030 - year}.")
''',
"explanation": r'''
The first `input()` reads the name and `strip()` removes stray spaces. The second line is
converted to an `int` so that subtraction works. Both results are printed with f-strings.
''',
"tests": r'''
class TestInputOutput(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("Ada\n2006\n")
        self.assertEqual(out, "Hello, Ada!\nIn 2030 you will turn 24.\n")

    def test_strips_name(self):
        out, _ = run_program("   Grace  \n1990\n")
        self.assertEqual(out.splitlines()[0], "Hello, Grace!")

    def test_year_with_spaces(self):
        out, _ = run_program("Linus\n  1969 \n")
        self.assertEqual(out.splitlines()[1:], ["In 2030 you will turn 61."])

    def test_two_word_name(self):
        out, _ = run_program("Alan Turing\n1912\n")
        self.assertEqual(out, "Hello, Alan Turing!\nIn 2030 you will turn 118.\n")

    def test_future_year(self):
        out, _ = run_program("Kid\n2030\n")
        self.assertEqual(out.splitlines()[1], "In 2030 you will turn 0.")

    def test_no_prompt_text(self):
        out, _ = run_program("Ada\n2006\n")
        self.assertTrue(out.startswith("Hello, "))
''',
"feedback": [
    ("test_strips_name", "Call `.strip()` on the name you read."),
    ("test_year_with_spaces", "Convert the second line with `int(...)` and subtract it from 2030."),
    ("test_no_prompt_text", "Do not pass a prompt to `input()`; it is printed as part of your output."),
    ("test_example", "Check punctuation: `Hello, Ada!` and a full stop after the age."),
],
},
# ---------------------------------------------------------------- arithmetic-operators
{
"slug": "arithmetic-operators", "title": "Arithmetic Operators", "kind": "script",
"difficulty": "beginner", "prereqs": ["input-output"], "packages": [],
"objectives": ["Use //, % and ** alongside + - * /", "Apply operator precedence and parentheses",
               "Format numbers with :02d and :.2f"],
"tags": ["operators", "integer-division", "modulo", "precedence", "formatting"],
"sources": ["S040", "S049"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# Arithmetic Operators

## Intuition
Converting 3725 seconds into hours, minutes and seconds is a division with remainders: how many
whole hours fit, and what is left over? Python has an operator for each part.

## Precise explanation
| Operator | Meaning | Example |
|---|---|---|
| `+ - *` | add, subtract, multiply | `7 * 2 == 14` |
| `/` | true division (always float) | `7 / 2 == 3.5` |
| `//` | floor division (round down) | `7 // 2 == 3`, `-7 // 2 == -4` |
| `%` | remainder (modulo) | `7 % 2 == 1` |
| `**` | power | `2 ** 10 == 1024` |

* For non-negative `a` and positive `b`: `a == (a // b) * b + a % b`.
* **Precedence**: `**` first, then `* / // %`, then `+ -`; use parentheses to be explicit:
  `2 + 3 * 4 == 14`, `(2 + 3) * 4 == 20`, `-2 ** 2 == -4`.
* **Augmented assignment**: `x += 5` means `x = x + 5` (also `-=`, `*=`, `//=`, ...).
* **Format specs** inside f-strings: `f"{5:02d}"` → `05` (at least 2 digits, zero-padded);
  `f"{62.0833:.2f}"` → `62.08` (two decimals).

## Worked example
`3725` seconds: hours = `3725 // 3600` = 1; remaining = `3725 % 3600` = 125;
minutes = `125 // 60` = 2; seconds = `125 % 60` = 5 → `1:02:05`.

## Common mistakes
* Using `/` where you want a whole number: `3725 / 3600` is `1.034...`.
* Forgetting zero-padding, producing `1:2:5`.
* Writing `x ^ 2` for a power — `^` is bitwise XOR in Python; use `x ** 2`.

## Why this matters
Integer division and remainders appear in batching (`n // batch_size` full batches), image
indexing (row = `i // width`, column = `i % width`) and time-series resampling.
''',
"statement": r'''
Read one non-negative integer: a number of seconds. Print two lines:

1. The duration as `H:MM:SS` — hours without padding, minutes and seconds with two digits.
2. The duration in minutes with exactly two decimals, followed by ` minutes`.

**Example**
```
input:  3725
output: 1:02:05
        62.08 minutes
```
Hours may exceed 24 (`90000` → `25:00:00`).
''',
"starter": r'''
total = int(input())
# TODO: compute hours, minutes and seconds with // and %
# TODO: print H:MM:SS and the minutes with two decimals
''',
"hints": [
    "`hours = total // 3600` and `rest = total % 3600`.",
    "`minutes = rest // 60`, `seconds = rest % 60`.",
    "`print(f\"{hours}:{minutes:02d}:{seconds:02d}\")` and `print(f\"{total / 60:.2f} minutes\")`.",
],
"solution": r'''
total = int(input())
hours = total // 3600
rest = total % 3600
minutes = rest // 60
seconds = rest % 60
print(f"{hours}:{minutes:02d}:{seconds:02d}")
print(f"{total / 60:.2f} minutes")
''',
"explanation": r'''
Floor division gives the number of whole hours; the remainder holds what is left, which is split
again into minutes and seconds. `:02d` pads minutes and seconds to two digits and `:.2f` shows
the true-division result with two decimals.
''',
"tests": r'''
class TestDuration(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("3725\n")
        self.assertEqual(out, "1:02:05\n62.08 minutes\n")

    def test_zero(self):
        out, _ = run_program("0\n")
        self.assertEqual(out, "0:00:00\n0.00 minutes\n")

    def test_padding(self):
        out, _ = run_program("59\n")
        self.assertEqual(out.splitlines()[0], "0:00:59")

    def test_exact_hour(self):
        out, _ = run_program("3600\n")
        self.assertEqual(out, "1:00:00\n60.00 minutes\n")

    def test_end_of_day(self):
        out, _ = run_program("86399\n")
        self.assertEqual(out, "23:59:59\n1439.98 minutes\n")

    def test_more_than_a_day(self):
        out, _ = run_program("90000\n")
        self.assertEqual(out.splitlines()[0], "25:00:00")

    def test_minutes_two_decimals(self):
        out, _ = run_program("61\n")
        self.assertEqual(out.splitlines()[1], "1.02 minutes")
''',
"feedback": [
    ("test_padding", "Pad minutes and seconds with `:02d`."),
    ("test_zero", "Use `:.2f` so zero is printed as `0.00`."),
    ("test_end_of_day", "Take the remainder after removing hours before computing minutes."),
    ("test_more_than_a_day", "Do not wrap hours at 24; just use `total // 3600`."),
    ("test_minutes_two_decimals", "Minutes use true division `/`, then `:.2f` formatting."),
],
},
# ---------------------------------------------------------------- string-basics
{
"slug": "string-basics", "title": "Strings: Indexing, Slicing and Methods", "kind": "script",
"difficulty": "beginner", "prereqs": ["arithmetic-operators"], "packages": [],
"objectives": ["Index characters with positive and negative indices", "Slice substrings, including with a step",
               "Use len(), upper(), lower(), strip(), replace() and the in operator"],
"tags": ["strings", "indexing", "slicing", "string-methods"],
"sources": ["S040", "S049"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# Strings: Indexing, Slicing and Methods

## Intuition
A string is a row of characters with numbered positions, starting at 0. You can point at one
position, cut out a piece, or ask the string to produce a changed copy of itself.

## Precise explanation
```
 P   y   t   h   o   n
 0   1   2   3   4   5     positive index
-6  -5  -4  -3  -2  -1     negative index (counts from the end)
```
* `word[0]` → `"P"`, `word[-1]` → `"n"`. An index past the end raises `IndexError`.
* **Slicing** `word[start:stop]` takes positions `start` up to but **not including** `stop`:
  `word[0:3]` → `"Pyt"`; omitted ends mean "from the start"/"to the end": `word[:3]`, `word[3:]`.
  Slices never raise errors: `"ab"[:3]` → `"ab"`.
* A third number is the step: `word[::2]` → `"Pto"`, `word[::-1]` → `"nohtyP"` (reversed).
* `len(word)` → 6. `"th" in word` → `True` (substring test).
* Methods return **new** strings: `word.upper()`, `word.lower()`, `"  x ".strip()`,
  `"a-b".replace("-", "+")`, `"py".title()`. Strings are immutable: `word[0] = "J"` is an error.

## Worked example
`word = "Python"` → `len(word)` 6, `word[0]` P, `word[-1]` n, `word[:3]` Pyt,
`word[::-1]` nohtyP, `word.upper()` PYTHON, `"th" in word` True.

## Common mistakes
* Off-by-one: the last character is `word[len(word) - 1]`, not `word[len(word)]`.
* Expecting `word.upper()` to change `word`; store the result if you need it.
* Confusing `word[1:3]` (2 characters) with "characters 1 to 3 inclusive".

## Why this matters
Text cleaning in NLP, parsing HTTP requests and file names, and reading model output all rely on
slicing and string methods.
''',
"statement": r'''
Read one word (strip surrounding spaces). Print exactly these seven lines for it:

```
Length: <number of characters>
First: <first character>
Last: <last character>
First three: <first three characters, or the whole word if shorter>
Reversed: <the word backwards>
Upper: <the word in upper case>
Contains 'th': <True or False>
```

**Example** for `Python`:
```
Length: 6
First: P
Last: n
First three: Pyt
Reversed: nohtyP
Upper: PYTHON
Contains 'th': True
```
The word has at least one character. The `'th'` test is case-sensitive.
''',
"starter": r'''
word = input().strip()
print(f"Length: {len(word)}")
# TODO: print the remaining six lines
''',
"hints": [
    "`word[0]` is the first character and `word[-1]` the last.",
    "`word[:3]` never fails even if the word is shorter; `word[::-1]` reverses it.",
    "`'th' in word` gives True or False; print it inside an f-string.",
],
"solution": r'''
word = input().strip()
print(f"Length: {len(word)}")
print(f"First: {word[0]}")
print(f"Last: {word[-1]}")
print(f"First three: {word[:3]}")
print(f"Reversed: {word[::-1]}")
print(f"Upper: {word.upper()}")
print(f"Contains 'th': {'th' in word}")
''',
"explanation": r'''
Indexing picks single characters, slicing with omitted bounds handles short words safely, and a
negative step reverses the string. `upper()` returns a new string and `in` returns a bool.
''',
"tests": r'''
def lines_for(word):
    out, _ = run_program(word + "\n")
    return out.splitlines()


class TestStrings(unittest.TestCase):
    def test_python(self):
        self.assertEqual(lines_for("Python"), [
            "Length: 6", "First: P", "Last: n", "First three: Pyt",
            "Reversed: nohtyP", "Upper: PYTHON", "Contains 'th': True"])

    def test_short_word(self):
        self.assertEqual(lines_for("ab")[3], "First three: ab")

    def test_single_character(self):
        lines = lines_for("x")
        self.assertEqual(lines[1:5], ["First: x", "Last: x", "First three: x", "Reversed: x"])

    def test_strip(self):
        self.assertEqual(lines_for("   data  ")[0], "Length: 4")

    def test_contains_false(self):
        self.assertEqual(lines_for("THEN")[6], "Contains 'th': False")

    def test_reverse_palindrome(self):
        self.assertEqual(lines_for("level")[4], "Reversed: level")

    def test_upper(self):
        self.assertEqual(lines_for("mathematics")[5], "Upper: MATHEMATICS")
''',
"feedback": [
    ("test_short_word", "Use a slice `word[:3]`; slices stop at the end of the string without errors."),
    ("test_strip", "Strip the input before measuring its length."),
    ("test_contains_false", "The test is case-sensitive: use `'th' in word` on the original word."),
    ("test_single_character", "Use `word[-1]` for the last character and `word[::-1]` to reverse."),
],
},
# ---------------------------------------------------------------- conditionals
{
"slug": "conditionals", "title": "Conditionals: Letter Grades", "kind": "script",
"difficulty": "beginner", "prereqs": ["string-basics"], "packages": [],
"objectives": ["Compare values with == != < <= > >=", "Branch with if / elif / else",
               "Combine conditions with and, or, not and chained comparisons"],
"tags": ["conditionals", "if-elif-else", "comparisons", "boolean-logic"],
"sources": ["S042", "S049"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# Conditionals

## Intuition
Programs make decisions: *if* the score is at least 90, the grade is A; *otherwise, if* it is at
least 80, B; and so on. Python checks the conditions from top to bottom and runs the first block
whose condition is true.

## Precise explanation
```python
if score < 0 or score > 100:
    print("Invalid score")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")
```
* Comparisons produce bools: `==` equal, `!=` not equal, `<`, `<=`, `>`, `>=`.
* `and` is true only if both sides are; `or` if at least one is; `not` flips a bool.
* Chained comparison: `0 <= score <= 100` means `0 <= score and score <= 100`.
* The **indented** lines (4 spaces) form the block. `elif` and `else` are optional; at most one
  branch runs.
* `=` assigns, `==` compares. `if score = 90:` is a `SyntaxError`.

## Worked example
`score = 85`: `85 < 0 or 85 > 100` is False → `85 >= 90` False → `85 >= 80` True → prints `B`;
the remaining branches are skipped.

## Common mistakes
* Wrong order: testing `score >= 60` before `score >= 90` gives every passing score a D.
* Writing `if 0 <= score and <= 100` — each side of `and` must be a full comparison.
* Forgetting the colon after the condition, or mixing tabs and spaces.

## Why this matters
Thresholds turn model scores into decisions (spam / not spam), and branches handle edge cases
such as empty data, which you will meet in every later topic.
''',
"statement": r'''
Read one integer score. Print two lines.

Line 1 — the grade:
| Score | Output |
|---|---|
| below 0 or above 100 | `Invalid score` |
| 90–100 | `A` |
| 80–89 | `B` |
| 70–79 | `C` |
| 60–69 | `D` |
| 0–59 | `F` |

Line 2 — `Pass` if the score is valid and at least 60, `Fail` if it is valid and below 60, and
`Check the input` if it is invalid.
''',
"starter": r'''
score = int(input())
if score >= 90:
    print("A")
else:
    print("F")
# TODO: handle invalid scores and the B, C, D bands, then print the second line
''',
"hints": [
    "Test the invalid case first: `if score < 0 or score > 100:`.",
    "Then go from the highest band down with `elif score >= 90:`, `elif score >= 80:` ...",
    "For line 2 use a second if/elif/else; `0 <= score <= 100` checks validity.",
],
"solution": r'''
score = int(input())

if score < 0 or score > 100:
    print("Invalid score")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

if not 0 <= score <= 100:
    print("Check the input")
elif score >= 60:
    print("Pass")
else:
    print("Fail")
''',
"explanation": r'''
Invalid scores are handled first so that later branches only see 0–100. The bands are tested from
highest to lowest, so each `elif` implicitly knows the score is below the previous threshold.
The second decision reuses a chained comparison for validity.
''',
"tests": r'''
def grade(score):
    out, _ = run_program(f"{score}\n")
    return out.splitlines()


class TestGrades(unittest.TestCase):
    def test_a_band(self):
        self.assertEqual(grade(95), ["A", "Pass"])

    def test_boundaries_top(self):
        self.assertEqual(grade(100), ["A", "Pass"])
        self.assertEqual(grade(90), ["A", "Pass"])
        self.assertEqual(grade(89), ["B", "Pass"])

    def test_middle_bands(self):
        self.assertEqual(grade(80)[0], "B")
        self.assertEqual(grade(79)[0], "C")
        self.assertEqual(grade(70)[0], "C")
        self.assertEqual(grade(69)[0], "D")

    def test_pass_boundary(self):
        self.assertEqual(grade(60), ["D", "Pass"])
        self.assertEqual(grade(59), ["F", "Fail"])

    def test_zero(self):
        self.assertEqual(grade(0), ["F", "Fail"])

    def test_invalid_low(self):
        self.assertEqual(grade(-1), ["Invalid score", "Check the input"])

    def test_invalid_high(self):
        self.assertEqual(grade(101), ["Invalid score", "Check the input"])
''',
"feedback": [
    ("test_boundaries_top", "Use `>=` so that exactly 90 is an A and 89 is a B."),
    ("test_middle_bands", "Check the bands from highest to lowest with elif."),
    ("test_invalid_high", "Handle scores above 100 before the A band."),
    ("test_invalid_low", "Negative scores are invalid, not F."),
    ("test_pass_boundary", "60 passes; 59 fails."),
],
},
# ---------------------------------------------------------------- while-loops
{
"slug": "while-loops", "title": "While Loops: Read Until Done", "kind": "script",
"difficulty": "beginner", "prereqs": ["conditionals"], "packages": [],
"objectives": ["Repeat work with while", "Stop a loop with a sentinel value and break",
               "Keep running totals, counts and maxima", "Use None for 'no value yet'"],
"tags": ["while", "break", "sentinel", "accumulator"],
"sources": ["S042"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# While Loops

## Intuition
Sometimes you do not know in advance how many times to repeat something: "keep reading numbers
until the user types `done`". A `while` loop repeats its block for as long as its condition is
true.

## Precise explanation
```python
count = 0
while count < 3:      # checked before every repetition
    print(count)
    count += 1        # without this the loop never ends
```
* `while True:` loops forever until a `break` statement leaves it — a common pattern when the
  stopping condition is discovered *inside* the loop.
* `continue` skips the rest of the current repetition.
* A **sentinel** is a special input that means "stop", such as `done`.
* `None` represents "no value yet". Test it with `is None`.

```python
largest = None
while True:
    line = input().strip()
    if line == "done":
        break
    x = int(line)
    if largest is None or x > largest:
        largest = x
```

## Worked example
Lines `4`, `9`, `2`, `done`: count 1→2→3, total 4→13→15, largest 4→9→9. Output:
`count=3 total=15 max=9`.

## Common mistakes
* Infinite loops: the condition never becomes false and there is no `break`.
* Converting the sentinel: `int("done")` raises `ValueError`; check for it first.
* Starting `largest = 0`, which is wrong when every number is negative.

## Why this matters
Training loops run "until converged", agents loop "until the goal is reached or the step budget
runs out" ([[goal-and-budget]] later), and servers loop over incoming requests.
''',
"statement": r'''
Read integers, one per line, until a line equal to `done` (ignore surrounding spaces). Then print
one line:

```
count=<how many numbers> total=<their sum> max=<the largest>
```
If `done` is the first line, print `count=0 total=0 max=None`. Numbers may be negative.
''',
"starter": r'''
count = 0
total = 0
largest = None
# TODO: loop, reading lines until "done"; update count, total and largest
print(f"count={count} total={total} max={largest}")
''',
"hints": [
    "Use `while True:` and read `line = input().strip()` at the top of the loop.",
    "`if line == \"done\": break` must come before `int(line)`.",
    "Update the maximum with `if largest is None or x > largest: largest = x`.",
],
"solution": r'''
count = 0
total = 0
largest = None
while True:
    line = input().strip()
    if line == "done":
        break
    x = int(line)
    count += 1
    total += x
    if largest is None or x > largest:
        largest = x
print(f"count={count} total={total} max={largest}")
''',
"explanation": r'''
The loop has no natural end, so `while True` with a `break` on the sentinel is clearest. Three
accumulators are updated per number; starting the maximum at `None` makes the first number win
regardless of sign, and lets the empty case print `None`.
''',
"tests": r'''
class TestReadUntilDone(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("4\n9\n2\ndone\n")
        self.assertEqual(out, "count=3 total=15 max=9\n")

    def test_empty(self):
        out, _ = run_program("done\n")
        self.assertEqual(out, "count=0 total=0 max=None\n")

    def test_negatives(self):
        out, _ = run_program("-5\n-2\n-9\ndone\n")
        self.assertEqual(out, "count=3 total=-16 max=-2\n")

    def test_single(self):
        out, _ = run_program("7\ndone\n")
        self.assertEqual(out, "count=1 total=7 max=7\n")

    def test_spaces_around_done(self):
        out, _ = run_program("1\n2\n  done  \n")
        self.assertEqual(out, "count=2 total=3 max=2\n")

    def test_stops_at_done(self):
        out, _ = run_program("1\ndone\n100\n")
        self.assertEqual(out, "count=1 total=1 max=1\n")
''',
"feedback": [
    ("test_negatives", "Start `largest` at `None`, not 0, so negative maxima work."),
    ("test_spaces_around_done", "Strip each line before comparing it with `done`."),
    ("test_stops_at_done", "Break as soon as you see `done`; ignore anything after it."),
    ("test_empty", "If `done` comes first, print the initial values: 0, 0 and None."),
],
},
# ---------------------------------------------------------------- for-loops-range
{
"slug": "for-loops-range", "title": "For Loops and range: FizzBuzz", "kind": "script",
"difficulty": "beginner", "prereqs": ["while-loops"], "packages": [],
"objectives": ["Loop a known number of times with for and range", "Use range(start, stop, step)",
               "Loop over the characters of a string", "Combine loops with conditionals and %"],
"tags": ["for", "range", "iteration", "fizzbuzz"],
"sources": ["S042"], "entry": "program (reads stdin, prints to stdout)",
"article": r'''
# For Loops and range

## Intuition
When you know what to repeat over — the numbers 1 to n, or the letters of a word — a `for` loop
is simpler than `while`: it hands you each item in turn and stops by itself.

## Precise explanation
```python
for i in range(5):        # 0, 1, 2, 3, 4   (stop is excluded)
    print(i)
for i in range(1, 6):     # 1, 2, 3, 4, 5
    ...
for i in range(10, 0, -3):  # 10, 7, 4, 1  (step may be negative)
    ...
for ch in "abc":          # 'a', 'b', 'c'
    ...
```
* `range(stop)`, `range(start, stop)`, `range(start, stop, step)` produce integers from `start`
  up to but not including `stop`. `range(0)` and `range(1, 1)` are empty.
* `break` and `continue` work as in while loops.
* Loops can be nested; the inner loop runs completely for each outer repetition.

## Worked example
Sum of multiples of 3 or 5 up to 10:
```python
total = 0
for i in range(1, 11):
    if i % 3 == 0 or i % 5 == 0:
        total += i          # 3 + 5 + 6 + 9 + 10 = 33
```

## Common mistakes
* `range(1, n)` stops at `n - 1`; use `range(1, n + 1)` to include n.
* Testing `% 3` before `% 15` in FizzBuzz, so 15 prints `Fizz` instead of `FizzBuzz`.
* Changing the loop variable inside the loop and expecting it to affect the next repetition.

## Why this matters
Epoch loops in training, sweeps over hyperparameters, and iteration over pixels, tokens and
episodes are all `for` loops.
''',
"statement": r'''
Read an integer `n` (0 ≤ n ≤ 1000). For each `i` from 1 to `n` print one line:
* `FizzBuzz` if `i` is divisible by both 3 and 5,
* `Fizz` if divisible by 3 only,
* `Buzz` if divisible by 5 only,
* otherwise the number itself.

Finally print `sum=<sum of all i from 1 to n divisible by 3 or 5>`.

**Example** for `n = 5`:
```
1
2
Fizz
4
Buzz
sum=8
```
''',
"starter": r'''
n = int(input())
total = 0
# TODO: loop from 1 to n, print FizzBuzz lines and add multiples of 3 or 5 to total
print(f"sum={total}")
''',
"hints": [
    "`for i in range(1, n + 1):` includes n.",
    "Check `i % 15 == 0` (or `i % 3 == 0 and i % 5 == 0`) before the single cases.",
    "Add to `total` inside `if i % 3 == 0 or i % 5 == 0:`.",
],
"solution": r'''
n = int(input())
total = 0
for i in range(1, n + 1):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
    if i % 3 == 0 or i % 5 == 0:
        total += i
print(f"sum={total}")
''',
"explanation": r'''
`range(1, n + 1)` visits every number once. The combined case is tested first because a number
divisible by 15 also passes the single tests. The sum is a separate condition inside the same
loop, so no second pass is needed.
''',
"tests": r'''
class TestFizzBuzz(unittest.TestCase):
    def test_five(self):
        out, _ = run_program("5\n")
        self.assertEqual(out, "1\n2\nFizz\n4\nBuzz\nsum=8\n")

    def test_fifteen_line(self):
        out, _ = run_program("15\n")
        self.assertEqual(out.splitlines()[14], "FizzBuzz")

    def test_fifteen_sum(self):
        out, _ = run_program("15\n")
        self.assertEqual(out.splitlines()[-1], "sum=60")

    def test_zero(self):
        out, _ = run_program("0\n")
        self.assertEqual(out, "sum=0\n")

    def test_one(self):
        out, _ = run_program("1\n")
        self.assertEqual(out, "1\nsum=0\n")

    def test_line_count(self):
        out, _ = run_program("100\n")
        lines = out.splitlines()
        self.assertEqual(len(lines), 101)
        self.assertEqual(lines[-1], "sum=2418")
''',
"feedback": [
    ("test_fifteen_line", "Test divisibility by both 3 and 5 before testing 3 alone."),
    ("test_five", "Use `range(1, n + 1)` so n itself is included."),
    ("test_zero", "With n = 0 the loop runs zero times; only the sum line is printed."),
    ("test_fifteen_sum", "Add i to the total when it is divisible by 3 **or** 5."),
],
},
]
