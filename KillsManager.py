import random
import speaker as spk
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

    def monitorKills(self):
        while not self.stopEvent.is_set():
            killcount = detectors.getKills(me=False)
            print('killcount = ' + str(killcount))

            #for i in range(killcount):
            if killcount > 0: # temporary change because I want to eventually have a system to tell when the kills happened and be able to not say a voice line if it is too close together so im not spamming vc
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
