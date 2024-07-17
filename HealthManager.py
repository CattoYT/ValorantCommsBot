from types import NoneType

import speaker as spk



class HealthManager:
    def __init__(self):
        self.health = 100
        self.shield = 0
        self.isAlreadyLow = False
        self.isAlreadyDead = False
        self.isAlive = True


    def updateHP(self, hp):

        if isinstance(hp, NoneType):
            hp = 0

        self.health = hp
        if self.isAlive == False:
            self.health = 0
        if int(self.health) < 50 and not self.isAlreadyLow and self.isAlive and int(self.health) != 0:
            print("HEALTH LOW")
            spk.sayVoice(spk.getRandomFile('low-hp', 'mio'))
            self.isAlreadyLow = True

        elif int(self.health) > 50:
            self.isAlreadyLow = False

        elif not self.health:
            print("MISSING HEALTH")


    def updateShield(self, shield):
        self.shield = shield
        if self.isAlive == False:
            self.shield = 0

    def updateAlive(self, alive):

        self.isAlive = alive

        if not self.isAlive:
            print("DEAD")
            if self.isAlreadyDead:
                return
            spk.sayVoice(spk.getRandomFile('death', 'mio'))
            self.isAlreadyDead = True
            pass
        else:
            self.isAlreadyDead = False