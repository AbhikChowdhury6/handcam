#iterate through the video back and forth displaying the frame and frame number (as df)
#and give them option to tag (1234) (0 to remove)

import cv2
import pickle
#vid1 = sys.argv[1]

vid1 = '/home/chowder/Documents/1550419316.586681638-handcam-topCamera.mp4'


vid1i = []
vid1Timestamps = []
cap1 = cv2.VideoCapture(vid1)

while(cap1.isOpened()):
    frame_exists, curr_frame = cap1.read()
    if frame_exists:
        vid1i.append(curr_frame)
    else:
        break

cmd = ""
frame = 0
tags = {}

while cmd != "q":
    cmd = input("enter cmd")
    if cmd == "a":
        frame -= 10
    if cmd == "s":
        frame -= 1
    if cmd == "d":
        frame += 1
    if cmd == "f":
        frame += 10
    if cmd.isnumeric():
        tags[frame] = cmd
    if cmd == "x":
        tags.pop(frame)
    if frame < 0:
        frame = 0
    if frame >= len(vid1i):
        frame = len(vid1i)-1
    #display the frame
    cv2.imshow('Image',vid1i[frame])
    cv2.waitKey(2)


#write tags to a file
pickle.dump(tags,"tags.p", "wb")
#TAGS_f = open( "tags.csv", "a+")

#cv2.destroyAllWindows()