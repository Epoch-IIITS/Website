# NP-P1 · Project idea: Photo Filters with NumPy

**Topic:** NumPy · ungraded

## Brief

Build a small photo-filter program using only NumPy array operations: greyscale, brightness and
contrast, blur, edge detection and a vignette — applied to your own photos.

## You will use

- NP-01 Create an Array and Inspect It
- NP-02 Vectorised Arithmetic and ufuncs
- NP-03 Slicing a Sub-grid
- NP-05 Aggregations Along Axes
- NP-07 Centering Columns with Broadcasting
- NP-14 Moving Average with cumsum

## Milestones

1. Load a photo into a NumPy array (with Pillow) and print its shape and dtype.
2. Write greyscale, brightness and contrast filters with vectorised arithmetic, clipping to 0–255.
3. Write a box blur by averaging shifted copies of the image.
4. Write a simple edge filter from differences between neighbouring pixels.
5. Add a vignette with a broadcast distance-from-centre mask, and save the results side by side.

## Stretch goals

- Write a sepia filter as a 3×3 colour matrix applied with matrix multiplication.
- Compare your blur's speed with a Python double loop.
- Build a command-line tool that chains filters: `python filters.py in.jpg out.jpg grey blur vignette`.

## Data

Your own photos. [Pillow](https://pillow.readthedocs.io/en/stable/) only loads and saves the files;
the filters themselves use NumPy ([broadcasting guide](https://numpy.org/doc/stable/user/basics.broadcasting.html)).

## Run it yourself

```bash
pip install numpy pillow
python filters.py photo.jpg
```
