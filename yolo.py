#!/usr/bin/env python
# https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

import numpy as np
import argparse
import time
import cv2
import os


class YOLO:
    def __init__(self, names,weights,config,confidence,threshold, target_name = "all"):
        self.confidence = confidence
        self.threshold = threshold
        # load the COCO class labels our YOLO model was trained on
        self.labelsPath = names
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        if(target_name != "all" and target_name in self.LABELS):
            self.target_id = self.LABELS.index(target_name)
        else:
            self.target_id = -1

        # initialize a list of colors to represent each possible class label
        #np.random.seed(42)
        #self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
        #    dtype="uint8")

        # derive the paths to the YOLO weights and model configuration
        self.weightsPath = weights
        self.configPath = config

        self.center_x_coord = 0

        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        
        # if this line breaks, redownload weights file
        # stack exchange on issue: https://tinyurl.com/y6rw5jvx
        # redownload link (will initiate 200MB download): https://tinyurl.com/yyey45r4
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)

        # determine only the *output* layer names that we need from YOLO
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def analyze_image(self,image):
        # load our input image and grab its spatial dimensions
        (H, W) = image.shape[:2]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()

        # show timing information on YOLO
        #print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        #classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)

                # only look out features that match our target
                if(self.target_id == -1 or self.target_id == classID):

                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > self.confidence:
                        # scale the bounding box coordinates back relative to the
                        # size of the image, keeping in mind that YOLO actually
                        # returns the center (x, y)-coordinates of the bounding
                        # box followed by the boxes' width and height
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        self.center_x_coord = centerX

                        # use the center (x, y)-coordinates to derive the top and
                        # and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates, confidences,
                        # and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        #classIDs.append(classID)

                        # RETURNS COORDINATES
                        # returns the coordinates and confidence of the box
                        return([centerX, centerY, int(width), int(height), float(confidence)])

        

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            for i in idxs.flatten():
                return( [boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3], confidences[i]])
        #    # loop over the indexes we are keeping
        #    for i in idxs.flatten():

        # IF NO TARGET FOUND, RETURN NONE
        return None

        # kept the image stuff in case we want it later

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        #idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence,
        #    self.threshold)

        # ensure at least one detection exists
        #if len(idxs) > 0:
        #    # loop over the indexes we are keeping
        #    for i in idxs.flatten():
        #        # extract the bounding box coordinates
        #        (x, y) = (boxes[i][0], boxes[i][1])
        #        (w, h) = (boxes[i][2], boxes[i][3])

        #        # draw a bounding box rectangle and label on the image
        #        color = [int(c) for c in self.COLORS[classIDs[i]]]
        #        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        #        text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
        #        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
        #            0.5, color, 2)

    def get_center(self):
        return self.center_x_coord

