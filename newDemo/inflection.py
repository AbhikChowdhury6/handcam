import requests
import time
import sys

import pygame
import pygame.camera
from pygame.locals import *

from busio import I2C
from board import SDA, SCL
import adafruit_bno055


serverAddr = sys.argv[1]


pygame.init()
pygame.camera.init()


i2c = I2C(SCL, SDA)

address = 0x28
IMU = adafruit_bno055.BNO055(i2c,address)



camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0],(640,480))

cam.start()


starttime=time.time()
lastTime = time.time()

while True:
    #read IMU
    #signal processing
    #take picture


    IMU.accelerometer



    image = cam.get_image()
    pygame.image.save(image,"f1.jpg")

    image_path = "f1.jpg"
    b64_image = ""
    # Encoding the JPG,PNG,etc. image to base64 format
    with open(image_path, "rb") as imageFile:
        b64_image = base64.b64encode(imageFile.read())

    # data to be sent to api
    data = {'b64': b64_image}

    # sending post request and saving response as response object
    r = requests.post(url=url, data=data)
    lastTime = time.time()
    time.sleep(0.05 - ((time.time() - starttime) % 0.05))




