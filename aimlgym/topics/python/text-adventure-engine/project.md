# PY-P3 · Project idea: Text Adventure Engine

**Topic:** Python · ungraded

## Brief

Build a small engine for text adventures: rooms, exits, items and simple puzzles described in a data
file, a command parser ("go north", "take lamp", "use key on door"), and saved games — then write a
short adventure with it.

## You will use

- PY-06 Strings: Indexing, Slicing and Methods
- PY-13 Vowel Counter
- PY-23 Files, CSV and JSON
- PY-25 Classes: A Bank Account
- PY-26 Inheritance, Special Methods and Dataclasses
- PY-27 Writing Unit Tests

## Milestones

1. Model Room, Item and Player as classes; describe a three-room world in a JSON file.
2. Write a parser that turns commands into (verb, object) pairs and rejects unknown verbs politely.
3. Implement go, look, take, drop and inventory.
4. Add locked doors and items that unlock them.
5. Save and load the game state to a file; test the parser and the save format with unittest.

## Stretch goals

- Add characters that respond to `talk` with a small dialogue tree.
- Load several adventures from a folder and let the player choose.
- Add a scoring system and an ending condition.

## Data

You write the world file yourself; keep it small at first (three rooms, two items, one puzzle).

## Run it yourself

```bash
python adventure.py worlds/castle.json
```
