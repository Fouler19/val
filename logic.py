import cv2
import numpy as np
from math import sqrt, ceil, floor

def create_collage(image_paths):
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        images.append(image)

    num_images = len(images)
    num_cols = floor(sqrt(num_images))
    num_rows = ceil(num_images / num_cols)

    collage = np.zeros((num_rows * images[0].shape[0], num_cols * images[0].shape[1], 3), dtype=np.uint8)

    for i, image in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        collage[row*image.shape[0]:(row+1)*image.shape[0], col*image.shape[1]:(col+1)*image.shape[1], :] = image

    return collage
