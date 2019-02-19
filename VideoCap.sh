#!/bin/bash
#t="$(date +"%d-%m-%Y-%H-%M-%S.%N")"
t="$(date +"%s.%N")"
name=/home/pi/$t-$1-$2
echo $name
raspivid -t 0 -n -w 1280 -h 720 $3 $4 -ih -fl -fps 30 -o $name.h264

MP4Box -add $name.h264 $name.mp4

rm $name.h264
