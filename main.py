import time
from multiprocessing import Process

import detectors

from detectors import getPlayerHealth, getPlayerShield

from HealthManager import HealthManager

from KillsManager import KillsManager


# il eventually fix this cuz i really dont want to have a billion global vars xd
global frame
global isAlreadyLow
global isAlive
global isTeammateDead
global isAlreadyDead


def main():
    HealthMgr = HealthManager()

    while True:

        frame = detectors.capture_screenshot()

        HealthMgr.updateHP(getPlayerHealth(frame) or None)
        HealthMgr.updateShield(getPlayerShield(frame) or None)

        print("Health: " + str(HealthMgr.health))
        print("Shield: " + str(HealthMgr.shield))

        isAlive = detectors.getAlive()
        if HealthMgr.health and not isAlive:
            isAlive = True  # override because holy shit its not consistent

        HealthMgr.updateAlive(isAlive)

        print("\n")
        time.sleep(1)





if __name__ == '__main__':
    KillsMgr = KillsManager()
    KillsMgr.beginMonitoring()
    main()
