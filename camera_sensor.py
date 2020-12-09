#!/usr/bin/env python
import cv2
import pycozmo
import pygame
import numpy as np
from yolo import YOLO

class CameraSensor:
    def __init__(self, cli, target_name = "person", target_name_file = "./yolo-coco/coco.names"):
        #self.yolo = YOLO("./yolo-coco/coco.names","./yolo-coco/yolov3.weights",
        self.yolo = YOLO(target_name_file,"./yolo-coco/yolov3.weights",
        "./yolo-coco/yolov3.cfg",0.7,0.3, target_name)
        self.last_im = np.zeros((320,240,3), np.uint8)
        self.updated = False
        self.target = None
        self.cli = cli
        self.cli.add_handler(pycozmo.event.EvtNewRawCameraImage, self.on_camera_image)
        #self.target = target
        

    def has_target(self):
        return self.target != None

    def on_camera_image(self, cli, new_im):
        """ Handle new images, coming from the robot. """
        del cli

        # from: https://stackoverflow.com/a/14140796
        open_cv_image = np.array(new_im) 
        # Convert RGB to BGR 
        self.last_im = open_cv_image[:, :, ::-1].copy()

        self.updated = True

    def find_target(self):
        # Get last image.
        #self.updated = False
        #if self.updated:
        # YOLO, returns [x, y, width, height, confidence]
        self.target = self.yolo.analyze_image(self.last_im.copy())

        # if target has coordinates
        if self.target != None:
            #print("Person found!")
            return True
        
        # if target has None
        else:
            #print("Person not found")
            return False
        # if self.updated:
        #     # Get last image.
        #     self.updated = False
            
        #     # YOLO, returns [x, y, width, height, confidence]
        #     self.target = self.yolo.analyze_image(self.last_im.copy())

        #     # if target has coordinates
        #     if self.target:
        #         print("Person found!")
        #         return True
            
        #     # if target has None
        #     else:
        #         print("Person not found")
        #         return False
        
        # else:
        #     return False


    def get_offset(self):
        # simple offset from center of ID'd object and
        # half the width of the window (hard-coded)

        if self.target != None:
            x = self.target[0]
            offset = x - 320 / 2

            return offset

        # this shouldn't ever be needed, but just in case
        return 0

    def get_offset_dir(self,tolerance):
        offset = self.get_offset()
        if(offset < tolerance and offset > -tolerance):
            return 0
        return np.sign(offset)

    def get_output_img(self):
        image = self.last_im.copy()
        if self.updated:
            self.updated = False
            if(self.find_target()):
                # extract the bounding box coordinates
                (x, y) = (self.target[0], self.target[1])
                (w, h) = (self.target[2], self.target[3])

                # draw a bounding box rectangle and label on the image
                color = (255,0,0)
                cv2.rectangle(image, (x, y), (w, h), color, 2)

        return self.get_pygame_image(image)

    def get_pygame_image(self, cv2Image):
        #cv2Image = self.last_im.copy()
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
