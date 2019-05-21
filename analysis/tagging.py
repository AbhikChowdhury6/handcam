#iterate through the video back and forth displaying the frame and frame number (as df)
#display the graphs of all the data streams with the current timestap displayed as a vertical line

import matplotlib.pyplot as plt
import sys
import fnmatch
import os
import cv2

plt.ion()

baseFolder = sys.argv[1]


scale_percent = 30 # percent of original size
captureHeight = 1440 
captureWidth = 1440
width = int(captureHeight * scale_percent / 100)
height = int(captureHeight * scale_percent / 100)
dim = (width, height)


for file in os.listdir(baseFolder):
    if fnmatch.fnmatch(file,'*topCam*.mp4'):#top camera
        TopCamf = file
        print(TopCamf)
    if fnmatch.fnmatch(file,'*bottomCam*.mp4'):#bottom camera
        BottomCamf = file
        print(BottomCamf)
    if fnmatch.fnmatch(file,'*ACCEL*'):#accel
        Accelf = file
        print(Accelf)
    if fnmatch.fnmatch(file,'*LINACCEL*'):#linAccel
        LinAccelf = file
        print(LinAccelf)
    if fnmatch.fnmatch(file,'*GRAV*'):#grav
        Gravf = file
        print(Gravf)
    if fnmatch.fnmatch(file,'*MAG*'):#MAG
        Magf = file
        print(Magf)
    if fnmatch.fnmatch(file,'*EULERA*'):#euler
        Eulerf = file
        print(Eulerf)
    if fnmatch.fnmatch(file,'*GYRO*'):#gyro
        Gyrof = file
        print(Gyrof)
    if fnmatch.fnmatch(file,'*PARRAY3*'):#pressure
        Pressuref = file
        print(Pressuref)

lim = 300
#import topcam Data
#topCamStartTimestr = TopCamf.split("-")[0]
#topCamStartTime = (int(topCamStartTimestr.split(".")[0])  * 1000) + int(topCamStartTimestr.split(".")[1][:3])
#print(topCamStartTime)
topCami = []
frameNum = 0
topCap = cv2.VideoCapture(baseFolder+TopCamf)
while(topCap.isOpened() and len(topCami) < lim):
    frame_exists, curr_frame = topCap.read()
    if frame_exists:
        topCami.append(curr_frame)
    else:
        break

print("imported topCam:" + str(len(topCami)))

#import bottomCam data
#bottomCamStartTimestr = BottomCamf.split("/")[3].split("-")[0]
#bottomCamStartTime = (int(bottomCamStartTimestr.split(".")[0])  * 1000) + int(bottomCamStartTimestr.split(".")[1][:3])
#print(bottomCamStartTime)
bottomCami = []
bottomCap = cv2.VideoCapture(baseFolder+BottomCamf)
while(bottomCap.isOpened() and len(bottomCami) < lim):
    frame_exists, curr_frame = bottomCap.read()
    if frame_exists:
        bottomCami.append(curr_frame)
    else:
        break

print("imported bottomCam" + str(len(bottomCami)))


