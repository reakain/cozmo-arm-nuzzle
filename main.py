#!/usr/bin/env python

import time

import pycozmo
import pygame

import numpy as np
import cv2

from yolo import YOLO
from camera_sensor import CameraSensor
from expressions import Expressions
from cozmo_controller import CozmoController

def main():
    with pycozmo.connect() as cli:
        # Setup camera
        cli.enable_camera(enable=True, color=True)
        camera = CameraSensor(cli,'person')
        #cli.add_handler(pycozmo.event.EvtNewRawCameraImage, camera.on_camera_image)

        # Setup Expressions
        cli.load_anims()
        emote = Expressions(cli)

        # Setup controller
        controller = CozmoController(cli,camera)

        # Drive off charger
        controller.drive_off_charger()

        # Check for target
        if(not camera.find_target()):
            # If no target, make a sad face and quit
            emote.act_sad()
            break

        # Center the target
        controller.center_target()
        # Be happy at target once centered
        emote.act_happy()
        # Drive to the target while keeping it centered
        if(controller.drive_to_target()):
            # If made it to the target...
            emote.act_happy()
        else:
            # Else be sad and quit
            emote.act_sad()
            break

        # Nudge/Nuzzle the person
        controller.nuzzle_target()


            



if __name__ == "__main__":
    main()
