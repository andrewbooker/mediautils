#!/usr/bin/env python

#pip install opencv-python

import time
import cv2
import sys

videoIdx = int(sys.argv[1]) if len(sys.argv) > 1 else 0

camera = cv2.VideoCapture(videoIdx)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while not camera.isOpened():
    time.sleep(0.1)

rval, frame = camera.read()

rval = True
while rval:
    cv2.imshow("Camera", frame)
    rval, frame = camera.read()
    key = cv2.waitKey(20)
    if key == 27 or key == ord("q"):
        break

cv2.destroyWindow("Camera")
camera.release()
del(camera)

