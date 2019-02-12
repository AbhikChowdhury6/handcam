#!/bin/bash
t="$(date +"%d-%m-%Y-%H-%M-%S.%N")"

name=/home/pi/handcam-camera-$t.h264
echo $name
raspivid -t 0 -n -w 1280 -h 720 -hf -ih -fl -fps 30 -o $name 
