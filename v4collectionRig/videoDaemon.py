import time
import cv2

from daemons.prefab import run

class VidDaemon(run.RunDaemon):

    def run(self):
        print("starting Video Rec")
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        vidNF = open( "vidnum.txt", "r")
        vidNum = int(vidNF.read())
        vidNF.close()

        vidNF = open( "vidnum.txt", "w")
        vidNF.write(str(vidNum + 1))
        vidNF.close()

        
        while True:
            lastTime = time.time()
            ret, frame = cam.read()
            if(ret):
                cv2.imwrite("/home/pi/data/" + str(time.time()) + "-" + str(vidNum) +".jpg", frame)
            #print(time.time()-lastTime)