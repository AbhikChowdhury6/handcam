import pygame
import pygame.camera
from pygame.locals import *

import requests
import base64
import sys

pygame.init()
pygame.camera.init()

url=sys.argv[1]#"http://0.0.0.0:5000/upload/"

camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0],(640,480))

cam.start()

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
