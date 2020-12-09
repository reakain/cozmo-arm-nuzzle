#!/usr/bin/env python

import time

import pycozmo
#import pygame

import signal
import sys

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
        camera = CameraSensor(cli,'target_name')
        #cli.add_handler(pycozmo.event.EvtNewRawCameraImage, camera.on_camera_image)

        # Setup Expressions
        # if load_anims breaks, run 'pycozmo_resources.py download'
        cli.load_anims()
        emote = Expressions(cli)

        # Setup controller
        controller = CozmoController(cli,camera)

        # initialize the head angle
        cli.set_head_angle(angle = 0.6)

        # Drive off charger (call twice)
        # Get to charger edge, override cliff detector
        controller.drive_off_charger()
        controller.drive_off_charger()

        # Check for target
        if(not controller.find_target()):
            # If no target, make a sad face and quit
            emote.act_sad()
            return

        # Center the target
        controller.center_target()
        # Be happy at target once centered
        emote.act_happy()
        # Drive to the target while keeping it centered
        if(controller.drive_to_target()):
            # If made it to the target...
            emote.act_happy()
            
            # Nudge/Nuzzle the person
            controller.nuzzle_target()
        else:
            # Else be sad and quit
            emote.act_sad()
            return


# Callback to handle SIGINT and SIGTERM
def shutdown_callback(_1, _2):
    sys.exit(0)


if __name__ == "__main__":
    # Allow keyboard exit
    signal.signal(signal.SIGINT, shutdown_callback)
    signal.signal(signal.SIGTERM, shutdown_callback)

    # Start main control run
    print("Start main control run!", flush=True)
    main()
