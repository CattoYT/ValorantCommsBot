
import time

import detectors

from detectors import getPlayerHealth, getPlayerShield
import speaker as spk

global frame
global healthIsLow
global isAlive
global isTeammateDead


while True:

    frame = detectors.capture_screenshot()
    print('\n')
    health = getPlayerHealth(frame)
    shield = getPlayerShield(frame)
    print("Health: " + str(health))
    print("Shield: " + str(shield))
    print("")
    time.sleep(5)

    isAlive = detectors.getAlive()
    if not isAlive:
        print("DEAD")
        spk.sayVoice(spk.getRandomFile('death', 'mio'))
        # go to next iteration
        continue
    print("ALIVE")
    if health < 50:
        print("HEALTH LOW")
        spk.sayVoice(spk.getRandomFile('health-low', 'mio'))
        continue
    time.sleep(5)