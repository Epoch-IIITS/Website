# CV-P2 · Project idea: Shape and Colour Sorter

**Topic:** Computer Vision · ungraded

## Brief

Train a CNN that sorts photos of simple objects — for example coloured blocks, coins or bottle caps —
into classes, and test it with your webcam or new photos taken in different light.

## You will use

- CV-03 OpenCV Basics: BGR, dtypes and Indexing
- CV-18 Resizing with cv2.resize
- CV-21 A Small CNN in PyTorch
- CV-22 Data Augmentation
- DL-18 A Full Training Loop

## Milestones

1. Collect 30–50 photos per class (or generate synthetic shapes) and resize them to 64×64.
2. Split into train, validation and test folders and write a Dataset that loads them with OpenCV.
3. Train the small CNN, adapted to 3 colour channels and 64×64 inputs.
4. Add augmentation (flips, shifts, brightness) and compare validation accuracy with and without it.
5. Classify frames from a webcam with cv2.VideoCapture and show the predicted label on screen.

## Stretch goals

- Fine-tune a pretrained torchvision model (for example ResNet-18) and compare.
- Add a confidence threshold that answers 'unknown' for low-probability predictions.
- Export the model with TorchScript or ONNX.

## Data

Take your own photos with a phone or webcam. For a synthetic start, draw coloured circles, squares and
triangles with `cv2.circle`, `cv2.rectangle` and `cv2.fillPoly` at random positions and sizes.

## Run it yourself

```bash
pip install torch opencv-python numpy
python train_sorter.py data/
```
