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
    alreadyDead = False

    while True:
        time.sleep(5)
        print('\n')
        isAlive = getAlive()
        print('Alive: ' + str(isAlive))


        if isAlive == False and alreadyDead == False:
            print('dead')
            alreadyDead = True
            spk.sayVoice(spk.getRandomFile('death', 'mio'))
        elif isAlive == True and alreadyDead == True:
            alreadyDead = False


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
        time.sleep(5)
        isTeammateDead = detectors.getDeaths()
        print('Dead Teammates: ' + str(isTeammateDead))


        killcount = detectors.getKills()
        print('killcount = ' + str(killcount))

        for i in range(killcount):
            if random.randint(1, 10) > 0:
                print('monitorKills - succeeded rng (guaranteed rn)')
                spk.sayVoice(spk.getRandomFile('encouragement', 'mio'))
            else:
                print('monitorKills - failed rng')
        killcount = 0
        if isTeammateDead:
            spk.sayVoice(spk.getRandomFile('teammate-death', 'mio'))
            print("Shit teammates")



if __name__ == '__main__':
    # TODO: Fix this bullshit + make detection for null or >50 shield
    # TODO: do the funny with some video on this cuz theres a market for it
    # TODO: make it use only one screenshot for all checks
    # TODO:



    threading.Thread(target=main).start()
    print('Started main bot!')
    threading.Thread(target=monitorKills).start()
    print('Started Teammate detector!')

    #CHECKLIST:

    # Teammate death detection - sometimes doesnt work if the killer name is too short
    # My death detection - Fine
    # Health - buggy, cant do shit about it
    # Shield - same
    # Alive status - perfect <3
    # my kills - seem fine?
    # round detector - NOT IMPLEMENTED


