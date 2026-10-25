# CV-P1 · Project idea: Document Scanner

**Topic:** Computer Vision · ungraded

## Brief

Turn a phone photo of a page lying on a desk into a flat, black-and-white scan: find the page,
straighten it, and clean up the lighting — what scanner apps do.

## You will use

- CV-03 OpenCV Basics: BGR, dtypes and Indexing
- CV-04 Flips, Rotations and Affine Warps
- CV-06 Thresholding and Otsu's Method
- CV-11 Edges with Sobel and Canny
- CV-20 Contours and Bounding Boxes

## Milestones

1. Load a photo, resize it to about 800 pixels wide and convert it to greyscale.
2. Blur, run Canny and find the largest contour.
3. Approximate the contour with cv2.approxPolyDP until it has four corners; draw them on the photo.
4. Order the corners and warp the page flat with cv2.getPerspectiveTransform and cv2.warpPerspective.
5. Clean the result with adaptive or Otsu thresholding and save it as a PNG.

## Stretch goals

- Handle photos where the page is not the largest object.
- Process a folder of photos into one multi-page PDF.
- Add a fallback that lets the user click the four corners when detection fails.

## Data

Photograph a few printed pages on a contrasting desk with your phone (different angles and lighting).
No dataset download is needed.

## Run it yourself

```bash
pip install opencv-python numpy
python scan.py photo.jpg scanned.png
```
