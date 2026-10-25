# PY-P2 · Project idea: Quiz Game with High Scores

**Topic:** Python · ungraded

## Brief

Build a quiz game that loads questions from a file, asks them in random order, keeps score with time
bonuses, and stores a high-score table — with unit tests for the scoring rules.

## You will use

- PY-15 Importing the Standard Library
- PY-23 Files, CSV and JSON
- PY-25 Classes: A Bank Account
- PY-26 Inheritance, Special Methods and Dataclasses
- PY-27 Writing Unit Tests

## Milestones

1. Store questions (text, options, answer, category) in a JSON file and load them into Question objects.
2. Ask ten random questions, check answers and show the score.
3. Add a Player class and a high-score table saved to a file, keeping the top five.
4. Give multiple-choice and true/false questions their own subclasses with a shared check() method.
5. Write unittest tests for scoring, loading and the high-score table.

## Stretch goals

- Add difficulty levels that choose questions by category or score.
- Download questions once from the Open Trivia Database and cache them in your file.
- Make a two-player mode that alternates turns.

## Data

Write 20–30 questions yourself, or fetch some from the [Open Trivia Database](https://opentdb.com/)
and save them to your JSON file (the game itself should not need the network).

## Run it yourself

```bash
python quiz.py
python -m unittest -v
```
