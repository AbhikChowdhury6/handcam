#states
    #standby--------------------flashing green--------after bootup and when the button is clicked while recording
    #recording -----------------flashing red----------a quick click from the button
    #recording with light ------flashing amber--------a 1 second click of the button
    #debug mode with wifi ------solid white-----------a 10 second click from the button ----- reboot device to exit
    #transfering data  ---------flsahing blue---------plug in a USB drive with space available
    #done transferring ---------solid blue------------unplug the USB to resume normal operation


    #error states
        #local memory full -----------------three purple flashes-----plug in a USB drive with space available, wait for transfer, then record
        #sense drive but can't transfer ----solid teal---------------make sure the drive has space and is the right format
        #searching for wifi ----------------flashing white-----------make sure the wifi network is on and the credintals are correct
        #internal error---------------------solid red----------------enter debug mode, ssh in and poke around to see if sensors are connected
        #battery dead-----------------------solid off----------------charge the battery


#boot TODO's
    #disable HDMI
        #/usr/bin/tvservice -o
    #disable activity LED
        #add to /boot/config.txt
            ## Disable the ACT LED on the Pi Zero.
            #dtparam=act_led_trigger=none
            #dtparam=act_led_activelow=on
    #disable Wifi
    #start this program

#recording TODO's
    #check available space on device
        #use subprocess with a grep and conditionals

#Wifi debug TODO's
    #turn wifi on
    #check if wifi is connected
        #will need to edit files and reboot for it to work

#USB transfer TODO;s
    #check if USB drive is connected
        #use sub proceeses for all of these
    #retrieve size of files to transfer
    #retrive available space on USB
    #encrypt relevant files
    #transfer 

#async TODO's
    #video daemon
    #IMU daemon



import time
import cv2
import board
import neopixel
import os
import csv
import RTIMU


pixels = neopixel.NeoPixel(board.D18, 2)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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

standby = True

LEDoutput = (0,0,0)

loopCount = 0
flashing=True

buttonPushedCount = 0
execute = True

recording= False
recLight= False
recLightBrightness = 255

transferring = False

wifiDebug = False
wifiOff=True
wifiConnected = False

canIRecord=True
amIRecording=False
recStartTime = time.time()-15

statBrightness = 255



@daemonizer.run(pidfile="/tmp/vidRec.pid")
def vidRec(cam, fn):
    starttime = time.time()
    #cature first frame and save it to Session and data
    ret, frame = cam.read()
    cv2.imwrite("/home/pi/data/" + fn + "/thumbnail.jpg", frame)
    cv2.imwrite("/home/pi/data/" + fn + "/data/" + str(time.time()) + ".jpg", frame)
    while True:
        #capture frame and save it to the data folder
        ret, frame = cam.read()
        cv2.imwrite(fn + "/" + str(time.time()) + ".jpg", frame)
        if(time.time()-starttime > 15):
            break

@daemonizer.run(pidfile="/tmp/sleepy.pid")
def imuRec(imu, fn):
    starttime = time.time()
    while True:
        #append datapoint to csv
        f=open("/home/pi/data/" + fn + "/data/IMU.csv",mode='a')
        w=csv.writer(f,delimiter=',')

        startTime=time.time()

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
        if(time.time()-starttime > 15):
            break



#fixed time loop @ 10HZ
while(True):
    #set color green
    LEDoutput = (0,statBrightness,0)
    flashing=True

    #execute command 
    if(execute):
        if(not standby and buttonPushedCount>0):
            standby= True
            if(amIRecording):
                #stop recording
                dvid.stop()
        else:
            standby=False
        
        if(buttonPushedCount>0):
            recording = True

        if(buttonPushedCount>10):
            recLight = True

        if(buttonPushedCount>100):
            recording = False
            recLight = False
            wifiDebug = True

        

    if(recording):
        #check how much local memory there is
        #if there's < 5 minutes of memory
            #flash purple three times
            for _ in range(3):
                pixels[0] = (statBrightness,0,statBrightness)
                time.sleep(.5)
                pixels[0] = (0,0,0)
            canIRecord=False
        #else
            if(canIRecord and not amIRecording):
                amIRecording=True
        #set color red
        LEDoutput = (statBrightness,0,0)
        flashing=True
            

    if(recLight):
        #turn on recLight
        #set color amber
        LEDoutput = (statBrightness,statBrightness,0)
        flashing=True


    if(wifiDebug):
        if(wifiOff):
            #turn on wifi
        #test wifi connecttion
        #set color white
        LEDoutput = (statBrightness,statBrightness,statBrightness)
        flashing=True
        if(wifiConnected):
            #set color white, show, and exit the program
            pixels[0] = (statBrightness,statBrightness,statBrightness)
            #exit

    
    #Check if button is being pushed
    if(button and not wifiConnected):
        execute=False
        buttonPushedCount = buttonPushedCount + 1 

    else:
        execute=True
        buttonPushedCount = 0



    #check if USB is connected 
    os.system("ls /media/pi/")
    if(res=="USBDrive" and standby and execute):
        #set color to blue
        LEDoutput = (0,0,statBrightness)
        #check to see if you have any files to transfer
        os.system("ls /home/pi/data")
            if(res!=""):
                #zip up files
                    #first all of the data folders and encrypt them and name it the timestamp
                    #zip up the whole session and name it the timestamp
                tot = 0
                fl = os.system("ls -l /home/pi/data/")
                for f in fl:
                    tot += int(f)
                #check if you have files to transfer and if there is space on the USB for all of your files
                
                    #initiate async transfer
                    transfering=True
                    flashing=True
                #else
                    #set to teal
                    LEDoutput = (0,statBrightness,statBrightness)
                    flashing = False
        #else:
            transfering=False

    

    if(amIRecording):
        if(time.time() - recStartTime > 15):
            fn = str(time.time())
            os.makedirs("/home/pi/" + fn)
            os.makedirs("/home/pi/" + fn + "/data/")

            vidRec(cv, fn)
            imuRec(imu, fn)
            recStartTime = time.time()

    
    if(flashing):
        if(loopCount%10<5):
            #set color black
            LEDoutput = (0,0,0)

    #write LED state
    pixels[0] = LEDoutput
    if(recLight):
        pixels[1] = (recLightBrightness, recLightBrightness, recLightBrightness)
    else:
        pixels[1] = (0, 0, 0)

    #wait for a bit
    time.sleep(.1)

    