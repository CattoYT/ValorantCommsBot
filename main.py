import time
from multiprocessing import Process

from Modules.Managers.WinLossManager import WLManager

from detectors import getPlayerHealth, getPlayerShield

from Modules.Managers.HealthManager import HealthManager

from Modules.Managers.KillsManager import KillsManager

from Modules.Managers.RoundPhaseManager import RPManager



# il eventually fix this cuz i really dont want to have a billion global vars xd
global frame
global isAlreadyLow
global isAlive
global isTeammateDead
global isAlreadyDead

# for deciding what goes in main loop, it should be anything that can run on a 5s cooldown. Anything outside of that probably should be in its own file with its own manager
#python is also way too slow for this lmao


# TODO: STOP COPYPASTING THE SCREENSHOT REGIONS INTO EVERY METHOD LMAOOOO
# TODO: Refactor all the managers to use inheritance so that its a lot cleaner
# TODO: Reorganise the managers so that it is easier to start each one
# TODO: GUI (Low prio)
# TODO: Finish Yolo Implementation
# TODO: prevent double talking
# TODO: Improve performance in YOLO or make a colab server for it
#  (Server is here: https://colab.research.google.com/drive/1FFb7bS8LVFH1V9DwMC_x_ZFO6M9Z-8JN?authuser=4#scrollTo=UitBtdPf03sw) and in yolo_inference.ipynb

def main():
    HealthMgr = HealthManager()

    KillsMgr = KillsManager()
    KillsMgr.beginMonitoring()

    #EnemyMgr = EnemyManager(visualize=True)
    #EnemyMgr.beginYoloV8Detection()

    #innit round phase detector
    RPMgr = RPManager()
    RPMgr.beginDetection()
    # #innit win loss detection
    WLMgr = WLManager()
    WLMgr.beginWinLossDetection()


    while True:

        frame = detectors.capture_screenshot()
        # for these two lines, I have no idea if I want to separate them from the main thread or not.

        #the main advantage of doing this in the main thread is that the screenshot gets to be passed within here and doesnt get taken inside each of the managers
        HealthMgr.updateHP(getPlayerHealth(frame) or None)
        HealthMgr.updateShield(getPlayerShield(frame) or None)
        #
        print("Health: " + str(HealthMgr.health))
        print("Shield: " + str(HealthMgr.shield))
        print("Kills: " + str(KillsMgr.killcount)) #fixed
        print("Phase: " + str(RPMgr.currentPhase)) #working
        print("Last Round: " + str(WLMgr.previousRoundResult)) #working

        #print("Enemies: " + str(EnemyMgr.enemyCount)) # this line isn't really needed tbh
        print("")
        isAlive = detectors.getAlive()
        if HealthMgr.health and not isAlive:
            isAlive = True  # override because holy shit its not consistent
        HealthMgr.updateAlive(isAlive)




        time.sleep(1)





if __name__ == '__main__':
    from Modules import MultiprocessingIsAMistake
    import detectors

    Process(target=MultiprocessingIsAMistake.start).start()
    main()
