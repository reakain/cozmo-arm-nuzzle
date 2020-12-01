import numpy as np
    2 import cv2
    3 import glob
    4 
    5 # termination criteria
    6 criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    7 
    8 # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    9 objp = np.zeros((6*7,3), np.float32)
   10 objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
   11 
   12 # Arrays to store object points and image points from all the images.
   13 objpoints = [] # 3d point in real world space
   14 imgpoints = [] # 2d points in image plane.
   15 
   16 images = glob.glob('*.jpg')
   17 
   18 for fname in images:
   19     img = cv2.imread(fname)
   20     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
   21 
   22     # Find the chess board corners
   23     ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
   24 
   25     # If found, add object points, image points (after refining them)
   26     if ret == True:
   27         objpoints.append(objp)
   28 
   29         cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
   30         imgpoints.append(corners)
   31 
   32         # Draw and display the corners
   33         cv2.drawChessboardCorners(img, (7,6), corners2,ret)
   34         cv2.imshow('img',img)
   35         cv2.waitKey(500)
   36 
   37 cv2.destroyAllWindows()