import time

from daemons.prefab import run

from mypackage import imuDaemon
from mypackage import vidDaemon


class SleepyDaemon(run.RunDaemon):

    def run(self):
        vlogfile = os.path.join(os.getcwd(), "vid.log")
        vpidfile = os.path.join(os.getcwd(), "vid.pid")

        logging.basicConfig(filename=vlogfile, level=logging.DEBUG)
        dvid = vidDaemon(pidfile=vpidfile)


        ilogfile = os.path.join(os.getcwd(), "imu.log")
        ipidfile = os.path.join(os.getcwd(), "imu.pid")

        logging.basicConfig(filename=ilogfile, level=logging.DEBUG)
        dimu = imuDaemon(pidfile=ipidfile)

        while(True):
        #create a dolder for the data

        #start recording
        dvid.start()
        dimu.start()