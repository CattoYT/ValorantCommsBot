import threading
import time
from multiprocessing import Process


import detectors
from WinLossManager import WLManager

from detectors import getPlayerHealth, getPlayerShield

from HealthManager import HealthManager

from KillsManager import KillsManager

from EnemyManager import EnemyManager

from RoundPhaseManager import RPManager



# il eventually fix this cuz i really dont want to have a billion global vars xd
global frame
global isAlreadyLow
global isAlive
global isTeammateDead
global isAlreadyDead

# for deciding what goes in main loop, it should be anything that can run on a 5s cooldown. Anything outside of that probably should be in its own file with its own manager
#python is also way too slow for this lmao


# TODO: STOP COPYPASTING THE SCREENSHOT REGIONS INTO EVERY METHOD LMAOOOO

def main():
    HealthMgr = HealthManager()

    KillsMgr = KillsManager()
    KillsMgr.beginMonitoring()

    #EnemyMgr = EnemyManager(visualize=True)
    #EnemyMgr.beginEnemyDetection()

    #innit round phase detector
    #RPMgr = RPManager()
    #RPMgr.beginPhaseDetection()
    #innit win loss detection
    WLMgr = WLManager()
    WLMgr = WLMgr.beginWinLossDetection()


    while True:

        frame = detectors.capture_screenshot()
        HealthMgr.updateHP(getPlayerHealth(frame) or None)
        HealthMgr.updateShield(getPlayerShield(frame) or None)

        print("Health: " + str(HealthMgr.health))
        print("Shield: " + str(HealthMgr.shield))
        print("Kills: " + str(KillsMgr.killcount))
        #print("Phase: " + str(RPMgr.currentPhase))
        print("Last Round: " + str(WLMgr.previousRoundResult))

        #print("Enemies: " + str(EnemyMgr.enemyCount))
        print("")
        isAlive = detectors.getAlive()
        if HealthMgr.health and not isAlive:
            isAlive = True  # override because holy shit its not consistent
        HealthMgr.updateAlive(isAlive)




        time.sleep(1)





if __name__ == '__main__':
    main()
