import time

from daemons import daemonizer

@daemonizer.run(pidfile="/tmp/sleepy.pid")
def rec(cv,imu):

    while True:
        #create files for Session, Data

        
        #start 15 second recordings
        vidRec(cv, fn)
        vidRec(imu, fn)
        
        #wait 15 seconds
        time.sleep(15)

@daemonizer.run(pidfile="/tmp/sleepy.pid")
def vidRec(cv, fn):
    starttime = time.time()
    #cature first frame and save it to Session and data
    while True:
        #capture frame and save it to the data folder
        
        
        if(time.time()-starttime > 15):
            break

@daemonizer.run(pidfile="/tmp/sleepy.pid")
def imuRec(imu, fn):
    starttime = time.time()
    while True:
        #append datapoint to csv
        
       
        if(time.time()-starttime > 15):
            break


#initialize camera and IMU

rec