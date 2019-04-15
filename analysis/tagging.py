#iterate through the video back and forth displaying the frame and frame number (as df)
#and give them option to tag (1234) (0 to remove)

import cv2

#vid1 = sys.argv[1]

vid1 = '/home/chowder/1550594841.134619449-handcam-topcamera.mp4'


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

#cv2.destroyAllWindows()