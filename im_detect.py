#!/usr/bin/env python

import cv2 as cv

class FrameAnalysis:
    def __init__(self, image):
        self.image = image

    def find_edges(self, threshold1 = 100, threshold2 = 200):
        # Canny edge detection with threshold settings to start...
        self.edges = cv.Canny(img,threshold1,threshold2)
        return self.edges
