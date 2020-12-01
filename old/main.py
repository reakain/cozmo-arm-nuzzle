#!/usr/bin/env python

import cv2 as cv
import time
import pycozmo
from im_detect import FrameAnalysis


# pycozmo program
def pycozmo_program(cli: pycozmo.client.Client):
    # spin up the Frame Analysis stuff
    frame_analysis = FrameAnalysis()

    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    pkt = pycozmo.protocol_encoder.EnableCamera()
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.EnableColorImages(enable=True)
    cli.conn.send(pkt)

    # Wait for image to stabilize.
    time.sleep(2.0)

    # handler to get image and feed to frame analysis
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, frame_analysis.new_image, one_shot=True)

    # Wait for image to be captured.
    time.sleep(1)

    # Ouput frame and edges
    plt.subplot(121),plt.imshow(frame_analysis.image,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(frame_analysis.edges,cmap = 'gray')
    plt.title('Edge'), plt.xticks([]), plt.yticks([])

    plt.show()


pycozmo.run_program(pycozmo_program)


