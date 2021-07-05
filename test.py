#camera.py
# import the necessary packages
import cv2
from flask import Flask, render_template, Response
# defining face detector
cascPath = './Cascade/data/haarcascade_frontalface_alt2.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
ds_factor=0.6
class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        #releasing camera
        self.video.release()
def get_frame(self):
        # Capture frame-by-frame
        ret, frame = self.video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Display the resulting frame
        #cv2.imshow('Video', frame)
        cv2.imshow('frame1',gray)
       
        # if x+w > 0:
            #return render_template('output.html')
            # break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if x+w > 0:
                return render_template('output.html')