from math import degrees
from time import sleep
import time
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

while True:
    if imu.IMURead():
        data = imu.getIMUData()
        fusionPose = data["fusionPose"]
        accel=data["accel"]
        gyro=data["gyro"]
        mag=data["compass"]

        global roll, pitch, yaw, accelX,accelY,accelZ,gyroX,gyroY,gyroZ, magX,magY,magZ
        roll = round(degrees(fusionPose[0]),2)
        pitch = round(degrees(fusionPose[1]),2)
        yaw = round(degrees(fusionPose[2]),2)
        accelX=round(accel[0],2)
        accelY=round(accel[1],2)
        accelZ=round(accel[2],2)
        gyroX=round(gyro[0],2)
        gyroY=round(gyro[1],2)
        gyroZ=round(gyro[2],2)
        magX=round(mag[0],2)
        magY=round(mag[1],2)
        magZ=round(mag[2],2)

        timeStamp=round((time.time()-startTime),3)


        #print(str(accelX) + "   " + str(accelY) + "   " + str(accelZ)+"  "+str(gyroX) + "   " + str(gyroY) + "   " + str(gyroZ))
        print(str(timeStamp)+" "+str(roll) + "   " + str(pitch) + "   " + str(yaw))
        #print(str(timeStamp)+"  "+str(accelX) + "  " + str(accelY) + "  " + str(accelZ))
        sleep(poll_interval*1.0/1000.0) 
