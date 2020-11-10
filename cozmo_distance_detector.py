#!/usr/bin/env python

# example Cozmo video feed
# taken from
# https://github.com/zayfod/pycozmo/blob/master/examples/video.py
# example pygame from https://www.geeksforgeeks.org/python-display-images-with-pygame/

import time

import pycozmo
import pygame

import numpy as np
import cv2 as cv

import imutils




# Last image, received from the robot.
last_im = np.zeros((320,240,3), np.uint8)
updated = False


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    del cli

    global last_im, updated
    # from: https://stackoverflow.com/a/14140796
    open_cv_image = np.array(new_im) 
    # Convert RGB to BGR 
    last_im = open_cv_image[:, :, ::-1].copy()

    updated = True

# From: https://stackoverflow.com/a/64183410
def cv2ImageToSurface(cv2Image):
    if cv2Image.dtype.name == 'uint16':
        cv2Image = (cv2Image / 256).astype('uint8')
    size = cv2Image.shape[1::-1]
    if len(cv2Image.shape) == 2:
        cv2Image = np.repeat(cv2Image.reshape(size[1], size[0], 1), 3, axis = 2)
        format = 'RGB'
    else:
        format = 'RGBA' if cv2Image.shape[2] == 4 else 'RGB'
        cv2Image[:, :, [0, 2]] = cv2Image[:, :, [2, 0]]
    surface = pygame.image.frombuffer(cv2Image.flatten(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()

def pycozmo_program(cli: pycozmo.client.Client):

    global last_im, updated

    # activate the pygame library . 
    # initiate pygame and give permission 
    # to use pygame's functionality. 
    pygame.init() 
    
    # define the RGB value 
    # for white colour 
    white = (255, 255, 255) 
    
    # assigning values to X and Y variable 
    X = 320
    Y = 720
    
    # create the display surface object 
    # of specific dimension..e(X, Y). 
    display_surface = pygame.display.set_mode((X, Y )) 
    
    # set the pygame window name 
    pygame.display.set_caption('Image') 
    
    # Set to look straight ahead
    cli.set_head_angle(0)

    pkt = pycozmo.protocol_encoder.EnableCamera()
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.EnableColorImages(enable=True)
    cli.conn.send(pkt)

    # Wait for image to stabilize.
    time.sleep(2.0)

    # Register to receive new camera images.
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)

    # MANUAL DISTANCE CALIBRATIONS
    calibrated = False
    # calibration: distance from cozmo to object (inches)
    KNOWN_DISTANCE = 12.0
    # calibration: width of your object of interest (inches)
    KNOWN_WIDTH = 1.0

    fgbg = cv.createBackgroundSubtractorMOG2(
    history=10,
    varThreshold=2,
    detectShadows=False)

    while True:

        if updated:

            # Get last image.
            im = last_im
            im2 = im.copy()
            gray = cv.cvtColor(im2, cv.COLOR_BGR2GRAY)
            updated = False

            # filtering https://www.sicara.ai/blog/2019-03-12-edge-detection-in-opencv
            filtered = cv.bilateralFilter(gray, 7, 50, 50)
            foreground = fgbg.apply(filtered)

            kernel = np.ones((50,50),np.uint8)
            foreground = cv.morphologyEx(foreground, cv.MORPH_CLOSE, kernel)

            # edge detection
            edges = cv.Canny(filtered,100,200)

            # Crop off moving area
            cropped = (foreground //255) * edges

            # DISTANCE DETECTION
            # referenced https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
            # create a list of contours to work with
            boxContours = cv.findContours(edges.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            boxContours = imutils.grab_contours(boxContours)

            # try finding the contour with the largest area
            try:
                # using the boxContours list, finds biggest in terms of area, fits rect to that area
                target = max(boxContours, key = cv.contourArea)
                targetBox = cv.minAreaRect(target)

                # get a calibrated focal length for cozmo camera, first pass only
                if calibrated == False:
                    focalLength = (targetBox[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
                    calibrated = True

                # find distance to object based on:
                # manually set KNOWN_WIDTH (earlier in code, starting contour width)
                # focalLength (calculated on the first pass, scale factor)
                # targetBox[1][0], which is this frame's contour width
                # scale factor * (starting width / current width)
                currentDistance = focalLength * (KNOWN_WIDTH / targetBox[1][0])

                # draw bounding box
                box = cv.boxPoints(targetBox)
                box = np.int0(box)
                boxImg = cv.drawContours(im2, [box], -1, (255, 255, 150), 2)

                # add text below the bounding box
                cv.putText(boxImg, "%.2fin" % (currentDistance),
                           (boxImg.shape[1] - 200, boxImg.shape[0] - 20),
                           cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 150), 2)

            # if no contours are available
            except ValueError:
                print("No object detected")

            # completely fill the surface object 
            # with white colour 
            display_surface.fill(white) 
        
            # copying the image surface object 
            # to the display surface object at 
            # (0, 0) coordinate. 
            display_surface.blit(cv2ImageToSurface(im), (0, 0))
            display_surface.blit(cv2ImageToSurface(cropped), (0,240))

            # draw the distance detecting image
            display_surface.blit(cv2ImageToSurface(boxImg), (0, 480)) 

            # Draws the surface object to the screen.   
            pygame.display.update()  

        # iterate over the list of Event objects 
        # that was returned by pygame.event.get() method. 
        for event in pygame.event.get() : 
    
            # if event object type is QUIT 
            # then quitting the pygame 
            # and program both. 
            if event.type == pygame.QUIT : 
    
                # deactivates the pygame library 
                pygame.quit() 
    
                # quit the program. 
                quit()  

        # Run with 25 FPS.
        time.sleep(1 / 25)


pycozmo.run_program(pycozmo_program, protocol_log_level="INFO", robot_log_level="DEBUG")
