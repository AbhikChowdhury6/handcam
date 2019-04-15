#!/bin/bash

#usage 
#first arg is trial number ex 1,2,3
#second is device name (topcam bottomcam)
#third is the person on the network to send the data to in ssh format

trialNumber = $1
placeToSend = $2

trap 'kill %1;' SIGINT
bash VideoCap.sh $trialNumber topCam & python IMUlogging.py $trialNumber & python logSerialPressure.py $trialNumber 

bash send.sh $trialNumber $placeToSend topCam