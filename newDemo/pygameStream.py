import pygame
import pygame.camera
from pygame.locals import *


import socket
import sys
import struct

serverAddr = sys.argv[1]
pictureW = sys.argv[2]
pictureH = sys.argv[3]


pygame.init()
pygame.camera.init()

camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0],(480,480))

cam.start()


client_socket = socket.socket()
client_socket.connect((serverAddr, 777))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    
        image = cam.get_image()

        connection.write(image)
        connection.flush()


    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
