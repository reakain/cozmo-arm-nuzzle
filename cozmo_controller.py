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
        self.cliff_detected = False

    #def on_robot_state(self, cli, pkt: pycozmo.protocol_encoder.RobotState):
        #if(pkt.status == pycozmo.event.STATUS_EVENTS.

    def on_cliff_detected(self, cli, new_state):
        self.cliff_detected = new_state
        self.cli.stop_all_motors()


    def drive_off_charger(self):
        self.cli.drive_wheels(100, 100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)
        return

    def center_target(self):
        not_centered = True
        while(not_centered):
            offset = self.camera.get_offset()
            if(offset > self.tolerance):
                # Drive right
                self.cli.drive_wheels(100,-100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)
            elif(offset < -self.tolerance):
                # Drive left
                self.cli.drive_wheels(-100,100, lwheel_acc=999, rwheel_acc=999, duration = 0.3)
            else:
                not_centered = False

    def is_centered(self):
        offset = self.camera.get_offset()
        return (offset < self.tolerance and offset > -self.tolerance)

    def sense_target(self):
        return True

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
        return

    
