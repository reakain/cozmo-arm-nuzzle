#!/usr/bin/env python

# example Cozmo video feed
# taken from
# https://github.com/zayfod/pycozmo/blob/master/examples/video.py
# example pygame from https://www.geeksforgeeks.org/python-display-images-with-pygame/

import time

import pycozmo
import pygame

import numpy as np
import cv2

import imutils

from yolo import YOLO

# ground, yolo, edge
analysis_method = "yolo"


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

# Taken from https://github.com/BigFace83/BFRMR1
def CheckGround(img):

    StepSize = 8
    EdgeArray = []

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #convert img to grayscale and store result in imgGray
    imgGray = cv2.bilateralFilter(imgGray,9,30,30) #blur the image slightly to remove noise             
    imgEdge = cv2.Canny(imgGray, 50, 100)             #edge detection
    
    imagewidth = imgEdge.shape[1] - 1
    imageheight = imgEdge.shape[0] - 1
    
    for j in range (0,imagewidth,StepSize):    #for the width of image array
        for i in range(imageheight-5,0,-1):    #step through every pixel in height of array from bottom to top
                                               #Ignore first couple of pixels as may trigger due to undistort
            if imgEdge.item(i,j) == 255:       #check to see if the pixel is white which indicates an edge has been found
                EdgeArray.append((j,i))        #if it is, add x,y coordinates to ObstacleArray
                break                          #if white pixel is found, skip rest of pixels in column
        else:                                  #no white pixel found
            EdgeArray.append((j,0))            #if nothing found, assume no obstacle. Set pixel position way off the screen to indicate
                                               #no obstacle detected
            
    
    for x in range (len(EdgeArray)-1):      #draw lines between points in ObstacleArray 
        cv2.line(img, EdgeArray[x], EdgeArray[x+1],(0,255,0),1) 
    for x in range (len(EdgeArray)):        #draw lines from bottom of the screen to points in ObstacleArray
        cv2.line(img, (x*StepSize,imageheight), EdgeArray[x],(0,255,0),1)

    return img,EdgeArray


    #if DisplayImage is True:
    #    cv2.imshow("camera", img)
    #    cv2.waitKey(10)


def pycozmo_program(cli: pycozmo.client.Client):

    global last_im, updated, analysis_method

    if(analysis_method == "yolo"):
        yolo = YOLO("./yolo-coco/coco.names","./yolo-coco/yolov3.weights",
    "./yolo-coco/yolov3.cfg",0.5,0.3)

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
    cli.set_head_angle(0)#angle)

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

    # MANUAL DISTANCE CALIBRATIONS
    calibrated = False
    # calibration: distance from cozmo to object (inches)
    KNOWN_DISTANCE = 12.0
    # calibration: width of your object of interest (inches)
    KNOWN_WIDTH = 1.0


    fgbg = cv2.createBackgroundSubtractorMOG2(
    history=10,
    varThreshold=2,
    detectShadows=False)

    while True:

        if updated:

            # Get last image.
            im = last_im
            updated = False

            # completely fill the surface object 
            # with white colour 
            display_surface.fill(white) 

            if(analysis_method == "yolo"):
                grnd, edges = CheckGround(last_im.copy())
                detect_im = yolo.analyze_image(grnd.copy())
                im_both = np.vstack((last_im, detect_im))
            
            elif(analysis_method == "ground"):
                grnd, edges = CheckGround(last_im.copy())
                im_both = np.vstack((last_im, grnd))

                im2 = last_im.copy()
                gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

                # filtering https://www.sicara.ai/blog/2019-03-12-edge-detection-in-opencv
                filtered = cv2.bilateralFilter(gray, 7, 50, 50)
                foreground = fgbg.apply(filtered)

                kernel = np.ones((50,50),np.uint8)
                foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, kernel)

                # edge detection
                edges = cv2.Canny(filtered,100,200)

                # Crop off moving area
                cropped = (foreground //255) * edges

                # convex hull from edge detection
                contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    hull = cv2.convexHull(c)
                    cv2.drawContours(im2, [hull], 0, (0, 255, 0), 2)
                
                im_both = np.vstack((last_im, im2))

                # DISTANCE DETECTION
                # referenced https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
                # create a list of contours to work with
                boxContours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                boxContours = imutils.grab_contours(boxContours)

                # try finding the contour with the largest area
                try:
                    # using the boxContours list, finds biggest in terms of area, fits rect to that area
                    target = max(boxContours, key = cv2.contourArea)
                    targetBox = cv2.minAreaRect(target)

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
                    box = cv2.boxPoints(targetBox)
                    box = np.int0(box)
                    boxImg = cv2.drawContours(grnd.copy(), [box], -1, (255, 255, 150), 2)

                    # add text below the bounding box
                    cv2.putText(boxImg, "%.2fin" % (currentDistance),
                            (boxImg.shape[1] - 200, boxImg.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 150), 2)

                    im_both = np.vstack((last_im, boxImg))

                # if no contours are available
                except ValueError:
                    print("No object detected")
            
        
            # copying the image surface object 
            # to the display surface object at 
            # (0, 0) coordinate. 
            display_surface.blit(cv2ImageToSurface(im_both), (0, 0)) 
            #display_surface.blit(cv2ImageToSurface(grnd), (0,240))
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
