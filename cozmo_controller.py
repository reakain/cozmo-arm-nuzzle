#!/usr/bin/env python
import pycozmo
import numpy as np

class CozmoController:
    def __init__(self, cli, camera, tolerance = 2.0):
        self.cli = cli
        self.camera = camera
        self.tolerance = tolerance

    def drive_off_charger(self):
        return

    def center_target(self):
        not_centered = True
        while(not_centered):
            offset = self.camera.get_offset()
            if(offset > self.tolerance):
                # Drive right
            elif(offset < -self.tolerance):
                # Drive left
            else:
                not_centered = False


    def drive_to_target(self):
        # return true if reached target
        return True
        # return false otherwise

    def nuzzle_target(self):
        return
