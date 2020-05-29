#import sys, getopt
#sys.path.append('.')
#import os.path

import time
from math import degrees
from time import sleep

try:
    import RTIMU
except ImportError:
    RTIMU = None

SETTINGS_FILE = "RTIMULib"

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

if (not imu.IMUInit()):
  print("IMU init failed")
  exit(1)
else:
  print("IMU init succeeded")

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()

while True:
	if imu.IMURead():
		data = imu.getIMUData()
		fusionPose = data["fusionPose"]
		accel=data["accel"]
		gyro=data["gyro"]
		mag=data["compass"]

		global accelX,accelY,accelZ,gyroX,gyroY,gyroZ,roll,pitch,yaw

		accelX=round(accel[0],2)
		accelY=round(accel[1],2)
		accelZ=round(accel[2],2)
		gyroX=round(gyro[0],2)
		gyroY=round(gyro[1],2)
		gyroZ=round(gyro[2],2)
		roll = round(degrees(fusionPose[0]),2)
		pitch = round(degrees(fusionPose[1]),2)
		yaw = round(degrees(fusionPose[2]),2)

		timeStamp=time.time()

		print(str(accelX) + "  " + str(accelY) + "  " + str(accelZ))
		#print(str(gyroX) + "   " + str(gyroY) + "   " + str(gyroZ))
		#print(str(roll) + "   " + str(pitch) + "   " + str(yaw))
		sleep(poll_interval*1.0/1000.0) 
