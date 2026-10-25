"""Ungraded project ideas for the NumPy topic (library revision, Phase 6)."""

PROBLEMS = [
{
"kind": "project", "slug": "numpy-photo-filters", "title": "Photo Filters with NumPy",
"tags": ["images", "arrays", "broadcasting"],
"brief": r'''
Build a small photo-filter program using only NumPy array operations: greyscale, brightness and
contrast, blur, edge detection and a vignette — applied to your own photos.
''',
"uses": ["array-info", "vectorized-math", "slicing-subgrid", "axis-aggregations", "broadcast-center", "moving-average"],
"milestones": [
    "Load a photo into a NumPy array (with Pillow) and print its shape and dtype.",
    "Write greyscale, brightness and contrast filters with vectorised arithmetic, clipping to 0–255.",
    "Write a box blur by averaging shifted copies of the image.",
    "Write a simple edge filter from differences between neighbouring pixels.",
    "Add a vignette with a broadcast distance-from-centre mask, and save the results side by side.",
],
"stretch": [
    "Write a sepia filter as a 3×3 colour matrix applied with matrix multiplication.",
    "Compare your blur's speed with a Python double loop.",
    "Build a command-line tool that chains filters: `python filters.py in.jpg out.jpg grey blur vignette`.",
],
"data": r'''
Your own photos. [Pillow](https://pillow.readthedocs.io/en/stable/) only loads and saves the files;
the filters themselves use NumPy ([broadcasting guide](https://numpy.org/doc/stable/user/basics.broadcasting.html)).
''',
"setup": r'''
```bash
pip install numpy pillow
python filters.py photo.jpg
```
''',
},
]
