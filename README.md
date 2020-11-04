# Cozmo Arm Nuzzling
Term project for intro to robotics class, focused on developing routines and sensing for the Cozmo desktop robot to recognize arms and hands and appropriately bump or "nuzzle" them as a means of displaying affection.

## Environment Setup
This application uses python 3, and these instructions assume python3 is set as your default python command. You can check your version with ```python --version```

1. In bash (or git bash on Windows) navigate to this respository folder, then create your virtual environment with ```python -m venv ./venv```
2. Once complete activate your environment with ```source ./venv/Scripts/activate```
3. Install the requirements once activated with ```pip install -r requirements.txt```
4. If you install any additional libraries, update the requirements with ```pip3 freeze > requirements.txt```
5. Exit the virtual environment with ```deactivate```

## Part 1 Requirements - Nov 2
This is a very open-ended assignment that can be done as a group. The goal is to download a piece of software and get it to do Something Useful. Please OK your project (and group members) with the Professor first.

Note: We have several Intel RealSense and Kinects floating around, along with a few lidar units, You may do this with cameras or lidar or sonar.

### Some possible tasks
- 3D reconstruct an object (images->textured 3D model)
- Track the location of an object in 2.5D
- Track the location of a camera/robot in the plane or 6D
- Reliably segment an object out of a cluttered background
- Identify objects in an image
- Do high-quality tracking with one of our opti-trak systems (the box or stand-alone cameras)
 
### What to turn in
A BOX folder with the following:
- A description of what you were trying to do (get this approved first)
-  A detailed report on how you got the software to work and what issues you ran into (i.e., keep track of what happens as you go)
-  Details on the hardware and software used
-  BOX link with input images/data, output results
- If applicable, a snapshot of the executable/code used

You may fail entirely to get the software to work. That's (mostly) ok, provided you can document/explain *why* it didn't work, along with the experiments you tried to get it working...

## Part 2 Requirements - Nov 9th
Find a person/object in an image using existing software. You may use any existing software package; the point is to learn to use a piece of software that might be useful for a project. This can be a group project, but the level of difficulty should match the number of people.

### Possible projects
- Find and track SIFT features in a video
- Segment an image into foreground and background 
- Determine if a specific object is in an image (eg stop signs)
- Find lines/cones/planes etc in an image
- Find faces in a set of images
- Determine facial expression in a set of images 
- Track/recognize gestures
- Draw a box around an object as it moves around an image (tracking)

### What to turn in
A BOX folder with the following:
- A description of what you were trying to do (get this approved first)
- A detailed report on how you got the software to work and what issues you ran into (i.e., keep track of what happens as you go)
- Details on the hardware and software used
- BOX link with input images/data, output results
- If applicable, a snapshot of the executable/code used

You may fail entirely to get the software to work. That's (mostly) ok, provided you can document/explain *why* it didn't work, along with the experiments you tried to get it working...

## Part 3 Requirements - Nov 30
The goal of the final project is to use a Real Robot to do a Real task that involves at least some interaction with a Human. This is a group project; you should not try to do this one on your own.

### Constraints
You may use any robot hardware that your lab has access to. We also have several Kuri robots that would love to get out of their boxes. Dr. Smart's lab has a Fetch, Turtle Bot and PR2, Dr. Grimm's lab has a Kenova arm, Dr. Hollinger's lab has drones, and Dr. Davidson's lab has a UR5. If you wish to use these platforms you will need to communicate with the lab owners to make sure they're available, and if so, when (many of these are in use with active research projects). One of the goals of this project is to "train-up" on your lab's robotic's hardware.

Your task must involve some form of sense, think, and act. I would prefer this to involve some sort of interaction with a human; if you can make a compelling case for robot-robot interaction then run it by me first.

You may use as much existing software as you can; however, there must be some novel part that is not out-of-the-box (i.e., no downloading a demo...) 

### What to turn in
- A description of the desired interaction[1-2pages]
  - Sense: Describe the sensing the robot will do.
    - Hardware: What hardware are you using for the sensing?
    - Algorithms: What algorithms are you using to process the sensing?
  - Act: Describe the actions the robot will take.
    - Hardware: What hardware are you using/activating?
    - What low-level control algorithms/strategies are you using?
  - Think: What is your world state? How is the robot representing the world?
    - What decisions will the robot make?
    - What planning (if any) does the robot need to do?
    - How will the robot make its decisions?
- A timeline for completion
  - Who will do what and when?
- Assignment of points
  - For each item above, assign points for completion (should total to 100)
  - Assign an owner for each item (who in your group is responsible for ensuring that part is done?)
    - You can all work on all things, but there should be one *owner* for each item
  - Define how you will demonstrate that each item is working (eg, video, interaction, test code...)

Possible platform to try: https://aws.amazon.com/robomaker/


## References

### Part 1
1. [OpenCV](https://opencv.org/)
2. [pycozmo](https://github.com/zayfod/pycozmo/)
3. [cozmo SDK](http://cozmosdk.anki.com/docs/index.html)
4. [OpenCV tutorials](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html)
5. [imutils](https://github.com/jrosebr1/imutils)
6. [OpenCV feature detection](https://docs.opencv.org/3.4/d7/d66/tutorial_feature_detection.html)
7. [OpenCV edge detection](https://docs.opencv.org/master/da/d22/tutorial_py_canny.html)
8. [Google hand tracking](https://ai.googleblog.com/2019/08/on-device-real-time-hand-tracking-with.html)
9. [OpenCV Shape Detection](https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/)
10. [More Shape Detection](https://hub.packtpub.com/opencv-detecting-edges-lines-shapes/)
11. [Object Recognition](https://towardsdatascience.com/extracting-circles-and-long-edges-from-images-using-opencv-and-python-236218f0fee4)
12. [Contours](https://towardsdatascience.com/edges-and-contours-basics-with-opencv-66d3263fd6d1)
13. [Object Detection](https://www.analyticsvidhya.com/blog/2018/06/understanding-building-object-detection-model-python/)
14. [TensorFlow? TensorFlow](https://towardsdatascience.com/object-detection-with-less-than-10-lines-of-code-using-python-2d28eebc5b11)
15. [More TensorFlow](https://stackabuse.com/object-detection-with-imageai-in-python/)

### Part 2
1. [OpenCV Distance](https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/)
2. [OpenCV Distance between objects](https://www.pyimagesearch.com/2016/04/04/measuring-distance-between-objects-in-an-image-with-opencv/)
3. [Raytracing oh no](https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9)
4. [Finger detection and tracking](https://dev.to/amarlearning/finger-detection-and-tracking-using-opencv-and-python-586m)
