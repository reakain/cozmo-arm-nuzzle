#!/usr/bin/env python
import cv2
import pycozmo
import numpy as np
from yolo import YOLO

class CameraSensor:
    def __init__(self, cli, target_name_file):
        #self.yolo = YOLO("./yolo-coco/coco.names","./yolo-coco/yolov3.weights",
        self.yolo = YOLO(target_name_file,"./yolo-coco/yolov3.weights",
        "./yolo-coco/yolov3.cfg",0.7,0.3)
        self.last_im = np.zeros((320,240,3), np.uint8)
        self.updated = False
        self.cli = cli
        self.cli.add_handler(pycozmo.event.EvtNewRawCameraImage, self.on_camera_image)
        #self.target = target
        self.target = []


    def on_camera_image(self, cli, new_im):
        """ Handle new images, coming from the robot. """
        del cli

        # from: https://stackoverflow.com/a/14140796
        open_cv_image = np.array(new_im) 
        # Convert RGB to BGR 
        self.last_im = open_cv_image[:, :, ::-1].copy()

        self.updated = True

    def find_target(self):
        if self.updated:
            # Get last image.
            self.updated = False
            
            # YOLO, returns [x, y, width, height, confidence]
            self.target = self.yolo.analyze_image(self.last_im.copy())

            # if target has coordinates
            if self.target:
                print("Person found!")
                return True
            
            # if target has None
            else:
                print("Person not found")
                return False
        
        else:
            return False


    def get_offset(self):
        # simple offset from center of ID'd object and
        # half the width of the window (hard-coded)

        if self.target:
            x = self.target[0]
            offset = x - 320 / 2

            return offset

        # this shouldn't ever be needed, but just in case
        return 0
