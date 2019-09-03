import cv2
import math

#takes in the tags file
#takes in the video file

#is an object that has and parses all of them from a directory
    #RAWframes w/times
    #normalized frames
    #distance from object
    #rotation
    #tags w/ Times : motion started, object grabbed, object put down, returned
    #RAWIMUValues w/ Times
    #RAWPressureValues w/ Times


class handsDown:
    def __init__(self, topVid, bottomVid, IMUTimes, linAccel, eulerA, pressure, tags):
        self.topVid = topVid
        self.bottomVid = bottomVid
        self.IMUTimes = IMUTimes
        self.linAccel = linAccel
        self.eulerA = eulerA
        self.pressure = pressure
        self.tags = tags

        self.bottomFrameTimes = getTimes()
        self.distance = calcDistance()
        self.rotation = calcRotarion()
        self.topRotated = rotateVid(self.topVid, self.topRotated,self.rotation)
        self.bottomRotated = rotateVid(self.bottomVid, self.bottomRotated,self.rotation)

    def calcRotarion(self): #update algorithm to be more efficent if neccissary
        r = []
        best = math,inf
        for t in self.bottomFrameTimes:
            lastBesti = best
            best = math.inf
            for i in range(len(IMU):
                if abs(t-IMUTimes[i]) < best:
                    best
            r.append(self.eulerA[0][lastBesti])


