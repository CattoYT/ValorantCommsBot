import random
import threading

import time
import speaker as spk
import detectors

from detectors import getAlive, getPlayerHealth, getPlayerShield


def main():
    global healthIsLow
    global isAlive
    global isTeammateDead

    healthIsLow = False
    isAlive = True
    isTeammateDead = False


    while True:
        time.sleep(5)
        print('\n')
        isAlive = getAlive()
        print('Alive: ' + str(isAlive))

        if isAlive == False:
            print('dead')
            spk.sayVoice(spk.getRandomFile('death', 'mio'))
        else:
            isAlive == True


        health = getPlayerHealth()
        shield = getPlayerShield()

        try:
            int(health)
        except ValueError:
            health = None
        try:
            int(shield)
        except ValueError:
            shield = None

        if health and isAlive:
            print("Health: " + str(health))

            if int(health) > 70:
                healthIsLow = False
                isAlive = True
                if healthIsLow == True:
                    healthIsLow = False
                    spk.sayVoice(spk.getRandomFile('health-recovered', 'mio'))
            if int(health) <= 70 and healthIsLow == False:
                healthIsLow = True
                print("Attempting to speak...")


                spk.sayVoice(spk.getRandomFile('low-hp', 'mio'))
        else:
            print("Failed to get health!")

        if shield:
            print("Shield: " + shield)
        else:
            print("Failed to get shield!")

        # TODO: put this in a new thread
        #if random.randint(1, 10) > 8:
        #    spk.sayVoice(spk.getRandomVoiceLine('encouragement', 'mio'))


def monitorKills():

    while True:
        print('\n')
        time.sleep(5)
        isTeammateDead = detectors.getDeaths()
        print('Dead Teammates: ' + str(isTeammateDead))


        killcount = detectors.getKills()
        print('killcount = ' + str(killcount))

        for i in range(killcount):
            if random.randint(1, 10) > 0:
                spk.sayVoice(spk.getRandomFile('encouragement', 'mio'))
            else:
                print('failed rng')
        killcount = 0



if __name__ == '__main__':
    # TODO: Fix this bullshit + make detection for null or >50 shield
    # TODO: do the funny with some video on this cuz theres a market for it
    # TODO: STOP MAKING IT PLAY WHEN IM IN CHARACTER SELECT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    threading.Thread(target=main).start()
    print('Started main bot!')
    threading.Thread(target=monitorKills).start()
    print('Started Teammate detector!')
