#!/usr/bin/env python
import pycozmo
import numpy as np
import time
from accel_tracker import BumpTracker

class CozmoController:
    def __init__(self, cli, camera, tolerance = 2.0):
        self.cli = cli
        self.camera = camera
        self.bump_tracker = BumpTracker()
        self.tolerance = tolerance
        #self.cli.add_handler(pycozmo.protocol_encoder.RobotState, self.bump_tracker.on_new_measurement)
        #self.cli.add_handler(pycozmo.event.EvtRobotStateUpdated, self.on_state_update)
        self.cli.add_handler(pycozmo.event.EvtCliffDetectedChange, self.on_cliff_detected)
        # self.cli.add_handler(pycozmo.protocol_encoder.RobotPoked, self.on_robot_poked)
        self.cli.add_handler(pycozmo.event.EvtRobotMovingChange, self.on_robot_moving_change)
        self.cli.add_handler(pycozmo.event.EvtRobotWheelsMovingChange, self.on_wheels_moving_change)
        # self.cli.add_handler(pycozmo.event.EvtRobotBodyAccModeChange, self.on_body_acc_mode_change)
        self.cliff_detected = False
        self.robot_moving = False
        self.wheels_moving = False
        self.driving_off_charger = False
        self.looking_for_target = False
        self.on_charger = True
        self.turning = False
        self.turning_direction = 0
        self.turning_start_time = time.time()
        self.is_driving = False
        self.bump_detected = False
        self.get_off_charger_time = time.time()

    #def on_robot_state(self, cli, pkt: pycozmo.protocol_encoder.RobotState):
        #if(pkt.status == pycozmo.event.STATUS_EVENTS.

    def on_body_acc_mode_change(self, cli, state):
        print("Accel mode does nothing!", flush=True)
        print("Accel mode is " + state, flush=True)

    def on_robot_moving_change(self, cli, state: bool):
        self.robot_moving = state

        #print("Robot is moving: " + str(state), flush=True)

    def on_wheels_moving_change(self, cli, state: bool):
        # clear out bump tracker of any bumps on start moving
        #if(state and not self.wheels_moving):
        #    self.bump_tracker.has_bumped()
        
        self.wheels_moving = state
        #print("Wheels moving: " + str(state), flush=True)

    def on_cliff_detected(self, cli, state: bool):
        # This works. Disabled the print/backup for driving off charger
        # if it doesn't back up, then the next drive_wheels will
        # cause Cozmo to fling itself into the abyss
        if not self.on_charger:
            if state:
                self.cliff_detected = True
                self.cli.stop_all_motors()
                self.bump_back()
        # if state:
        #     self.cliff_detected = True
        #     self.cli.stop_all_motors()
        #     if self.driving_off_charger == False:
        #         # back up, say that cliff is found
        #         self.cli.drive_wheels(-100, -100, lwheel_acc=999, rwheel_acc=999, duration = 1)
        #         print("Cozmo has detected a cliff!")

    def on_robot_poked(self, cli, pkt: pycozmo.protocol_encoder.RobotPoked):
        # TODO: maybe this will work for sensing?
        print("Robot poked.")

    # def drive_off_charger(self):
    #     # Drives off charger, call twice to get past cliff detection
    #     self.driving_off_charger = True
    #     self.cli.drive_wheels(100, 100, lwheel_acc=999, rwheel_acc=999, duration = 1)
    #     self.driving_off_charger = False
    #     return

    def drive_off_charger(self):
        # Drives off charger, call twice to get past cliff detection
        self.driving_off_charger = True
        self.cli.drive_wheels(100, 100, lwheel_acc=999, rwheel_acc=999, duration= 2)
        #target = pycozmo.util.Pose(1000, 00.0, 0.0, angle_z=pycozmo.util.Angle(degrees=0.0))
        #self.cli.go_to_pose(target, relative_to_robot=True)
        self.get_off_charger_time = time.time()

    def is_on_charger(self):
        if(self.driving_off_charger):
            if((time.time() - self.get_off_charger_time) > 3):
                self.cli.stop_all_motors()
                self.driving_off_charger = False
                self.on_charger = False
                return False
            return True
        return self.on_charger


    # def find_target(self):
    #     print("finding person", flush=True)
    #     if(self.camera.find_target()):
    #         return True

    #     # the elegant way wasn't working, so here's the brute force way
    #     # note that duration of 0.4 is about 45 degrees
    #     if self.rotate_left(.4):
    #         return True
    #     if self.rotate_left(.4):
    #         return True
    #     if self.rotate_right(1.2):
    #         return True
    #     if self.rotate_right(.4):
    #         return True

    #     return False

    # duration of 0.4 is ~ 45 degrees
    def rotate_left (self, dur):
        self.cli.drive_wheels(-100, 100, lwheel_acc=999, rwheel_acc=999, duration = dur)
        if(self.camera.find_target()):
            return True
        else:
            return False

    def rotate_right (self, dur):
        self.cli.drive_wheels(100, -100, lwheel_acc=999, rwheel_acc=999, duration = dur)
        if(self.camera.find_target()):
            return True
        else:
            return False

    def turn_in_place(self,direction):
        self.turning = True
        self.turning_start_time = time.time()
        self.turning_direction = np.sign(direction)
        self.cli.drive_wheels(self.turning_direction*100, -self.turning_direction*100)
        # if(direction > 0):
        #     # Turn right
        #     self.cli.drive_wheels(100, -100)
        # else:
        #     # Turn left
        #     self.cli.drive_wheels(-100, 100)

    def stop_turning(self):
        self.cli.stop_all_motors()
        self.turning = False
    # the elegant way that didn't quite work
    #def find_target(self):
    #    if(self.camera.find_target()):
    #        return True
    #
    #    # Do a 45 degree sweep right then left
    #    current_angle = 0.0
    #    dtheta = 5.0
    #    checked_right = False
    #    while(current_angle > -45):
    #        print("trying to turn in place")
    #        self.turn_in_place(dtheta)
    #        print("made it past first turn call")
    #        current_angle += dtheta
    #        if(self.camera.find_target()):
    #            return True
    #        if(self.cli.pose.rotation.angle_z.degrees >= 45):
    #            dtheta = -dtheta
    #    return False


    #def turn_in_place(self, angle):
    #    print("made it to the call")
    #    target = pycozmo.util.Pose(0.0, 0.0, 0.0, angle_z=pycozmo.util.Angle(degrees=angle))
    #    print("got the target")
    #    self.cli.go_to_pose(target, relative_to_robot=True)
    #    print("understands target pose")
    #    # starting = self.cli.pose.rotation.angle_z.degrees
    #    # finish = starting + angle
    #   # while(abs(self.cli.pose.rotation.angle_z.degrees - finish) > self.tolerance):
    #    #     if(angle >= 0):
    #    #         self.cli.drive_wheels(100,-100, lwheel_acc=999, rwheel_acc=999)
    #    #     else:
    #    #         self.cli.drive_wheels(-100,100, lwheel_acc=999, rwheel_acc=999)
    #    # self.cli.stop_all_motors()

    def stop_driving(self):
        self.cli.stop_all_motors()
        self.is_driving = False

    def drive_forward(self):
        self.is_driving = True
        self.cli.drive_wheels(100,100)

    def bump_back(self):
        self.cli.drive_wheels(-100,-100,duration=0.075)


    def center_target(self):
        # centers target. Note that the rotate_right/left methods
        # grab a new yolo'd frame to work with, so no worries there!
        print("start centering", flush=True)
        not_centered = True
        while(not_centered):
            offset = self.camera.get_offset()
            if(offset > self.tolerance):
                # Drive right
                self.rotate_right(0.06)
            elif(offset < -self.tolerance):
                # Drive left
                self.rotate_left(0.06)
            else:
                not_centered = False
            
    def is_centered(self):
        offset = self.camera.get_offset()
        return (offset < self.tolerance and offset > -self.tolerance)

    def sense_target(self):
        # TODO: Figure out target sensing
        #accel_bump = self.bump_tracker.has_bumped()
        #return self.wheels_moving and accel_bump
        print("sensing target", flush=True)
        return self.wheels_moving and not self.robot_moving

    def drive_to_target(self):
        print("going totarget", flush=True)
        # self.looking_for_target = True
        # # While we haven't sensed the target...
        # #while(not self.sense_target()):
        # while(self.looking_for_target):
        #     # if we havefound a cliff...
        #     if(self.cliff_detected):
        #         # Stop driving
        #         self.cli.stop_all_motors()
        #         self.looking_for_target = False
        #         return False
        #     # if we're still centered..
        #     if(self.is_centered()):
        #         self.cli.drive_wheels(100,100,lwheel_acc=999, rwheel_acc=999,duration=0.4)
        #     else:
        #         self.center_target()
        # # return true if reached target
        # return True
        # # return false otherwise

    def nuzzle_target(self):
        print("start nuzzling", flush=True)
        # TODO: Add nuzzling behavior
        # Lift shovel
        self.cli.set_lift_height(pycozmo.robot.MAX_LIFT_HEIGHT.inches)
        # Drive in a bit
        self.cli.drive_wheels(100, 100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)
        # Bop with shovel
        self.cli.set_lift_height((pycozmo.robot.MAX_LIFT_HEIGHT.inches - pycozmo.robot.MIN_LIFT_HEIGHT.inches)/2 + pycozmo.robot.MIN_LIFT_HEIGHT.inches)
        # TODO: Add a wait period?
        self.cli.set_lift_height(pycozmo.robot.MAX_LIFT_HEIGHT.inches)
        # TODO: smile maybe
        # Drive back out
        self.cli.drive_wheels(-100, -100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)
        # Lower shovel
        self.cli.set_lift_height(pycozmo.robot.MIN_LIFT_HEIGHT.inches)
        # TODO: wiggle/smile?
        return

    
