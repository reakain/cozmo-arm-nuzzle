# Cozmo Arm Nuzzling
Term project for intro to robotics class, focused on developing routines and sensing for the Cozmo desktop robot to recognize arms and hands and appropriately bump or "nuzzle" them as a means of displaying affection.

## Environment Setup
This application uses python 3, and these instructions assume python3 is set as your default python command. You can check your version with ```python --version```

1. In bash (or git bash on Windows) navigate to this respository folder, then create your virtual environment with ```python -m venv ./venv```
2. Once complete activate your environment with ```source ./venv/Scripts/activate```
3. Install the requirements once activated with ```pip install -r requirements.txt```
4. If you install any additional libraries, update the requirements with ```pip3 freeze > requirements.txt```
5. Exit the virtual environment with ```deactivate```

## uhhh


## Obsolete code
Everything in old folder is from initial testing



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
5. [Distance overlay options](https://www.oxagile.com/article/tracking-live-video-objects-with-a-moving-camera/)
6. [Single camera distance estimate](https://oroboto.net/2018/11/11/estimating-object-location-with-a-single-camera-and-opencv/)
7. [cam distance calibration](http://emaraic.com/blog/distance-measurement)
8. [Object localization](https://kapernikov.com/object-localization-with-a-single-camera-and-object-dimensions/)
9. [Camera Calibration in OpenCV](https://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html)
10. [IDK size and distance](https://handmap.github.io/measuring-size-and-distance-opencv/)
11. [Optical Flow](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html)
12. [OpenCV real time pose](https://docs.opencv.org/master/dc/d2c/tutorial_real_time_pose.html)
13. [OpenCV py pose](https://docs.opencv.org/master/d7/d53/tutorial_py_pose.html)
14. [OpenCV Dense Optical Flow](https://www.geeksforgeeks.org/python-opencv-dense-optical-flow/)
15. [DeepSort Tracking and Relative Distance](https://nanonets.com/blog/object-tracking-deepsort/)
