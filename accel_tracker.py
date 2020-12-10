import numpy
import pycozmo
import math

# accel tracking
# To prevent mis-reads and rapid flip-flopping, a small buffer has been incorporated.
class BumpTracker:
    def __init__(self):
        self.size = 20
        self.rms = numpy.zeros(self.size)
        self.current_index = 0
        self.new_bump = False
        self.is_initializing = True
        self.tracking = False
        self.num_stds = 3

    def on_new_measurement(self, cli, pkt: pycozmo.protocol_encoder.RobotState):
        if(not self.tracking):
            return
        strength2D = math.sqrt((pkt._accel_x*pkt.accel_x) + (pkt.accel_y*pkt.accel_y))

        if(not self.is_initializing):
            diff = abs(strength2D - numpy.mean(self.rms))
            if(diff > self.num_stds*numpy.std(self.rms)):
                self.new_bump = True
        elif(self.current_index == self.size-1):
            self.is_initializing = False

        self.rms[self.current_index] = strength2D
        self.current_index = self.current_index + 1
        if self.current_index >= self.size:
            self.current_index = 0

    def has_bumped(self):
        bump_val = self.new_bump
        self.new_bump = False
        return bump_val

    def start_tracking(self):
        self.tracking = True