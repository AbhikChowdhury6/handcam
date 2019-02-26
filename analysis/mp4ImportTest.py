import cv2
import numpy as np
import time
vid1 = '/home/chowder/1551119463.666197034--.mp4'


cap1 = cv2.VideoCapture(vid1)

vid1i = []

while(cap1.isOpened()):
    frame_exists, curr_frame = cap1.read()
    if frame_exists:
        vid1i.append(curr_frame)
        print("processed")
        cv2.imshow('Image',curr_frame)
        cv2.waitKey(4)
        #time.sleep(.25)
    else:
        break

cap1.release()


stitcher = cv2.Stitcher_create()
print(len(vid1i))

i = 0
while i < len(vid1i)/5:
    cv2.imshow('Image',vid1i[i*5]) 
    cv2.waitKey(3000)
    i += 1

(status, stitched) = stitcher.stitch(vid1i)
print(status)
cv2.imshow('Image',stitched) 
cv2.waitKey(1000)
