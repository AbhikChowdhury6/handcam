#!/bin/bash

trap 'kill %1;' SIGINT
bash VideoCap.sh & python IMUlogging.py

