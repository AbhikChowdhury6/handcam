#!/bin/bash
#t="$(date +"%d-%m-%Y-%H-%M-%S.%N")"
t="$(date +"%s.%N")"
name=/home/pi/$t-$1-$2
echo $name
raspivid -t 0 -n -w 1920 -h 1080 -hf -ih -fl -fps 30 -o $name.h264

MP4Box -add $name.h264 $name.mp4

rm $name.h264
