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
    Y = 480
    
    # create the display surface object 
    # of specific dimension..e(X, Y). 
    display_surface = pygame.display.set_mode((X, Y )) 
    
    # set the pygame window name 
    pygame.display.set_caption('Image') 
    

    # Raise head.
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    pkt = pycozmo.protocol_encoder.EnableCamera()
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.EnableColorImages(enable=True)
    cli.conn.send(pkt)

    # Wait for image to stabilize.
    time.sleep(2.0)

    # Register to receive new camera images.
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)

    # Enable camera.
    #pkt = pycozmo.protocol_encoder.EnableCamera()
    #cli.conn.send(pkt)

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

            # convex hull from edge detection
            contours, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for c in contours:
                hull = cv.convexHull(c)
                cv.drawContours(im2, [hull], 0, (0, 255, 0), 2)

            # completely fill the surface object 
            # with white colour 
            display_surface.fill(white) 
        
            # copying the image surface object 
            # to the display surface object at 
            # (0, 0) coordinate. 
            display_surface.blit(cv2ImageToSurface(im), (0, 0)) 
            display_surface.blit(cv2ImageToSurface(cropped), (0,240))
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
