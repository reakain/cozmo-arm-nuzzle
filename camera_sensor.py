#!/usr/bin/env python
import cv2
import pycozmo
import numpy as np
from yolo import YOLO

class CameraSensor:
    def __init__(self, cli, target_name_file):
        #self.yolo = YOLO("./yolo-coco/coco.names","./yolo-coco/yolov3.weights",
        self.yolo = YOLO(target_name_file,"./yolo-coco/yolov3.weights",
        "./yolo-coco/yolov3.cfg",0.5,0.3)
        self.last_im = np.zeros((320,240,3), np.uint8)
        self.updated = False
        self.cli = cli
        self.cli.add_handler(pycozmo.event.EvtNewRawCameraImage, self.on_camera_image)
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
        if self.updated:
            # Get last image.
            self.updated = False
            # YOLO
            detect_im = yolo.analyze_image(last_im.copy())

            # TODO: understand the yolo enough to know if it actually found our target in the image...
            # If the target is in the image...
            # if ()
            #     return True
            # else:
            #     return False

        else:
            return False


    def get_offset(self):
        # TODO: calculate some kind of offset for the target from center of image
        # Do the stuff to get the offset from center 
        # Positive => right of center, negative => left of center
        return 1.0