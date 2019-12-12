import requests
import base64

import numpy as np

import os

import subprocess

import time
import sys
import threading

from gpiozero import LED

import board
import busio
import adafruit_bno055
i2c = busio.I2C(board.SCL, board.SDA)
IMU = adafruit_bno055.BNO055(i2c)

led = LED(21)

url = sys.argv[1]

lastN = sys.argv[2]

#epsilon for judging zero of an inflectionEPS = 3.0
EPS = 2.2
Fs = 20
sr = 1.0 / Fs
pre_conv_kernel = 3 
post_conv_kernel = 2 
# length of time for an inflection point sample
INF_LEN = 3 
#gravitational constant in phoenix
G_PHX = 9.802

buffer_len = INF_LEN*2 + pre_conv_kernel + post_conv_kernel - 2

starttime=time.time()
lastTime = time.time()
	


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


LAST_GOOD_GRAV = np.array([0,0,0,0])

def get_data(sensor, prev, mask = 100):
	acd = np.array(sensor.linear_acceleration)
	gyd = np.array(sensor.gyro)
	#grd = np.array(sensor.quaternion)
	#print(str(acd) + "\t" + str(gyd))
	if(acd[0] == None):
		acd = mask+1 
	# remove outliers
	acd = acd * (acd <= mask) + prev[0] * (acd > mask)
	gyd = gyd * (gyd <= mask) + prev[1] * (gyd > mask)

	return acd, gyd

def get_data_fast(sensor, prev, mask = 100):
	acd = np.array(sensor.acceleration)
	gyd = np.array(sensor.gyro)
	grd = np.array(sensor.gravity)
	#print(str(acd) + "\t" + str(gyd))
	if(acd[0] == None):
		acd = mask+1 
	# get prev grav
	if None in grd or np.abs(np.sqrt(np.sum(grd*grd))-G_PHX) > 0.1:
		grd = np.array([0,0,0])
	acd = acd * (acd <= mask) + prev[0] * (acd > mask)
	gyd = gyd * (gyd <= mask) + prev[1] * (gyd > mask)
	return acd, gyd, grd

def interp_grav(data):
	grav_mag = np.sqrt(np.sum(data*data,axis=1))
	outliers = np.where(np.abs(grav_mag - G_PHX) > 0.01) [0]
	#init_errs = np.where(grav_mag == 0)
	
	#data[outliers] = (data[outliers-1] + data[outliers+1]) / 2

	outliers_left = outliers - 1
	outliers_right = outliers + 1
	outliers_left = outliers_left * (outliers_left >= 0) + outliers_right * (outliers_left < 0)
	outliers_right = outliers_right * (outliers_right < outliers.shape[0]) + outliers_left * (outliers_right >= outliers.shape[0])	
	data[outliers] = (data[outliers_left] + data[outliers_right]) / 2

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
	#print(np.transpose(inf_pt),end='\r')
	pos_sl = np.sum(inf_pt[-INF_LEN:]) >= INF_LEN-1 and np.sum(inf_pt[-2*INF_LEN:-INF_LEN])  <= 1
	neg_sl = np.sum(inf_pt[-INF_LEN:]) <= 1 and np.sum(inf_pt[-2*INF_LEN:-INF_LEN]) > INF_LEN-1
	return pos_sl or neg_sl

acd = np.array([0,0,0])
gyd = np.array([0,0,0])
grd = np.array([0,0,0])

acc_buffer = simple_buffer(buffer_len)
gyr_buffer = simple_buffer(buffer_len)
grv_buffer = simple_buffer(buffer_len)

camera_tread = False
prev_inf = time.time()
while True:
	#read IMU
	#signal processing
	#take picture

	# collect the data
	acd, gyd, grd = get_data_fast(IMU, (acd,gyd,grd))	
	# buffer
	acc_buffer.update(acd)
	gyr_buffer.update(gyd)
	grv_buffer.update(grd)
	print("{}".format(np.sqrt(np.sum(grd*grd))))

	if acc_buffer.ready() and gyr_buffer.ready():
		# smooth gravity
		gyrLP = lowpass(gyr_buffer.report(), pre_conv_kernel)
		accLP = lowpass(acc_buffer.report(), pre_conv_kernel)
		grvLP = lowpass(interp_grav(grv_buffer.report()), pre_conv_kernel)
		#print("{},{}".format(accLP, grvLP))
		inflection = find_inf_pt(accLP - grvLP, gyrLP, eps=EPS)
		if inflection and time.time()-prev_inf > 0.5:
			prev_inf = time.time()
			print("Inflection point at {}".format(time.time()))
			subprocess.call(["python3","sendLastn.py",url,str(lastN),str(0.7)])
			# if this introduces a lag, these can be invoked
#			time.sleep(2)
			#send_picture(url)
#			time.sleep(2)
#			acc_buffer.flush()
#			gyr_buffer.flush()
#			grv_buffer.flush()
	lastTime = time.time()
	time.sleep(sr - ((time.time() - starttime) % sr))




