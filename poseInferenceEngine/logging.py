import time
import math
from math import degrees
from time import sleep
import sys
import csv

import RTIMU

SETTINGS_FILE = "/home/pi/myProject/RTIMULib.ini"
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
startTime=time.time()

f=open("/home/pi/myProject/testLog.csv",mode='a')
w=csv.writer(f,delimiter=',')

try: 

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

            timeStamp=round((time.time()-startTime),3)

            print(str(timeStamp)+"  "+str(accelX) + "  " + str(accelY) + "  " + str(accelZ))
            w.writerow([timeStamp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,roll,pitch,yaw])
            sleep(poll_interval*1.0/1000.0) 

except KeyboardInterrupt:
    f.close()
    sys.exit()
    
