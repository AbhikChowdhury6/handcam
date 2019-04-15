#!/bin/bash
#t="$(date +"%d-%m-%Y-%H-%M-%S.%N")"
t="$(date +"%s.%N")"
name=/home/pi/data/$1-$2-$t
echo $name
raspivid -t 0 -n -w 1440 -h 1440 $3 $4 $5-ih -fl -fps 30 -o $name.h264

MP4Box -add $name.h264 $name.mp4

rm $name.h264