#import accel
accel = [[],[],[]]
with open(baseFolder+Accelf, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for i, t in enumerate(tuples):
    elements = t.split(",")
    accel[0].append(elements[0])
    accel[1].append(elements[1])
    accel[2].append(elements[2])
    if(len(accel[0])>lim*(100/30)):
        break
print("accel:" + str(len(accel[0])))

#import linAccel
linAccel = [[],[],[]]
with open(baseFolder+LinAccelf, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    linAccel[0].append(elements[0])
    linAccel[1].append(elements[1])
    linAccel[2].append(elements[2])
    if(len(linAccel[0])>lim*(100/30)):
        break
print("linAccel:" + str(len(linAccel[0])))

#import grav
grav = [[],[],[]]
with open(baseFolder+Gravf, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    grav[0].append(elements[0])
    grav[1].append(elements[1])
    grav[2].append(elements[2])
    if(len(grav[0])>lim*(100/30)):
        break
print("grav:" + str(len(grav[0])))

#import mag
mag = [[],[],[]]
with open(baseFolder+Magf, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    mag[0].append(elements[0])
    mag[1].append(elements[1])
    mag[2].append(elements[2])
    if(len(mag[0])>lim*(100/30)):
        break
print("mag:" + str(len(mag[0])))

#import euler
euler = [[],[],[]]
with open(baseFolder+Eulerf, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    euler[0].append(elements[0])
    euler[1].append(elements[1])
    euler[2].append(elements[2])
    if(len(euler[0])>lim*(100/30)):
        break
print("euler:" + str(len(euler[0])))

#import gyro
gyro = [[],[],[]]
with open(baseFolder+Gyrof, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    gyro[0].append(elements[0])
    gyro[1].append(elements[1])
    gyro[2].append(elements[2])
    if(len(gyro[0])>lim*(100/30)):
        break
print("gyro:" + str(len(gyro[0])))

#import pressure
pressure = [[],[],[]]
with open(baseFolder+Gyrof, 'r') as myfile:
    raw=myfile.read()
tuples = raw.split("),(")
for t in tuples:
    elements = t.split(",")
    pressure[0].append(elements[0])
    pressure[1].append(elements[1])
    pressure[2].append(elements[2])
    if(len(pressure[0])>lim*(100/30)):
        break
print("pressure:" + str(len(pressure[0])))



numStreams = 7 + 1 #including video frame
#generate graphs
#main title is the experement number and name
#sub plots for each stream
def plotaccel(targetSample):
    plt.subplot(numStreams,1,1)
    plt.cla()
    plt.ylabel('accel m/s^2')
    plt.xlabel('Samples')
    plt.plot(accel[0])
    plt.plot(accel[1])
    plt.plot(accel[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def plotlinAccel(targetSample):
    plt.subplot(numStreams,1,2)
    plt.cla()
    plt.xlabel('Samples')
    plt.plot(linAccel[0])
    plt.plot(linAccel[1])
    plt.plot(linAccel[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def plotgrav(targetSample):
    plt.subplot(numStreams,1,3)
    plt.cla()
    plt.ylabel('m/s^2')
    plt.xlabel('Samples')
    plt.plot(grav[0])
    plt.plot(grav[1])
    plt.plot(grav[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def plotmag(targetSample):
    plt.subplot(numStreams,1,4)
    plt.cla()
    plt.ylabel('mTesla')
    plt.xlabel('Samples')
    plt.plot(mag[0])
    plt.plot(mag[1])
    plt.plot(mag[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def ploteuler(targetSample):
    plt.subplot(numStreams,1,5)
    plt.cla()
    plt.title('euler')
    plt.ylabel('degrees')
    plt.xlabel('Samples')
    plt.plot(euler[0])
    plt.plot(euler[1])
    plt.plot(euler[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def plotgyro(targetSample):
    plt.subplot(numStreams,1,6)
    plt.cla()
    plt.ylabel('rad/s^2')
    plt.xlabel('Samples')
    plt.plot(gyro[0])
    plt.plot(gyro[1])
    plt.plot(gyro[2])
    plt.legend(['X', 'Y', 'Z'], loc='upper left')
    plt.axvline(x=targetSample)

def plotpressure(targetSample):
    plt.subplot(numStreams,1,7)
    plt.cla()
    plt.ylabel('realitive')
    plt.xlabel('Samples')
    plt.plot(pressure[0])
    plt.plot(pressure[1])
    plt.plot(pressure[2])
    plt.legend(['P1', 'P2', 'P3'], loc='upper left')
    plt.axvline(x=targetSample)

def plotvid(targetSample):
    plt.subplot(numStreams,1,8)
    plt.cla()
    plt.plot([0]*len(topCami))
    plt.axvline(x=targetSample)


cmd = ""
frame = 0
tags = {}
# import data as points and make a list of timestamps for each
# graph all of the data streams
# update the lines based on the current frames timestamp

#show both top and bottom frames
targetSample = 0
plotaccel(targetSample)
ploteuler(targetSample)
plotgrav(targetSample)
plotgyro(targetSample)
plotlinAccel(targetSample)
plotmag(targetSample)
plotpressure(targetSample)
plotvid(frame)
plt.draw()

while cmd != "q":
    cmd = input("enter cmd: ")
    if cmd == "a":
        frame -= 10
    if cmd == "s":
        frame -= 1
    if cmd == "d":
        frame += 1
    if cmd == "f":
        frame += 10
    if cmd == "g":
        frame += 100
    if cmd.isnumeric():
        tags[frame] = cmd
    if cmd == "x":
        tags.pop(frame)
    if frame < 0:
        frame = 0
    if frame >= len(bottomCami):
        frame = len(bottomCami)-1
    if frame < 0:
        frame = 0
    #display the frames
    #cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('topCam',cv2.resize(topCami[frame], dim, interpolation = cv2.INTER_AREA))
    cv2.imshow('bottomCam',cv2.resize(bottomCami[frame], dim, interpolation = cv2.INTER_AREA))
    targetSample = int(frame*(100/30))
    #update all of the graphs

    


    cv2.waitKey(2)


#cv2.destroyAllWindows()