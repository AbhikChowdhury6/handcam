#!/bin/bash

#usage 
#call from inside the data direcory like everything else
#call with trial num as first argument and where to send it to as second formatted the same as if you were to ssh

#Zip the data folder
#send the data folder named after the trial number dash date/time 



trialNum=$1
placeToSend=$2
deviceName=$3

t="$(date +"%s.%N")"

$filename=$deviceName-$trialNum-$t

cd ..

zip -r $filename.zip data

scp $trialNum*.zip $placeToSend:
rm -rf data
mkdir data
cd data
