import logging
import os
import sys
import time

from imuDaemon import ImuDaemon


if __name__ == '__main__':

    action = sys.argv[1]
    
    ilogfile = os.path.join(os.getcwd(), "imu.log")
    ipidfile = os.path.join(os.getcwd(), "imu.pid")

    logging.basicConfig(filename=ilogfile, level=logging.DEBUG)
    imuD = ImuDaemon(pidfile=ipidfile)

    if action == "start":

        imuD.start()

    elif action == "stop":

        imuD.stop()

    elif action == "restart":

        imuD.restart()