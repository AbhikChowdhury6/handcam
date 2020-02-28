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


#recording TODO's
    #check available space on device

#Wifi debug TODO's
    #turn wifi on
    #check if wifi is connected

#USB transfer TODO;s
    #check if USB drive is connected
    #retrieve size of files to transfer
    #retrive available space on USB


#async TODO's
    #start an async process
    #async transfer script
    #async record script


#general TODO's
    #add wait code
    #led code


standby = True

LEDoutput = black

loopCount = 0
flashing=True

buttonPushedCount = 0
execute = True

recording= False
recLight= False

transferring = False

wifiDebug = False
wifiOff=True
wifiConnected = False

canIRecord=True
amIRecording=False


#fixed time loop @ 10HZ
while(True):
    #set color green
    flashing=True

    #execute command 
    if(execute):
        if(not standby and buttonPushedCount>0):
            standby= True
            if(amIRecording):
                #stop recording
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
            canIRecord=False
        #else
            if(canIRecord and not amIRecording):
                pid = #start async recording #is there an error with starting the recording
                if(not pid):
                    #set to red, show and exit program
                amIRecording=True
        #set color red
        flashing=True
            

    if(recLight):
        #turn on recLight
        #set color amber
        flashing=True


    if(wifiDebug):
        if(wifiOff):
            #turn on wifi
        #test wifi connecttion
        #set color white
        flashing=True
        if(wifiConnected):
            #set color white, show, and exit the program

    
    #Check if button is being pushed
    if(button and not wifiConnected):
        execute=False
        buttonPushedCount = buttonPushedCount + 1 

    else:
        execute=True
        buttonPushedCount = 0

    #check if USB is connected 
        buttonPushedCount = 0 #block other commands
        #set color to blue
        #check to see if you have any files to transfer
            #check if you're already transferring
                #check if you have files to transfer and if there is space on the USB for all of your files
                    #initiate async transfer
                    transfering=True
                    flashing=True
                #else
                    #set to teal
                    flashing = False
        #else:
            transfering=False

        
    
    if(flashing):
        if(loopCount%10<5):
            #set color black

    #write LED state

    #wait for a bit

    