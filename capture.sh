#!/bin/bash

trap 'kill %1;' SIGINT
bash VideoCap.sh $1 $2 & python IMUlogging.py $1 $2

bash send.sh