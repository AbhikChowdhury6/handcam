import time
import csv
import RTIMU
from math import degrees
import logging


from daemons.prefab import run

class ImuDaemon(run.RunDaemon):

    def run(self):
        # idlogfile = os.path.join(os.getcwd(), "IMUDaemon.log")
        # logging.basicConfig(filename=idlogfile, level=logging.DEBUG)

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
        
        f=open("/home/pi/data/IMU.csv",mode='a')
        w=csv.writer(f,delimiter=',')

        while True:
            lastTime = time.time()
            #append datapoint to csv
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

                timeStamp=round((time.time()),3)

                #print(str(timeStamp)+"  "+str(accelX) + "  " + str(accelY) + "  " + str(accelZ))
                w.writerow([timeStamp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,roll,pitch,yaw])
                time.sleep(poll_interval*(1.0/1000.0))
                #print(time.time()-lastTime)
