# CV-P3 · Project idea: Simple Object Counter

**Topic:** Computer Vision · ungraded

## Brief

Count objects in images — coins on a table or cell nuclei under a microscope — and report their
sizes. Compare your counts with the ground truth and find out which images are hard and why.

## You will use

- CV-06 Thresholding and Otsu's Method
- CV-20 Contours and Bounding Boxes
- CV-23 Intersection over Union
- CV-24 Non-Maximum Suppression
- CV-25 Connected Components with OpenCV

## Milestones

1. Load an image, convert to greyscale, blur and threshold with Otsu.
2. Clean the mask with morphological opening (cv2.morphologyEx) to remove speckles.
3. Count objects with connectedComponentsWithStats and filter by area.
4. Draw numbered bounding boxes and save an annotated image.
5. On a labelled dataset, compare counts with the ground truth and report the mean absolute error.

## Stretch goals

- Separate touching objects with the distance transform and watershed.
- Match predicted boxes to ground-truth boxes with IoU and report precision and recall.
- Measure object sizes in millimetres using a reference object of known size.

## Data

* [BBBC039](https://bbbc.broadinstitute.org/BBBC039): fluorescent nuclei images with ground-truth
  masks (Broad Bioimage Benchmark Collection).
* A coins image ships with scikit-image: `skimage.data.coins()`
  ([data module](https://scikit-image.org/docs/stable/api/skimage.data.html)), or photograph coins yourself.

## Run it yourself

```bash
pip install opencv-python numpy scikit-image
python count.py image.png
```
