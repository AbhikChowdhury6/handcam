#!/bin/bash


trap 'kill %1;' SIGINT
python3 clientGrapher.py 192.168.43.55 0 Pressure1
& python3 clientGrapher.py 192.168.43.55 1 Pressure2
& python3 clientGrapher.py 192.168.43.55 2 Pressure3
& python3 clientGrapher.py 192.168.43.55 14 LinAccelX
& python3 clientGrapher.py 192.168.43.55 15 LinAccelY
& python3 clientGrapher.py 192.168.43.55 16 LinAccelz

