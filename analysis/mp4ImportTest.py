import cv2
import numpy as np
import time
vid1 = '/home/chowder/1550419318.666945617-handcam-bottomCam.mp4'


cap1 = cv2.VideoCapture(vid1)

while(cap1.isOpened()):
    frame_exists, curr_frame = cap1.read()
    if frame_exists:
        cv2.imshow('Image',curr_frame)
        cv2.waitKey(4)
        #time.sleep(.25)