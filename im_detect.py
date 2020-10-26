#!/usr/bin/env python

import cv2 as cv

class FrameAnalysis:
    def __init__(self,  threshold1 = 100, threshold2 = 200):
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def new_image(self, cli, image):
        del cli
        self.image = image
        self.find_edges()

    def find_edges(self):
        # Canny edge detection with threshold settings to start...
        self.edges = cv.Canny(self.image,self.threshold1,self.threshold2)
        return self.edges
