import random
import speaker as spk
import detectors
from multiprocessing import Process, Event, Value
import time

from Modules.BaseLiveManager import BaseLiveManager


# Kill management

# this should be pushed into a different thread because it needs to run every 5 seconds. This is a fixed
# timer cuz valorant despawns its kill messages after 5 secs



class KillsManager(BaseLiveManager):
    def __init__(self):
        """
        A manager that monitors the player's kills and plays voice lines based on the kills
        This should be safe to be left alone.
        """
        super().__init__()
        self.killcountV = Value('i', 0) # I swear i keep forgetting to do this
        self.liveProcess = self.monitorKills


    @property
    def killcount(self):
        return self.killcountV.value

    def monitorKills(self):
        """
        This is the liveProcess for the KillsManager, should be safe to loop
        Makes use of detectors.getKills
        :return:
        """
        while not self.stopEvent.is_set():
            self.killcountV.value = detectors.getKills(me=True)



            #for i in range(killcount):
            if self.killcountV.value > 0: # temporary change because I want to eventually have a system to tell when the kills happened and be able to not say a voice line if it is too close together so im not spamming vc
                #print('killcount = ' + str(self.killcount)) # this can stay commented for now since rng is guaranteed
                if random.randint(1, 10) > 0:
                    #print('monitorKills - succeeded rng (guaranteed rn)')
                    spk.sayVoice(spk.getRandomFile('encouragement'))
                else:
                    pass
                    #print('monitorKills - failed rng')
            time.sleep(5)



if __name__ == "__main__":
    km = KillsManager()
    km.beginMonitoring()
    while True:
        print(km.killcount)
        time.sleep(5)
