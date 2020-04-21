import logging
import os
import sys
import time

from videoDaemon import VidDaemon


if __name__ == '__main__':

    action = sys.argv[1]
    
    vlogfile = os.path.join(os.getcwd(), "vid.log")
    vpidfile = os.path.join(os.getcwd(), "vid.pid")

    logging.basicConfig(filename=vlogfile, level=logging.DEBUG)
    vidD = VidDaemon(pidfile=vpidfile)

    if action == "start":

        vidD.start()

    elif action == "stop":

        vidD.stop()

    elif action == "restart":

        vidD.restart()