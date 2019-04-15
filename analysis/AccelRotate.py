import cv2
import numpy as np
import sys
import time
import imutils

#vid1 = sys.argv[1]
#vid2 = sys.argv[2]

vid1 = '/home/chowder/1550594841.134619449-handcam-topcamera.mp4'


vid1StartTimestr = vid1.split("/")[3].split("-")[0]
vid1StartTime = (int(vid1StartTimestr.split(".")[0])  * 1000) + int(vid1StartTimestr.split(".")[1][:3])

print(vid1StartTime)


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

#loop through all IMU values and build a list of timestamps for them
IMUTimestamps = []
EulerRoll = []

#build an angel for frame list by iterating through the frame timestamps and averaging the Euler angles from them
angleForFrame = []
for t in 


out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1440,1440))

for f in vid1f:

    imutils.rotate(f, angle)

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