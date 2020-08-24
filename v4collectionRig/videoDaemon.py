import time
import cv2
import logging
import os

from daemons.prefab import run

class VidDaemon(run.RunDaemon):

    def run(self):
        # vdlogfile = os.path.join(os.getcwd(), "VidDaemon.log")
        # logging.basicConfig(filename=vdlogfile, level=logging.DEBUG)
        print("starting Video Rec")
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        vidNF = open( "/home/pi/vidnum.txt", "r")
        vidNum = int(vidNF.read())
        vidNF.close()

        vidNF = open( "/home/pi/vidnum.txt", "w")
        vidNF.write(str(vidNum + 1))
        vidNF.close()

        
        while True:
            lastTime = time.time()
            ret, frame = cam.read()
            if(ret):
                t = str(time.time()).split(".")
                t[1] = t[1] + "000"
                cv2.imwrite("/home/pi/data/" + t[0] + "." + t[1][:3] + "-" + str(vidNum) +".jpg", frame)
            #print(time.time()-lastTime)

