#!/usr/bin/env python

#pip install opencv-python


import datetime
import pygame
import pygame.camera
import time


import cv2
import time

camera = cv2.VideoCapture(0)
while not camera.isOpened():
    time.sleep(0.1)

time.sleep(5)
print("say cheese")
(ret, image) = camera.read()
if ret:
    print("got it")
    cv2.imwrite("thing.png", image)

camera.release()
del(camera)



pygame.init()
pygame.camera.init()
print("starting camera")
camera = pygame.camera.Camera("/dev/video0", (1600,1200), "RGB")
camera.start()
time.sleep(5)
print("camera initialised")

img = camera.get_image()            
f = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H%M%S")
pygame.image.save(img, "%s.jpg" % f)          

print("stopping camera")
camera.stop()
pygame.camera.quit()
pygame.quit()
