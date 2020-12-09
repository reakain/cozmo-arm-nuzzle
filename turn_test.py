import pycozmo


with pycozmo.connect() as cli:

    target = pycozmo.util.Pose(500, 00.0, 0.0, angle_z=pycozmo.util.Angle(degrees=0.0))
    cli.go_to_pose(target, relative_to_robot=True)
