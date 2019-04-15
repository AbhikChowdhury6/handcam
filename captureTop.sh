#!/bin/bash

#usage 
#first arg is trial number ex 1,2,3
#second is the person on the network to send the data to in ssh format

trialNumber=$1
placeToSend=$2

trap 'kill %1;' SIGINT
bash /home/pi/handcam/VideoCap.sh $trialNumber topCam & python3 /home/pi/handcam/BNOlogging.py $trialNumber #& python /home/pi/handcam/logSerialPressure.py $trialNumber 

bash /home/pi/handcam/send.sh $trialNumber $placeToSend topCam