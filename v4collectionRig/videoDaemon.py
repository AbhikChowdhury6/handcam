import time

from daemons.prefab import run

class vidDaemon(run.RunDaemon):

    def run(self):

        while True:

            time.sleep(1)