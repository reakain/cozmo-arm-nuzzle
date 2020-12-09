#!/usr/bin/env python
import pycozmo
import numpy as np

class CozmoController:
    def __init__(self, cli, camera, tolerance = 2.0):
        self.cli = cli
        self.camera = camera
        self.tolerance = tolerance
        #self.cli.add_handler(pycozmo.protocol_encoder.RobotState, self.on_robot_state)
        self.cli.add_handler(pycozmo.event.EvtCliffDetectedChange, self.on_cliff_detected)
        self.cli.add_handler(pycozmo.protocol_encoder.RobotPoked, self.on_robot_poked)
        self.cli.add_handler(pycozmo.event.EvtRobotMovingChange, self.on_robot_moving_change)
        self.cli.add_handler(pycozmo.event.EvtRobotWheelsMovingChange, self.on_wheels_moving_change)
        self.cliff_detected = False
        self.robot_moving = False
        self.wheels_moving = False

        self.driving_off_charger = False

    #def on_robot_state(self, cli, pkt: pycozmo.protocol_encoder.RobotState):
        #if(pkt.status == pycozmo.event.STATUS_EVENTS.

    def on_robot_moving_change(self, cli, state: bool):
        self.robot_moving = state
        print("Robot is moving: " + str(state))

    def on_wheels_moving_change(self, cli, state: bool):
        self.wheels_moving = state
        print("Wheels moving: " + str(state))

    def on_cliff_detected(self, cli, state: bool):
        # This works. Disabled the print/backup for driving off charger
        # if it doesn't back up, then the next drive_wheels will
        # cause Cozmo to fling itself into the abyss
        self.cliff_detected = state
        if state:
            self.cli.stop_all_motors()
            if self.driving_off_charger == False:
                # back up, say that cliff is found
                self.cli.drive_wheels(-100, -100, lwheel_acc=999, rwheel_acc=999, duration = 1)
                print("Cozmo has detected a cliff!")

    def on_robot_poked(self, cli, pkt: pycozmo.protocol_encoder.RobotPoked):
        # TODO: maybe this will work for sensing?
        print("Robot poked.")

    def drive_off_charger(self):
        # Drives off charger, call twice to get past cliff detection
        self.driving_off_charger = True
        self.cli.drive_wheels(100, 100, lwheel_acc=999, rwheel_acc=999, duration = 1)
        self.driving_off_charger = False
        return

    def find_target(self):
        if(self.camera.find_target()):
            return True

        # the elegant way wasn't working, so here's the brute force way
        if self.rotate_left(.4):
            return True
        if self.rotate_left(.4):
            return True
        if self.rotate_right(1.2):
            return True
        if self.rotate_right(.4):
            return True

        return False

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



    def center_target(self):
        # TODO: tune in turning
        not_centered = True
        while(not_centered):
            offset = self.camera.get_offset()
            if(offset > self.tolerance):
                # Drive right
                self.rotate_right(0.075)
            elif(offset < -self.tolerance):
                # Drive left
                self.rotate_left(0.075)
            else:
                not_centered = False
            
    def is_centered(self):
        offset = self.camera.get_offset()
        return (offset < self.tolerance and offset > -self.tolerance)

    def sense_target(self):
        # TODO: Figure out target sensing
        return self.wheels_moving and not self.robot_moving

    def drive_to_target(self):
        # While we haven't sensed the target...
        while(not self.sense_target()):
            # if we havefound a cliff...
            if(self.cliff_detected):
                # Stop driving
                self.cli.stop_all_motors()
                return False
            # if we're still centered..
            if(self.is_centered()):
                self.cli.drive_wheels(100,100)
            else:
                self.center_target()
        # return true if reached target
        return True
        # return false otherwise

    def nuzzle_target(self):
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

    
