#!/bin/bash
#mplayer -fps 30 -demuxer h264es ffmpeg://tcp://192.168.1.102:2222
raspivid -t 0 -n -w 1440 -h 1440 $2 $3 $4 $5 -ih -fl -fps 24 -o - | nc -k -l $1
