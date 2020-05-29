import time
import cv2

from daemons.prefab import run

class VidDaemon(run.RunDaemon):

    def run(self):
        print("starting Video Rec")
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while True:
            lastTime = time.time()
            ret, frame = cam.read()
            if (ret):
                cv2.imwrite("/home/pi/data/" + str(time.time()) + ".jpg", frame)
            #print(time.time()-lastTime)
