r"""Reference solution for PY-07 Conditionals: Letter Grades.

Invalid scores are handled first so that later branches only see 0–100. The bands are tested from
highest to lowest, so each `elif` implicitly knows the score is below the previous threshold.
The second decision reuses a chained comparison for validity.
"""
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
