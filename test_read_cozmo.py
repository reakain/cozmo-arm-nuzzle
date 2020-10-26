#!/usr/bin/env python
# From https://github.com/zayfod/pycozmo/blob/master/examples/camera.py

# To connect to Cozmo:
# A Wi-Fi connection needs to be established with Cozmo before using PyCozmo applications.
#   Wake up Cozmo by placing it on the charging platform
#   Make Cozmo display it's Wi-Fi PSK by rising and lowering its lift
#   Scan for Cozmo's Wi-Fi SSID (depends on the OS)
#   Connect using Cozmo's Wi-Fi PSK (depends on the OS)

# Test getting camera frames from cozmo using pycozmo
import time
import pycozmo
from matplotlib import pyplot as plt
def on_camera_image(cli, image):
    del cli
    image.save("camera.png", "PNG")

    # display a camera frame using plt
    plt.imshow(image)
    plt.title('Cozmo Frame'), plt.xticks([]), plt.yticks([])

    plt.show()

def pycozmo_program(cli: pycozmo.client.Client):
    angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
    cli.set_head_angle(angle)

    pkt = pycozmo.protocol_encoder.EnableCamera()
    cli.conn.send(pkt)
    pkt = pycozmo.protocol_encoder.EnableColorImages(enable=True)
    cli.conn.send(pkt)

    # Wait for image to stabilize.
    time.sleep(2.0)

    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image, one_shot=True)

    # Wait for image to be captured.
    time.sleep(1)


pycozmo.run_program(pycozmo_program)



