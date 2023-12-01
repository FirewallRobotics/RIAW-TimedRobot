from threading import Thread
import cv2
import numpy
import apriltag

class myWebcamVideoStream:
  def __init__(self, src=0):
    
    # initialize the video camera stream and read the 
    # first frame from the streamself.stream = cv2.VideoCapture(src, cv2.CAP_V4L)
    (self.grabbed, self.frame) = self.stream.read()

    # flag to stop the thread

    self.stopped = False

  def start(self):
    # start the thread to read frames
    Thread(target=self.update, args=()).start()
    return self

  def update(self):

    while True:
       # have we been told to stop?  If so, get out of here
       if self.stopped:
           return

       # otherwise, get another frame
       (self.grabbed, self.frame) = self.stream.read()

  def read(self):
      # return the most recent frame
      return self.frame

  def stop(self):
      # signal thread to end
      self.stopped = True
      return

def plotPoint(image, center, color):
    center = (int(center[0]), int(center[1]))
    image = cv2.line(image,
                     (center[0] - 5, center[1]),
                     (center[0] + 5, center[1]),
                     color,
                     3)
    image = cv2.line(image,
                     (center[0], center[1] - 5),
                     (center[0], center[1] + 5),
                     color,
                     3)
    return image


# main program
vs = myWebcamVideoStream(1).start() 
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

iteration = 0
saved = False

while iteration < 500:
   frame = vs.read()
   grayimage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   detections = detector.detect(grayimage)
   if not detections:
       #print("Nothing")
       continue
   else:
       for detect in detections:
           # print("tag_id: %s, center: %s" % (detect.tag_id, detect.center))
           frame=plotPoint(frame, detect.center, (255,0,255))
           for corner in detect.corners:
               frame=plotPoint(frame, corner, (0,255,255))
       if not saved:
           cv2.imwrite("fulmer.jpg",frame)
           saved = True
           print("Saved!")
   cv2.imshow('frame', frame)
   cv2.waitKey(1)
   iteration = iteration + 1

vs.stop()
cv2.destroyAllWindows()