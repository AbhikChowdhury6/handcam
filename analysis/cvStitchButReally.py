import cv2
import numpy as np
import sys
import time

vid1 = sys.argv[1]
vid2 = sys.argv[2]

vid1StartTime = long(vid1.split("-")[0])
vid2StartTime = long(vid2.split("-")[0])

#import videos as captures
#import both videos as arrays of frames
#get timestamp arrays for both captures
vid1i = []
vid1Timestamps = []
cap1 = cv2.VideoCapture(vid1)

while(cap1.isOpened()):
    frame_exists, curr_frame = cap1.read()
    if frame_exists:
        vid1i.append(curr_frame)
        vid1Timestamps.append(vid1StartTime + cap1.get(cv2.CAP_PROP_POS_MSEC) * 10000000)
    else:
        break

vid1f = np.array(vid1i)
cap1.release()

vid2i = []
vid2Timestamps = []
cap2 = cv2.VideoCapture(vid2)

while(cap2.isOpened()):
    frame_exists, curr_frame = cap2.read()
    if frame_exists:
        vid2i.append(curr_frame)
        vid2Timestamps.append(vid2StartTime + (cap2.get(cv2.CAP_PROP_POS_MSEC) * 1000000)
    else:
        break

vid2f = np.array(vid2i)
cap2.release()

#compare the first element in each array to determine which started first
#take the one that started first and iterate through the timestamps untill they sync
#do the sme thing with the end to see wich one ends first and where
vid1Start = 0
vid1End = len(vid1Timestamps) -1
vid2Start = 0
vid2End = len(vid2Timestamps) -1

while (vid1Timestamps[vid1Start] < vid2Timestamps[0]):
    vid1Start += 1

while (vid2Timestamps[vid2Start] < vid1Timestamps[0]):
    vid2Start += 1


while (vid1Timestamps[vid1End] > vid2Timestamps[vid2End]):
    vid1End -= 1

while (vid2Timestamps[vid2End] > vid1Timestamps[vid1End]):
    vid2End -= 1  

#iterate through the indexes in the common subset of both videos
#stitch them together and display them

frame = 0
stitcher = cv2.Stitcher_create()
while (frame < vid1End or vid2End):
    (status, stitched) = stitcher.stitch([vid1f[vid1Start + frame],vid2f[vid2Start + frame]])
    if status == 0:
        cv2.imshow('Image',stitched)
        time.sleep(0.033)
    else:
        print("failed to stitch")


#output synced frames that can be stitched together and displayed