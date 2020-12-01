#import statements
import math
import numpy as np
import scipy.optimize
import cv2
# Load captured image.
image_bgr = cv2.imread("box_location_input.png", cv2.IMREAD_COLOR)
# Convert to HSV color space.
image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
# Mask box
YELLOW = {"lower":(25, 100, 50),"upper":(35, 255, 200)}
GREEN = {"lower":(64, 96, 64),"upper": (90, 255, 200)}
mask = cv2.inRange(image_hsv, YELLOW["lower"],YELLOW["upper"])

mask = cv2.morphologyEx(
    mask, cv2.MORPH_OPEN,
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4)))
mask = cv2.morphologyEx(
    mask, cv2.MORPH_CLOSE,
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (16, 16)))
contours = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
contours = sorted(contours, key = cv2.contourArea, reverse = True)
cv2.drawContours(image_bgr, contours, 0, (255, 255, 255), 3)
targetmask = np.zeros((image_bgr.shape[0], image_bgr.shape[1], 1), np.uint8)
cv2.drawContours(targetmask, contours, 0, (255), -1)


# box_size = [0.150,0.100,0.075]
def boxcorners(box_size):
    # Define box corners in box coordinate system.
    half_size_x = box_size[0] / 2.0
    half_size_y = box_size[1] / 2.0
    half_size_z = box_size[2] / 2.0
    corners = np.array(
        [[-half_size_x, -half_size_y, -half_size_z],
         [+half_size_x, -half_size_y, -half_size_z],
         [-half_size_x, +half_size_y, -half_size_z],
         [+half_size_x, +half_size_y, -half_size_z],
         [-half_size_x, -half_size_y, +half_size_z],
         [+half_size_x, -half_size_y, +half_size_z],
         [-half_size_x, +half_size_y, +half_size_z],
         [+half_size_x, +half_size_y, +half_size_z]],
        'float64')
    return corners


def drawBoxOnImage(rotation_vector, translation_vector,camera_matrix,dist_coeffs, image):
    # Draw the box on a given (color) image, given the rotation and
    # translation vector.
    box_size = [0.150,0.100,0.075]
    corners = boxcorners(box_size)
    # Project box corners to image plane.
    pts = cv2.projectPoints(
        corners, rotation_vector, translation_vector,
        camera_matrix, dist_coeffs)[0]
    # Draw box on image
    projected_image = image.copy()
    cv2.polylines(
        projected_image,
        np.array([[pts[1][0], pts[0][0], pts[2][0], pts[3][0]],
                    [pts[0][0], pts[1][0], pts[5][0], pts[4][0]],
                    [pts[1][0], pts[3][0], pts[7][0], pts[5][0]],
                    [pts[3][0], pts[2][0], pts[6][0], pts[7][0]],
                    [pts[2][0], pts[0][0], pts[4][0], pts[6][0]],
                    [pts[4][0], pts[5][0], pts[7][0], pts[6][0]]], 'int32'),
        True, (0, 255, 0), 3)
    return projected_image

def projectBox(rotation_vector, translation_vector,camera_matrix,dist_coeffs, image):
    # Project the box to create a mask, given the rotation and translation
    # vector. This function is used in the optimisation loop to compare the
    # projection using the rotation and translation vectors to the original
    # image.
    box_size = [0.170,0.115,0.075]
    corners = boxcorners(box_size)

    pts = cv2.projectPoints(
        corners, rotation_vector, translation_vector,
        camera_matrix, dist_coeffs)[0]
    # Draw box on image
    projected_image = np.zeros((image.shape[0], image.shape[1], 1),
        np.uint8)
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[1][0], pts[0][0], pts[2][0], pts[3][0]], 'int32'),
        (255))
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[0][0], pts[1][0], pts[5][0], pts[4][0]], 'int32'),
        (255))
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[1][0], pts[3][0], pts[7][0], pts[5][0]], 'int32'),
        (255))
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[3][0], pts[2][0], pts[6][0], pts[7][0]], 'int32'),
        (255))
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[2][0], pts[0][0], pts[4][0], pts[6][0]], 'int32'),
        (255))
    cv2.fillConvexPoly(
        projected_image,
        np.array([pts[4][0], pts[5][0], pts[7][0], pts[6][0]], 'int32'),
        (255))
    # Return projected image.
    return projected_image

image_pixels = float(cv2.countNonZero(targetmask))
def objectiveFunction(x):
    # The objective function for the optimisation. Split the x input vector
    # in a rotation and a translation vector, project the box and measure
    # the difference between the projection and the given mask (COG
    # distance, total pixel count (surface) and non-overlapping pixel count
    # (shape difference).
 
    # Get rotation and translation vectors and project perfect box.
    rotation_vector = np.array([x[0], x[1], x[2]], 'float64')
    translation_vector = np.array([x[3], x[4], x[5]], 'float64')
    projected = projectBox(rotation_vector, translation_vector,camera_matrix,dist_coeffs,
            np.zeros(targetmask.shape, np.uint8))
 
    # Calculate size difference (pixel count).
    projected_pixels = float(cv2.countNonZero(projected))
    pixel_count_difference = \
        ((projected_pixels - image_pixels) / image_pixels) ** 2
 
    # Calculate overlap difference (pixel count).
    non_overlap = cv2.bitwise_xor(targetmask, projected)
    non_overlap_pixels = float(cv2.countNonZero(non_overlap))
    overlap_difference = non_overlap_pixels / self.image_pixels
 
    # Return penalty.
    return pixel_count_difference + overlap_difference 

result = scipy.optimize.minimize(
        objectiveFunction,np.hstack([rotation, translation]),
        method='Nelder-Mead')
x = result.x