import random
from Modules import speaker as spk
import detectors
from multiprocessing import Process, Event
import time

# Kill management

# this should be pushed into a different thread because it needs to run every 5 seconds. This is a fixed
# timer cuz valorant despawns its kill messages after 5 secs



class KillsManager:
    def __init__(self):

        self.stopEvent = Event()
        self.monitorProcess = None
        self.killcount = 0

    def monitorKills(self):
        while not self.stopEvent.is_set():
            self.killcount = detectors.getKills(me=True)



            #for i in range(killcount):
            if self.killcount > 0: # temporary change because I want to eventually have a system to tell when the kills happened and be able to not say a voice line if it is too close together so im not spamming vc
                #print('killcount = ' + str(self.killcount)) # this can stay commented for now since rng is guaranteed
                if random.randint(1, 10) > 0:
                    print('monitorKills - succeeded rng (guaranteed rn)')
                    spk.sayVoice(spk.getRandomFile('encouragement', 'mio'))
                else:
                    print('monitorKills - failed rng')
            time.sleep(5)



    def beginMonitoring(self):
        if self.monitorProcess is None or not self.monitorProcess.is_alive():
            self.monitorProcess = Process(target=self.monitorKills)
            self.monitorProcess.start()


    # thanks copilot for the events stuff
    def stopMonitoring(self):
        self.stopEvent.set()
        if self.monitorProcess is not None:
            self.monitorProcess.join()
