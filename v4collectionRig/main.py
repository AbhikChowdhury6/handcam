#states
    #standby--------------------flashing green--------after bootup and when the button is clicked while recording
    #recording -----------------flashing red----------a quick click from the button
    #recording with light ------flashing amber--------a 1 second click of the button
    #####################debug mode with wifi ------solid white-----------a 10 second click from the button ----- reboot device to exit
    #transfering data  ---------solid blue---------plug in a USB drive with space available
    ##############done transferring ---------solid blue------------unplug the USB to resume normal operation


    #error states
        ############local memory full -----------------three purple flashes-----plug in a USB drive with space available, wait for transfer, then record
        #############sense drive but can't transfer ----solid teal---------------make sure the drive has space and is the right format
        #############searching for wifi ----------------flashing white-----------make sure the wifi network is on and the credintals are correct
        ###############internal error---------------------solid red----------------enter debug mode, ssh in and poke around to see if sensors are connected
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
                                                                                    # retrieve size of files to transfer
                                                                                    # retrive available space on USB
                                                                                    # encrypt relevant files
    #zip files
    #transfer 

#async TODO's
    #video daemon
    #IMU daemon


import time
import board
import neopixel
import os
import RPi.GPIO as GPIO   
import logging

# mlogfile = os.path.join(os.getcwd(), "main.log")
# logging.basicConfig(filename=mlogfile, level=logging.DEBUG)


GPIO.setmode(GPIO.BCM)           # Set's GPIO pins to BCM GPIO numbering
INPUT_PIN = 4          
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#set up the other side of the button
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)

pixels = neopixel.NeoPixel(board.D18, 2)


LEDoutput = (0,0,0)
recLightBrightness = 0
statBrightness = 102

recording=False
green = statBrightness
red = 0

loopCount = 0
buttonPushedCount = 0

transfered = False



print("about to enter loop")
#fixed time loop @ 10HZ
while(True):
    loopCount = loopCount + 1  

    #Check if button is being pushed
    if(GPIO.input(INPUT_PIN)):
        print("button pushed")
        buttonPushedCount = buttonPushedCount + 1 
        if(buttonPushedCount == 1):
            recording = not recording
            
            if(not recording):
                green = statBrightness
                red = 0
                recLightBrightness = 0
            
                os.system("python3 vidController.py stop")
                os.system("python3 imuController.py stop")
                print("stopped both processes")

                transfered = False
            
            else:
                LEDoutput = (statBrightness,0,0)
                red = statBrightness
                green= 0
            
                os.system("python3 imuController.py start")
                os.system("python3 vidController.py start")
                print("started both processes")

        
        if(buttonPushedCount == 10):
            green = statBrightness
            recLightBrightness = 255
            print("turning on light")
    else:
        buttonPushedCount = 0


    #sense the usb and not transfered
    usbName = os.listdir("/media/pi/")
    if(not transfered and usbName != []):
        print("starting Transfer")
        #set to blue
        pixels[0] = ( 0,0,statBrightness)
        recLightBrightness = 0
        
        #stop recordings if they're happening
        if(recording):
            recording=False
            os.system("python3 vidController.py stop")
            os.system("python3 imuController.py stop")
        time.sleep(2)
        
        #make all files if theyre not already there
        os.system("mkdir /home/pi/export && mkdir /home/pi/export2 && /home/pi/export3")

        #move old export2 file to export3 and delete
        os.system("rm /home/pi/export3/* && mv /home/pi/export2/* /home/pi/export3/")

        #move old export file to export2 for safe keeping
        os.system("mv /home/pi/export/* /home/pi/export2")
        
        #move the data folder to export and make a new data folder for next time
        os.system("cd /home/pi/ && zip -r /home/pi/export/" + str(time.time()) + ".zip data")

        #remove items in the data folder
        os.system("rm -r /home/pi/data/ && mkdir /home/pi/data")

        #zip the export folerfolder and put it on the USB
        os.system("cp /home/pi/export/* /media/pi/" + usbName[0] + "/")

        os.system("eject /dev/sda1")
        

        transfered = True
        green = statBrightness
        red = 0

        #reset recording number to zero
        vidNF = open( "/home/pi/vidnum.txt", "w")
        vidNF.write("0")
        vidNF.close()

        print("finished Transfer")


    LEDoutput = (red,green,0)

    if(loopCount%10<5):
        LEDoutput = (0,0,0)
#        print("FLASH")

    pixels[0] = LEDoutput
    pixels[1] = (recLightBrightness,recLightBrightness,recLightBrightness)
    #wait for a bit
    time.sleep(.1)

    
