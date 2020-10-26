#!/usr/bin/env python

import cv2 as cv
import pycozmo
from im_detect import FrameAnalysis

# Setup pycozmo and cozmo

# Get frame from cozmo
frame = FrameAnalysis(img_cozmo)

# Analyze frame and get edges
result = frame.find_edges()

# Ouput frame
plt.subplot(121),plt.imshow(frame.image,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(frame.edges,cmap = 'gray')
plt.title('Edge'), plt.xticks([]), plt.yticks([])

plt.show()