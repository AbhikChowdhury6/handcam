import pygame
import pygame.camera
from pygame.locals import *

import os

import requests
import base64
import sys

import time
pygame.init()
pygame.camera.init()

url=sys.argv[1]#"http://0.0.0.0:5000/upload/"

camlist = pygame.camera.list_cameras()
print(camlist)

#cam = pygame.camera.Camera("/dev/video0",(384,288))
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
#cam.start()
#while True:
#    try:
#        cam.start()
#        break
#    except Exception as e:
#        print(start= Except, e)
#        time.sleep(1)


#cam.start()

#image = cam.get_image()
#pygame.image.save(image,"f1.jpg")
os.system("fswebcam f1.jpg")


print("saved!")
image_path = "f1.jpg"
b64_image = ""
# Encoding the JPG,PNG,etc. image to base64 format
with open(image_path, "rb") as imageFile:
    b64_image = base64.b64encode(imageFile.read())

# data to be sent to api
data = {'b64': b64_image}

# sending post request and saving response as response object
r = requests.post(url=url, data=data)
