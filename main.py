#!/usr/bin/env python

import time

import pycozmo
import pygame

import signal
import sys

import numpy as np
import cv2

import enum

from yolo import YOLO
from camera_sensor import CameraSensor
from expressions import Expressions
from cozmo_controller import CozmoController
from accel_tracker import BumpTracker

def main():
    pygame.init()

    # define the RGB value 
    # for white colour 
    white = (255, 255, 255) 
    black = (0,0,0)
    green = (0, 255, 0)

    # assigning values to X and Y variable 
    X = 320
    Y = 240

    # create the display surface object 
    # of specific dimension..e(X, Y). 
    display_surface = pygame.display.set_mode((X, Y )) 
    
    # set the pygame window name 
    pygame.display.set_caption('Cozmo View') 

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 14)
    log_message = "Starting system..."

    # Initial draw
    # completely fill the surface object 
    # with white colour 
    display_surface.fill(black) 

    # Add text label
    # create a text suface object,
    # on which text is drawn on it.
    text = font.render(log_message, True, green, black)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (int(textRect.w/2), int(textRect.h/2))
    # Draws the surface object to the screen.   
    display_surface.blit(text, textRect)
    # update display
    pygame.display.update()

    # some initialized settings
    exit_run = False
    looking_for_target = False
    moving_to_target = False
    nudging_target = False

    current_step = "Start"

    # setting up the cozmo client
    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()

    # Setup camera
    cli.enable_camera(enable=True, color=True)
    time.sleep(2.0)
    #camera = CameraSensor(cli,'target_name')
    camera = CameraSensor(cli)

    # Setup Expressions
    # if load_anims breaks, run 'pycozmo_resources.py download'
    cli.load_anims()
    emote = Expressions(cli)

    # Setup controller
    controller = CozmoController(cli,camera)

    # Setup Bump tracking
    bump_tracker = BumpTracker()
    cli.add_handler(pycozmo.protocol_encoder.RobotState, bump_tracker.on_new_measurement)

    # initialize the head angle
    cli.set_head_angle(angle = 0.6)

    # more setting initialization
    checked_right = False
    checked_left = False
    tolerance = 4.0

    # Update display
    # completely fill the surface object 
    # with white colour 
    display_surface.fill(black) 
    # copying the image surface object 
    # to the display surface object at 
    # (0, 0) coordinate. 
    display_surface.blit(camera.get_output_img(), (0, 0)) 
    # Add text label
    # create a text suface object,
    # on which text is drawn on it.
    text = font.render(log_message, True, green, black)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (int(textRect.w/2), int(textRect.h/2))
    # Draws the surface object to the screen.   
    display_surface.blit(text, textRect)
    # Wait to stabilize.

    time.sleep(2.0)

    # Control loop
    while True:
        # Check first for a cliff detection and then stop driving
        if controller.cliff_detected and current_step != "Idle":
            cli.stop_all_motors()
            log_message = "Found a cliff!"
            controller.bump_back()
            emote.act_sad()
            current_step = "Idle"

        # If an emote it running, don't do any other control steps
        elif emote.anim_running:
            pass

        # Initial start, getting off the charger
        elif current_step == "Start":
            log_message = "Moving off charger..."
            if(not controller.is_on_charger()):
                current_step = "Find Target"
                log_message = "Got off charger"
            elif(not controller.driving_off_charger):
                # Drive off charger (call twice)
                # Get to charger edge, override cliff detector
                controller.drive_off_charger()
                controller.drive_off_charger()
                log_message = "Moving off charger..."


        elif current_step == "Find Target":
            log_message = "Searching for friend..."
            if(not controller.turning and camera.has_target()):
                emote.act_happy()
                current_step = "Center on Target"
                log_message = "Found friend!"

            # note that duration of 0.4 is about 45 degrees
            elif not checked_right:
                log_message += " Checking right..."
                if(not controller.turning):
                    controller.turn_in_place(1)
                elif(camera.has_target()):
                    controller.stop_turning()
                    emote.act_happy()
                    current_step = "Center on Target"
                    log_message = "Found friend!"
                elif((time.time() - controller.turning_start_time) > 1):
                    controller.stop_turning()
                    checked_right = True
                
            elif not checked_left:
                log_message += " Checking left..."
                if(not controller.turning):
                    controller.turn_in_place(-1)
                elif(camera.has_target()):
                    controller.stop_turning()
                    emote.act_happy()
                    current_step = "Center on Target"
                    log_message = "Found friend!"
                elif((time.time() - controller.turning_start_time) > 2):
                    controller.stop_turning()
                    checked_left = True
                
            else:
                log_message = "Couldn't find friend..."
                current_step = "Failed"


        elif current_step == "Center on Target":
            cli.set_head_angle(angle = 0.6)
            log_message = "Facing new friend..."
            offset_dir = camera.get_offset_dir(tolerance)
            while offset_dir != 0:
                controller.turn_in_place(offset_dir)
                time.sleep(0.2)
                controller.stop_turning()
                offset_dir = camera.get_offset_dir(tolerance)
            controller.stop_turning()
            log_message = "Centered!"
            current_step = "Go To Target"
            
            #if(controller.turning):
            #    if(not camera.has_target()):
            #        controller.turn_in_place(-controller.turning_direction)

            #if(camera.has_target()):
            #    offset_dir = camera.get_offset_dir(tolerance)
            #    if(offset_dir == 0):
            ##        controller.stop_turning()
            #        log_message = "Centered!"
            #        current_step = "Go To Target"
            #    elif(not controller.turning or controller.turning_direction != offset_dir):
            #        controller.turn_in_place(offset_dir)

            # if(offset > tolerance):
            #     if(not controller.turning or controller.turning_direction < 0):
            #         # Drive right
            #         controller.turn_in_place(1)
            # elif(offset < -tolerance):
            #     if (not controller.turning or controller.turning_direction > 0):
            #         # Drive left
            #         controller.turn_in_place(-1)
            # else:
            #     controller.stop_turning()
            #     log_message = "Centered!"
            #     current_step = "Go To Target"

        elif current_step == "Go To Target":
            log_message = "Going to friend!"
            if(controller.cliff_detected):
                controller.stop_driving()
                controller.bump_back()
                log_message = "Found ledge!"
                current_step = "Failed"
            elif(controller.is_driving and bump_tracker.has_bumped()):
                controller.stop_driving()
                controller.bump_back()
                emote.act_happy()
                log_message = "Reached friend!"
                current_step = "Nudge Target"
            elif(not controller.is_driving):
                controller.drive_forward()
                bump_tracker.start_tracking()
            else:
                controller.drive_forward()

        elif current_step == "Nudge Target":
            log_message = "Getting attention..."
            controller.nuzzle_target()
            current_step = "Success"

        elif current_step == "Failed":
            log_message = "Gave up"
            # If no target, make a sad face and sit
            emote.act_sad()
            cli.stop_all_motors()
            current_step = "Idle"

        elif current_step == "Success":
            log_message = "Success!"
            # make a happy face
            emote.act_happy()
            cli.stop_all_motors()
            current_step = "Idle"


        # Update display
        # completely fill the surface object 
        # with white colour 
        display_surface.fill(white) 
        # copying the image surface object 
        # to the display surface object at 
        # (0, 0) coordinate. 
        display_surface.blit(camera.get_output_img(), (0, 0)) 
        # Add text label
        # create a text suface object,
        # on which text is drawn on it.
        text = font.render(log_message, True, green, black)
        
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        
        # set the center of the rectangular object.
        textRect.center = (int(textRect.w/2), int(textRect.h/2))
        # Draws the surface object to the screen.   
        display_surface.blit(text, textRect)

        # update display
        pygame.display.update()

        
        # iterate over the list of Event objects 
        # that was returned by pygame.event.get() method. 
        for event in pygame.event.get() : 
    
            # if event object type is QUIT 
            # then quitting the pygame 
            # and program both. 
            if event.type == pygame.QUIT : 
                cli.stop_all_motors()
                cli.disconnect()
                cli.stop()

                # deactivates the pygame library 
                pygame.quit() 
    
                # quit the program. 
                quit()  

        # Run with 25 FPS.
        time.sleep(1 / 25)

    cli.stop_all_motors()
    cli.disconnect()
    cli.stop()

