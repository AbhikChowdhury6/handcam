#!/bin/bash
#mplayer -fps 30 -demuxer h264es ffmpeg://tcp://192.168.1.102:2222
raspivid -t 0 -n -w 1280 -h 720 $3 -ih -fl $2 -fps 20 -o - | nc -k -l $1
