import requests
import base64

import time
import sys
import thread

from gpiozero import LED

import pygame
import pygame.camera
from pygame.locals import *

from busio import I2C
from board import SDA, SCL
import adafruit_bno055

led = LED(21)

url = sys.argv[1]

pygame.init()
pygame.camera.init()


i2c = I2C(SCL, SDA)

address = 0x28
IMU = adafruit_bno055.BNO055(i2c,address)
#epsilon for judging zero of an inflection
EPS = 0.3
pre_conv_kernel = 7
post_conv_kernel = 3
# length of time for an inflection point sample
INF_LEN = 3
#gravitational constant in phoenix
G_PHX = 9.802

buffer_len = INF_LEN*2 + pre_conv_kernel + post_conv_kernel - 2

camlist = pygame.camera.list_cameras()
if camlist:
	cam = pygame.camera.Camera(camlist[0],(640,480))

cam.start()


starttime=time.time()
lastTime = time.time()
	
def send_picture(cam, url):
    led.on()
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
    print(r)
    led.off()


class simple_buffer():
	def __init__(self, size):
		self.size = size
		self.list = []

	def update(self, data):
		if len(self.list) < self.size:
			self.list.append(data)
		else:
			self.list = self.list[1:] + [data]

	def report(self):
		return np.stack(self.list)

	def ready(self):
		return len(self.list) == self.size

	def flush(self):
		self.list = []

def get_data(sensor, prev, mask = 100):
	acd = np.array(sensor.accelerometer)
	gyd = np.array(sensor.gyroscope)
	grd = np.array(sensor.gravity)
	# remove outliers
	acd = acd * (acd <= mask) + prev[0] * (acd > mask)
	gyd = gyd * (gyd <= mask) + prev[1] * (gyd > mask)
	grd = grd * (grd <= mask) + prev[2] * (grd > mask)
	return acd, gyd, grd

def interp_grav(data):
	grav_mag = np.sqrt(np.sum(data*data,axis=1))
	outliers = np.where(np.abs(grav_mag - G_PHX) > 0.01) [0]
	#init_errs = np.where(grav_mag == 0)
	data[outliers] = (data[outliers-1] + data[outliers+1]) / 2
	#data[init_errs] = data[np.max(init_errs)+1]
	return data

def lowpass(data, kernel_size = 50, channels = 3):
	kernel = np.ones(kernel_size) / kernel_size
	convolved = []
	if channels > 1:
		for channel in range(channels):
			convolved.append(np.convolve(data[:,channel],kernel,'valid'))
	else:
		convolved = [np.convolve(data,kernel,'valid')]
	return np.transpose(np.stack(convolved))

def find_inf_pt(accel, gyro, eps = 0.001):
	accel_mag = lowpass(np.sqrt(np.sum(accel*accel,axis=1)),post_conv_kernel,1)
	gyro_mag = lowpass(np.sqrt(np.sum(gyro*gyro,axis=1)),post_conv_kernel,1)
	#inf_pt = np.logical_or(accel_mag < eps, gyro_mag < eps)
	inf_pt = 1 * (accel_mag < eps)
	pos_sl = np.sum(inf_pt[-INF_LEN:]) > INF_LEN/2 and np.sum(inf_pt[-INF_LEN:-INF_LEN]) < INF_LEN/2
	neg_sl = np.sum(inf_pt[-INF_LEN:]) < INF_LEN/2 and np.sum(inf_pt[-INF_LEN:-INF_LEN]) > INF_LEN/2
	return pos_sl or neg_sl

acd = np.array([0,0,0])
gyd = np.array([0,0,0])
grd = np.array([0,0,0])

acc_buffer = simple_buffer(buffer_len)
gyr_buffer = simple_buffer(buffer_len)
grv_buffer = simple_buffer(buffer_len)

while True:
	#read IMU
	#signal processing
	#take picture

	# collect the data
	acd, gyd, grd = get_data(IMU, (acd,gyd,grd))	
	# buffer
	acc_buffer.add(acd)
	gyr_buffer.add(gyd)
	grv_buffer.add(grd)

	if acc_buffer.ready() and gyr_buffer.ready() and grv_buffer.ready():
		# smooth gravity
		grvV = interp_grav(grv_buffer.report())
		gyrLP = lowpass(gyr.report(), pre_conv_kernel)
		accLP = lowpass(acc.report() - grvV, pre_conv_kernel)
		inflection = find_inf_pt(accLP, gyrLP, eps=EPS)
		if inflection:
			#thread.start_new_thread(send_picture, (cam, url))
			print("inflection at {}".format(time.time()))
			# if this introduces a lag, these can be invoked
			#acc_buffer.flush()
			#gyr_buffer.flush()
			#grv_buffer.flush()
	lastTime = time.time()
	time.sleep(0.05 - ((time.time() - starttime) % 0.05))




