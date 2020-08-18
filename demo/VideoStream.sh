#!/bin/bash
#mplayer -fps 30 -demuxer h264es ffmpeg://tcp://192.168.1.102:2222
#raspivid -t 0 -n -w 720 -h 720 -ih -fl -fps 20 -o - | nc -k -l 2222
raspivid -t 0 -n -w 720 -h 720 $2 $3 $4 $5 -ih -fl -fps 20 -o - | nc -k -l $1
