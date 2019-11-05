#!/bin/bash


#trap 'kill %1; kill %2; kill %3; kill %4; kill %5; kill %6;' SIGINT
trap 'kill %1; kill %2; kill %3;' SIGINT
python3 clientGrapher.py 192.168.43.55 0 Pressure1 &
python3 clientGrapher.py 192.168.43.55 1 Pressure2 &
python3 clientGrapher.py 192.168.43.55 2 Pressure3 &
python3 clientGrapher.py 192.168.43.55 15 LinAccelX &
python3 clientGrapher.py 192.168.43.55 16 LinAccelY &
python3 clientGrapher.py 192.168.43.55 17 LinAccelz

