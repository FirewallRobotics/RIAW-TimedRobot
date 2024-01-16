import json
import time
import sys
from threading import Thread
import cv2
import apriltag
from cscore import CameraServer
import cv2
import numpy as np
from networktables import NetworkTables

#When last update print
print("Updated 2023-12-2-117")

#Camera init
CameraServer.enableLogging()

width = 160
height = 120

camera = CameraServer.startAutomaticCapture()
camera.setResolution(width, height)

#Init NetworkTables
NetworkTables.initialize(server="localhost") # check the NetworkTables server address
table = NetworkTables.getTable("Dashboard") 

#grabs a frame from the camera
cvSink = CameraServer.getVideo()
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

  #Convert AprilTag data to a format suitable for Networktables
   tag_data = [{"id" : detection.tag_id, "pose" : detection.pose_t} for detection in result] 

   #Send data to NetworkTables 
   try:
       table.putString("april_tag_data". json.dumps(tag_data)) 
   except Exception as e:
       print("Error sending data to NetworkTables") 

   for detection in result: 
      detection.draw(input_img) 

   #Output the processed image
   output.putFrame(result)
