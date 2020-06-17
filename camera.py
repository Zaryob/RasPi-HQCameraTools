#!/usr/bin/python3
# -*- config: utf-8
# import the necessary packages

from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import cv2
capture_button = [120,170,420,480]
close_button = [170,220,420,480]

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 32
camera.rotation = 90
rawCapture = PiRGBArray(camera, size=(480, 320))
# allow the camera to warmup
time.sleep(0.1)

# function that handles the mousclicks
def process_click(event, x, y,flags, params):
# check if the click is within the dimensions of the button
	if event == cv2.EVENT_LBUTTONDOWN:
		if y > capture_button[0] and y < capture_button[1] and x > capture_button[2] and x < capture_button[3]:
			time.sleep(0.1)
			camera.capture("capture  {}.jpg".format(str(datetime.now())), resize=(4056, 3040))
			time.sleep(0.1)

		if y > close_button[0] and y < close_button[1] and x > close_button[2] and x < close_button[3]:
			cv2.destroyAllWindows()
			exit(0)


cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow("Image", 0,0)
cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# create a window and attach a mousecallback and a trackbar
cv2.setMouseCallback('Image',process_click)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = cv2.rectangle(frame.array,(capture_button[2], capture_button[0]),(capture_button[3],capture_button[1]),(0,255,0),-1)
	image = cv2.rectangle(frame.array,(close_button[2], close_button[0]),(close_button[3],close_button[1]),(0,0,255),-1)
	cv2.putText(image,str(datetime.now()),(240,300),cv2.FONT_HERSHEY_PLAIN, .7, (255,255,255),2,cv2.LINE_AA)
	# show the frame
	cv2.imshow("Image", image)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
