"""Ungraded project ideas for the Python topic (library revision, Phase 6)."""

PROBLEMS = [
{
"kind": "project", "slug": "expense-tracker-cli", "title": "Expense Tracker CLI",
"tags": ["command-line", "files", "json"],
"brief": r'''
Build a command-line program that records your expenses, saves them to a JSON file between runs, and
prints summaries: total this month, spending by category and your biggest purchases.
''',
"uses": ["input-output", "for-loops-range", "gradebook-aggregate", "safe-divide", "files-and-json"],
"milestones": [
    "Ask for an amount, a category and a note with input() and keep the expense in a list of dicts.",
    "Save the list to expenses.json when the program exits and load it when it starts.",
    "Add a menu: add, list, summary, quit.",
    "Summarise totals per category with a dict, sorted from largest to smallest.",
    "Handle bad input (letters for an amount, an empty category) without crashing.",
],
"stretch": [
    "Use argparse so commands like `python expenses.py add 120 food lunch` work without a menu.",
    "Export a month to CSV.",
    "Set monthly budgets per category and warn when one is exceeded.",
],
"data": r'''
Your own expenses — or invent a week of them to test with. See the [json module](https://docs.python.org/3/library/json.html)
and [argparse](https://docs.python.org/3/library/argparse.html) documentation.
''',
"setup": r'''
```bash
python expenses.py
```
Only the standard library is needed.
''',
},
{
"kind": "project", "slug": "quiz-game", "title": "Quiz Game with High Scores",
"tags": ["games", "classes", "testing"],
"brief": r'''
Build a quiz game that loads questions from a file, asks them in random order, keeps score with time
bonuses, and stores a high-score table — with unit tests for the scoring rules.
''',
"uses": ["standard-library", "files-and-json", "bank-account", "shapes-inheritance", "unit-testing"],
"milestones": [
    "Store questions (text, options, answer, category) in a JSON file and load them into Question objects.",
    "Ask ten random questions, check answers and show the score.",
    "Add a Player class and a high-score table saved to a file, keeping the top five.",
    "Give multiple-choice and true/false questions their own subclasses with a shared check() method.",
    "Write unittest tests for scoring, loading and the high-score table.",
],
"stretch": [
    "Add difficulty levels that choose questions by category or score.",
    "Download questions once from the Open Trivia Database and cache them in your file.",
    "Make a two-player mode that alternates turns.",
],
"data": r'''
Write 20–30 questions yourself, or fetch some from the [Open Trivia Database](https://opentdb.com/)
and save them to your JSON file (the game itself should not need the network).
''',
"setup": r'''
```bash
python quiz.py
python -m unittest -v
```
''',
},
{
"kind": "project", "slug": "text-adventure-engine", "title": "Text Adventure Engine",
"tags": ["games", "object-oriented-design", "parsing"],
"brief": r'''
Build a small engine for text adventures: rooms, exits, items and simple puzzles described in a data
file, a command parser ("go north", "take lamp", "use key on door"), and saved games — then write a
short adventure with it.
''',
"uses": ["string-basics", "vowel-counter", "files-and-json", "bank-account", "shapes-inheritance", "unit-testing"],
"milestones": [
    "Model Room, Item and Player as classes; describe a three-room world in a JSON file.",
    "Write a parser that turns commands into (verb, object) pairs and rejects unknown verbs politely.",
    "Implement go, look, take, drop and inventory.",
    "Add locked doors and items that unlock them.",
    "Save and load the game state to a file; test the parser and the save format with unittest.",
],
"stretch": [
    "Add characters that respond to `talk` with a small dialogue tree.",
    "Load several adventures from a folder and let the player choose.",
    "Add a scoring system and an ending condition.",
],
"data": r'''
You write the world file yourself; keep it small at first (three rooms, two items, one puzzle).
''',
"setup": r'''
```bash
python adventure.py worlds/castle.json
```
''',
},
]
