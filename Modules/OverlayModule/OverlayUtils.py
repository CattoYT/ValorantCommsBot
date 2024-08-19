# Each agent has a 40x40 area at the top of the screen.
# Player 1 on your team is at x=710 and y=30
# Player 2 is x=644
# P3 is x=578
# The offset for the left team from P1 is -66px
# Once the agent has been found, I can map that agent to the label and position.
# However, when a player dies, their model is shoved closer to the middle
# When this happens, i can run a scan again and move the labels accordingly
# I also don't need to research for each agent, i can just check for the ones found in the first place
# store them in a list or something ideally, maybe even a dict
import os
import time

from PIL import Image

# This is going to be offset from the first player on the right because it would just be easier lol
#
from detectors import capture_screenshot
import numpy as np


class Agent:
    def __init__(self, name, baseposition, health):
        self.name = name
        self.baseposition = baseposition
        self.currentPosition = baseposition # If this = 0, they are dead
        self.health = 150



    def __str__(self):
        return f"{self.name} at position {self.currentPosition}"

    def Info(self):
        return f"{self.name} at position {self.currentPosition}"

def checkFiles():
    valorantAgents = {
        # I did this manually. Im going to die :|
        (79, 61, 59): "Astra",
        (189, 154, 132): "Breach",
        (218, 169, 132): "Brimstone",
        (214, 195, 181): "Chamber",
        (190, 144, 135): "Clove",
        (20, 23, 33): "Cypher",
        (198, 146, 123): "Deadlock",
        (190, 145, 127): "Fade",
        (189, 134, 107): "Gekko",
        (119, 79, 68): "Harbor",
        (171, 131, 105): "Iso",
        (194, 138, 120): "Jett",
        (110, 126, 131): "KAY/O",
        (233, 213, 233): "Killjoy",
        (17, 18, 21): "Neon",
        (24, 255, 255): "Omen",
        (107, 73, 66): "Phoenix",
        (156, 112, 96): "Raze",
        (129, 85, 79): "Reyna",
        (66, 58, 58): "Sage",
        (183, 179, 157): "Skye",
        (201, 168, 160): "Sova",
        (101, 101, 95): "Viper",
        (8, 12, 24): "Yoru"
    }
    # iterate through every image in the "Correct Agents" directory

    for file in os.listdir("debugging-images/ValorantUI/Correct Agents"):
        f = os.path.join("debugging-images/ValorantUI/Correct Agents", file)

        image = Image.open(f)
        image = image.convert('RGB')
        agent = valorantAgents[image.getpixel((20,20))]
        print(agent)


def getAgent(position, team="L", screenshot=None): # position is 1 indexed.
    valorantAgents = {
        # I did this manually. Im going to die :|
        (79, 61, 59): "Astra",
        (189, 154, 132): "Breach",
        (218, 169, 132): "Brimstone",
        (214, 195, 181): "Chamber",
        (190, 144, 135): "Clove",
        (20, 23, 33): "Cypher",
        (198, 146, 123): "Deadlock",
        (190, 145, 127): "Fade",
        (189, 134, 107): "Gekko",
        (119, 79, 68): "Harbor",
        (171, 131, 105): "Iso",
        (194, 138, 120): "Jett",
        (110, 126, 131): "KAY/O",
        (233, 213, 233): "Killjoy",
        (17, 18, 21): "Neon",
        (24, 255, 255): "Omen",
        (107, 73, 66): "Phoenix",
        (156, 112, 96): "Raze",
        (129, 85, 79): "Reyna",
        (66, 58, 58): "Sage",
        (183, 179, 157): "Skye",
        (201, 168, 160): "Sova",
        (101, 101, 95): "Viper",
        (8, 12, 24): "Yoru"
    }
    if team == "L":

        offsetX = 380 + (int (position)*66)
    if team == "R":
        offsetX = 1104 + (int(position) * 66) # DONT TOUCH THESE VALUES, THEY ARE PIXEL PERFECT

    if not screenshot:
        screenshot = capture_screenshot()
    region_y = 30
    region_width = 40
    region_height = 40

    #screenshot = screenshot.crop((offsetX, region_y, offsetX + region_width, region_y + region_height))
    # center pixel of the cropped image
    screenshot = screenshot.convert('RGB')
    centerPixelX, centerPixelY = int(region_width / 2), int(region_height / 2)

    print(screenshot.getpixel((offsetX+centerPixelX, region_y+centerPixelY)))
    try:
        agent = valorantAgents[screenshot.getpixel((offsetX+centerPixelX, region_y+centerPixelY))]
        #print(agent)
    except KeyError:
        print("No agent")
        agent = "Dead"

    return agent

def getAllAgents(screenshot=None):
    positionsL = {
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",

    }
    positionsR = {
        1: "",
        2: "",
        3: "",
        4: "",
        5: "",

    }
    for i in positionsL:  # had to do this because of the way the agents are offset
        positionsL[i] = getAgent(6-i, team="L", screenshot=screenshot) # dont question it
    for i in positionsR:
        positionsR[i] = getAgent(i, team="R", screenshot=screenshot)
    return positionsL, positionsR # This returns from the center

# checkFiles()
if __name__ == "__main__":
    #This block here needs to be run in the buy phase ideally, since then everyone is alive
    #It also ensures that the base positions are correct
    validAgentsL = []
    validAgentsR = []
    L, R = getAllAgents()
    print(L)
    for i in L:
        validAgentsR.append(Agent(L[i], i, 150))

    print(R)
    for i in R:
        validAgentsR.append(Agent(R[i], i, 150))


    input()

    while True:
        screenshot = capture_screenshot()
        L, R = getAllAgents(screenshot)
        for i in L:
            if L[i] != validAgentsL[i - 1].name:
                #get the agent that changed
                agent = validAgentsL.pop(i - 1)

                if L[i] == "Dead":
                    agent.health = 0
                    agent.currentPosition = 0 # has to be set to 0 because i literally dont know any other way of maknig it seem that they are ead

                else:
                    agent.name = L[i]
                    agent.currentPosition = i

                # shove the agent back in
                validAgentsL.insert(i - 1, agent)
                print(f"Agent {i} has been moved to {L[i]} at position {i}")


        for agent in validAgentsL:
            print(agent.Info())
        # for i in R:
        #     if R[i] != validAgentsR[i - 1].name:
        #         #get the agent that changed
        #         agent = validAgentsR.pop(i - 1)
        #
        #         if R[i] == "Dead":
        #             agent.health = 0
        #             agent.currentPosition = 0 # has to be set to 0 because i literally dont know any other way of maknig it seem that they are ead
        #
        #         else:
        #             agent.name = R[i]
        #             agent.currentPosition = i
        #
        #         # shove the agent back in
        #         validAgentsR.insert(i - 1, agent)
        #         print(f"Agent {i} has been moved to {R[i]} at position {i}")
        #
        #
        # for agent in validAgentsR:
        #     print(agent.Info())

        time.sleep(5)




# Things to do in this file:
# Check which agents have died and move their object
# Check which agents have died and set their health to 0
# Account for revives (no i want to die)