#!/usr/bin/env python
import cv2
import pycozmo
import numpy as np
from yolo import YOLO

class CameraSensor:
    def __init__(self, cli, target_name):
        #self.yolo = YOLO("./yolo-coco/coco.names","./yolo-coco/yolov3.weights",
        self.yolo = YOLO(target_name,"./yolo-coco/yolov3.weights",
        "./yolo-coco/yolov3.cfg",0.5,0.3)
        self.last_im = np.zeros((320,240,3), np.uint8)
        self.updated = False
        self.cli = cli
        self.cli.add_handler(pycozmo.event.EvtNewRawCameraImage, camera.on_camera_image)
        #self.target = target


    def on_camera_image(self, cli, new_im):
    """ Handle new images, coming from the robot. """
        del cli

        # from: https://stackoverflow.com/a/14140796
        open_cv_image = np.array(new_im) 
        # Convert RGB to BGR 
        self.last_im = open_cv_image[:, :, ::-1].copy()

        self.updated = True

    def find_target(self):
        if updated:
            # Get last image.
            updated = False
            # YOLO
            detect_im = yolo.analyze_image(last_im.copy())

            # If the target is in the image...
            # if ()
            #     return True
            # else:
            #     return False

        else:
            return False


    def get_offset(self):
        # Do the stuff to get the offset from center 
        return 1.0
