r"""Reference solution for PY-06 Strings: Indexing, Slicing and Methods.

Indexing picks single characters, slicing with omitted bounds handles short words safely, and a
negative step reverses the string. `upper()` returns a new string and `in` returns a bool.
"""
word = input().strip()
print(f"Length: {len(word)}")
print(f"First: {word[0]}")
print(f"Last: {word[-1]}")
print(f"First three: {word[:3]}")
print(f"Reversed: {word[::-1]}")
print(f"Upper: {word.upper()}")
print(f"Contains 'th': {'th' in word}")
