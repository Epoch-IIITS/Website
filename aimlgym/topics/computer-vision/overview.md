# Computer Vision

**You will be able to:** Treat images as arrays, then process them with OpenCV (colour spaces, transforms, thresholds, histograms, edges, resizing, contours, connected components), train a small PyTorch CNN with augmentation, and post-process detections with IoU and NMS.

**Topic prerequisites:** Deep Learning

Images are arrays of numbers. After image dtypes and colour-to-grey conversion, OpenCV takes over:
BGR order and indexing, flips, rotations and affine warps, thresholding with Otsu's method,
histograms and equalisation, 2D filtering, Sobel and Canny edges, PSNR, resizing, contours and
bounding boxes. With PyTorch you use pooling layers and a convolution layer, train a small CNN and
add data augmentation; the topic ends with IoU, non-maximum suppression and connected components.

**Packages:** `numpy`, `opencv-python-headless` and `torch`. Images are small synthetic arrays
defined in the tests. The NumPy versions of the library steps follow them as **optional deep
dives**. **Project ideas:** a document scanner, a shape and colour sorter, and an object counter.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | CV-01 | [Images as Arrays](image-arrays/problem.md) | beginner | DL-24 |
| 2 | CV-02 | [RGB to Grayscale](rgb-to-gray/problem.md) | beginner | CV-01 |
| 3 | CV-03 | [OpenCV Basics: BGR, dtypes and Indexing](cv-opencv-basics/problem.md) | beginner | CV-02 |
| 4 | CV-04 | [Flips, Rotations and Affine Warps](cv-geometric-transforms/problem.md) | beginner | CV-03 |
| 5 | CV-05 | [Flip and Rotate (optional deep dive)](flip-rotate/problem.md) | beginner | CV-01 |
| 6 | CV-06 | [Thresholding and Otsu's Method](cv-threshold-otsu/problem.md) | beginner | CV-04 |
| 7 | CV-07 | [Binary Thresholding (optional deep dive)](threshold-binary/problem.md) | beginner | CV-02 |
| 8 | CV-08 | [Histograms and Equalisation](cv-histograms/problem.md) | beginner | CV-06 |
| 9 | CV-09 | [Intensity Histogram (optional deep dive)](intensity-histogram/problem.md) | beginner | CV-02, ST-04 |
| 10 | CV-10 | [2D Filtering (Blur)](conv2d-filter/problem.md) | intermediate | CV-02, DL-24 |
| 11 | CV-11 | [Edges with Sobel and Canny](cv-sobel-canny/problem.md) | intermediate | CV-10, CV-08 |
| 12 | CV-12 | [Sobel Edge Magnitude (optional deep dive)](sobel-edges/problem.md) | intermediate | CV-10 |
| 13 | CV-13 | [Pooling with nn.MaxPool2d and nn.AvgPool2d](cv-pooling-torch/problem.md) | intermediate | CV-11, DL-24 |
| 14 | CV-14 | [2D Max Pooling (optional deep dive)](max-pool-2d/problem.md) | intermediate | CV-10 |
| 15 | CV-15 | [A Convolution Layer with Channels](conv2d-layer/problem.md) | intermediate | CV-13, CV-10 |
| 16 | CV-16 | [Image Quality: MSE and PSNR](cv-psnr/problem.md) | intermediate | CV-15, CV-13 |
| 17 | CV-17 | [MSE and PSNR by Hand (optional deep dive)](psnr/problem.md) | intermediate | CV-01, ML-02 |
| 18 | CV-18 | [Resizing with cv2.resize](cv-resize/problem.md) | advanced | CV-16 |
| 19 | CV-19 | [Bilinear Resize (optional deep dive)](bilinear-resize/problem.md) | advanced | CV-05, NP-09 |
| 20 | CV-20 | [Contours and Bounding Boxes](cv-contours/problem.md) | advanced | CV-18 |
| 21 | CV-P1 | [Project idea: Document Scanner](document-scanner/project.md) | ungraded | CV-03, CV-04, CV-06, CV-11, CV-20 |
| 22 | CV-21 | [A Small CNN in PyTorch](cv-small-cnn/problem.md) | advanced | CV-20, DL-18 |
| 23 | CV-22 | [Data Augmentation](cv-augmentation/problem.md) | advanced | CV-21 |
| 24 | CV-P2 | [Project idea: Shape and Colour Sorter](shape-sorter/project.md) | ungraded | CV-03, CV-18, CV-21, CV-22, DL-18 |
| 25 | CV-23 | [Intersection over Union](iou/problem.md) | advanced | CV-01, NP-07 |
| 26 | CV-24 | [Non-Maximum Suppression](non-max-suppression/problem.md) | advanced | CV-23 |
| 27 | CV-25 | [Connected Components with OpenCV](cv-connected-components/problem.md) | advanced | CV-24 |
| 28 | CV-26 | [Connected Components Labeling by Hand (optional deep dive)](connected-components/problem.md) | advanced | CV-07 |
| 29 | CV-P3 | [Project idea: Simple Object Counter](object-counter/project.md) | ungraded | CV-06, CV-20, CV-23, CV-24, CV-25 |
