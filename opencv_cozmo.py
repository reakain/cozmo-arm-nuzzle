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
last_im = None
updated = False


def on_camera_image(cli, new_im):
    """ Handle new images, coming from the robot. """
    del cli

    global last_im, updated
    last_im = new_im
    updated = True


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

    while True:

        if updated:

            # Get last image.
            im = last_im
            updated = False

            #img = cv.imread('test.jpg',0)
            edges = cv.Canny(im,100,200)

            # completely fill the surface object 
            # with white colour 
            display_surface.fill(white) 
        
            # copying the image surface object 
            # to the display surface object at 
            # (0, 0) coordinate. 
            display_surface.blit(im, (0, 0)) 
            display_surface.blit(edges, (0,240))
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