# def main():
#     with pycozmo.connect() as cli:
#         # Setup camera
#         cli.enable_camera(enable=True, color=True)
#         camera = CameraSensor(cli,'target_name')
#         #cli.add_handler(pycozmo.event.EvtNewRawCameraImage, camera.on_camera_image)

#         # Setup Expressions
#         # if load_anims breaks, run 'pycozmo_resources.py download'
#         cli.load_anims()
#         emote = Expressions(cli)

#         # Setup controller
#         controller = CozmoController(cli,camera)

#         # initialize the head angle
#         cli.set_head_angle(angle = 0.6)

#         # Drive off charger (call twice)
#         # Get to charger edge, override cliff detector
#         controller.drive_off_charger()
#         controller.drive_off_charger()

#         # Check for target
#         if(not controller.find_target()):
#             # If no target, make a sad face and quit
#             emote.act_sad()
#             return

#         # Center the target
#         controller.center_target()
#         # Be happy at target once centered
#         emote.act_happy()
#         # Drive to the target while keeping it centered
#         if(controller.drive_to_target()):
#             # If made it to the target...
#             emote.act_happy()
            
#             # Nudge/Nuzzle the person
#             controller.nuzzle_target()
#         else:
#             # Else be sad and quit
#             emote.act_sad()
#             return


# Callback to handle SIGINT and SIGTERM
def shutdown_callback(_1, _2):
    sys.exit(0)
    quit()


if __name__ == "__main__":
    # Allow keyboard exit
    signal.signal(signal.SIGINT, shutdown_callback)
    signal.signal(signal.SIGTERM, shutdown_callback)

    # Start main control run
    print("Start main control run!", flush=True)
    main()
