#!/usr/bin/env python
import pycozmo
import numpy as np

class Expressions:
    def __init__(self, cli):
        self.cli = cli
        self.anim_running = False
        self.cli.add_handler(pycozmo.event.EvtAnimationCompleted, self.on_anim_complete)

    def act_sad(self):
        # Add in the action names
        self.do_action('CodeLabDejected')

    def act_frustrated(self):
        self.do_action('CodeLabFrustrated')

    def act_happy(self):
        # Add in the action names
        self.do_action('CodeLabHappy')

    def do_action(self, option):
        if option in self.cli.animation_groups:
            self.cli.play_anim_group(option)
            self.anim_running = True
            #self.cli.wait_for(pycozmo.event.EvtAnimationCompleted)

    def on_anim_complete(self, cli):
        self.anim_running = False

    def sad_face(self):
        self.generate_face(pycozmo.expressions.Sadness())
        cli.enable_procedural_face(True)

    def generate_face(self, expression):
        self.cli.enable_procedural_face(False)
        base_face = pycozmo.expressions.Neutral()

        rate = pycozmo.robot.FRAME_RATE
        timer = pycozmo.util.FPSTimer(rate)

        # Transition from base face to expression and back.
        for from_face, to_face in ((base_face, expression), (expression, base_face)):
            # Generate transition frames.
            face_generator = pycozmo.procedural_face.interpolate(from_face, to_face, rate // 3)
            for face in face_generator:

                # Render face image.
                im = face.render()

                # The Cozmo protocol expects a 128x32 image, so take only the even lines.
                np_im = np.array(im)
                np_im2 = np_im[::2]
                im2 = Image.fromarray(np_im2)

                # Display face image.
                self.cli.display_image(im2)

                # Maintain frame rate.
                timer.sleep()

            # Pause for 1s.
            for i in range(rate):
                timer.sleep()