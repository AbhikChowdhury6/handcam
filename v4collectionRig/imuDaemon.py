import time

from daemons.prefab import run

class imuDaemon(run.RunDaemon):

    def run(self):

        while True:
            #create folder for data
            time.sleep(1)