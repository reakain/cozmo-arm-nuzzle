#!/usr/bin/env python
# From https://docs.opencv.org/master/da/d22/tutorial_py_canny.html
# Test image from image taken for Lecture 5.1
# Test Canny edge detection from OpenCV
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('test.jpg',0)
edges = cv.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()