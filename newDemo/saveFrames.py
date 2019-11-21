import cv2
import time
import os

folderName = str(time.time())
path = os.getcwd() + "/data/" + folderName

print(path)
#create folder with name of time
try:
    os.makedirs(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s" % path)


#capture image and save to folder named time
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    starttime = time.time()
    ret, frame = cam.read()
#    print(ret)
    cv2.imwrite(path + "/" + str(time.time()) + ".jpg", frame)
    time.sleep(0.05 - ((time.time() - starttime) % 0.05))
    print(time.time() - starttime)



