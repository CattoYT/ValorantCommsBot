from types import NoneType

import speaker as spk


class HealthManager:
    def __init__(self):
        """
        Manager for the health of the player. Only one should exist, cuz what else is it used for lol
        """
        self.health = 100
        self.shield = 0
        self.isAlreadyLow = False
        self.isAlreadyDead = False
        self.isAlive = True


    def updateHP(self, hp):
        """
        Updates the health and plays a voice line depending on the update
        :param hp: int
        :return: None
        """
        if isinstance(hp, NoneType):
            hp = 0

        self.health = hp
        if self.isAlive == False:
            self.health = 0
        if int(self.health) < 50 and not self.isAlreadyLow and self.isAlive and int(self.health) != 0:
            print("HEALTH LOW")
            spk.sayVoice(spk.getRandomFile('low-hp'))
            self.isAlreadyLow = True

        elif int(self.health) > 50:
            self.isAlreadyLow = False



    def updateShield(self, shield):
        """
        Updates the shield value, does nothing else rn
        :param shield:
        :return:
        """
        if isinstance(shield, NoneType):
            shield = 0
        self.shield = shield

        if self.isAlive == False:
            self.shield = 0



    def updateAlive(self, alive):
        """
        Updates the alive status of the player
        This will also play voice lines if the player is dead
        :param alive:
        :return:
        """
        self.isAlive = alive

        if not self.isAlive:
            print("DEAD")
            if self.isAlreadyDead:
                return
            spk.sayVoice(spk.getRandomFile('death'))
            self.isAlreadyDead = True
            pass
        else:
            self.isAlreadyDead = False