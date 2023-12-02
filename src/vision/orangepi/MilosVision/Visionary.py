import json
import time
import sys
from threading import Thread
import cv2
import apriltag
from cscore import CameraServer
import cv2
import numpy as np

#When last update print
print("Updated 2023-12-2-117")

#Camera init
CameraServer.enableLogging()

width = 160
height = 120

camera = CameraServer.startAutomaticCapture()
camera.setResolution(width, height)

#grabs a frame from the camera
sink = CameraServer.getVideo()
output = CameraServer.putVideo("Cam1", width, height)

#Loop does the following:
#Grab a frame from the camera
#Find apriltages
#output processed image
while True:
   time, input_img = cvSink.grabFrame(input_img)

   if time == 0: # There is an error
      continue
   #Takes camera image and finds apriltages
   detector = apriltag.Detector()
   result = detector.detect(input_img)
   output.putFrame(result)
