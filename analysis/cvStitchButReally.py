import cv2
import numpy as np
import sys
import time

#vid1 = sys.argv[1]
#vid2 = sys.argv[2]

vid1 = '/home/chowder/1550419318.666945617-handcam-bottomCam.mp4'
vid2 = '/home/chowder/1550419316.586681638-handcam-topCamera.mp4'


vid1StartTimestr = vid1.split("/")[3].split("-")[0]
vid1StartTime = (int(vid1StartTimestr.split(".")[0])  * 1000) + int(vid1StartTimestr.split(".")[1][:3])

print(vid1StartTime)

vid2StartTimestr = vid2.split("/")[3].split("-")[0]
vid2StartTime = (int(vid2StartTimestr.split(".")[0])  * 1000) + int(vid2StartTimestr.split(".")[1][:3])

print(vid2StartTime)
#import videos as captures
#import both videos as arrays of frames
#get timestamp arrays for both captures
vid1i = []
vid1Timestamps = []
cap1 = cv2.VideoCapture(vid1)

while(cap1.isOpened()):
    frame_exists, curr_frame = cap1.read()
    if frame_exists:
 #       cv2.imshow('Image',curr_frame)
 #       cv2.waitKey(2)
        vid1i.append(curr_frame)
        vid1Timestamps.append(vid1StartTime + cap1.get(cv2.CAP_PROP_POS_MSEC))
        print(vid1StartTime + (cap1.get(cv2.CAP_PROP_POS_MSEC)))
    else:
        break

#cv2.destroyAllWindows()

vid1f = np.array(vid1i)
cap1.release()

print("######################")

vid2i = []
vid2Timestamps = []
cap2 = cv2.VideoCapture(vid2)

while(cap2.isOpened()):
    frame_exists, curr_frame = cap2.read()
    if frame_exists:
#        cv2.imshow('Image',curr_frame)
#        cv2.waitKey(2)
        vid2i.append(curr_frame)
        vid2Timestamps.append(vid2StartTime + (cap2.get(cv2.CAP_PROP_POS_MSEC)))
        print(vid2StartTime + (cap2.get(cv2.CAP_PROP_POS_MSEC)))
    else:
        break

vid2f = np.array(vid2i)
cap2.release()

#cv2.destroyAllWindows()

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
failed = 0
success = 0

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1920,1080))


frame = 0
stitcher = cv2.Stitcher_create()
while (frame < vid1End and frame < vid2End):
    (status, stitched) = stitcher.stitch([vid1f[vid1Start + frame],vid2f[vid2Start + frame]])
    print (vid1Timestamps[vid1Start + frame])
    print (vid2Timestamps[vid2Start + frame])
    if status == 0:
        restitched = cv2.resize(stitched,(1920,1080))
        cv2.imshow('ImageS',restitched)
        cv2.waitKey(2)
        print("stitched!")
        out.write(restitched)
        success +=1
        #time.sleep(0.033)
    else:
        print("failed to stitch")
        failed +=1

    frame += 1

print (success)
print (failed)
out.release()

cv2.destroyAllWindows()

#output synced frames that can be stitched together and displayed