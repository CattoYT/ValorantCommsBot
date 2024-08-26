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

# TODO: Rename this file to ValorantAgentTracker.py for cleaner organisation. Don't ask why this is todo

import os
import time
from PIL import Image
from detectors import capture_screenshot
import numpy as np
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class HealthLabel:
    def __init__(self, parentWindow, initialValue=150, offset=0, initNow=True):
        self.parentWindow = parentWindow
        self.initialValue = initialValue
        self.offset = offset
        if initNow:
            self.label = QLabel(parentWindow)
            self.label.setText(str(initialValue))
            self.label.setStyleSheet(
                "font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
            self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.label.setGeometry(882 + (self.offset * 52), 69, 38, 18)

    def createLabel(self):
        self.label = QLabel(self.parentWindow)
        self.label.setText(str(self.initialValue))
        self.label.setStyleSheet("font-family: 'JetBrains Mono'; font-size: 14pt; font-style: italic; color: white; background-color: rgba(0, 0, 0, 0);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label.setGeometry(882 + (self.offset * 52), 69, 38, 18)

    def updateLabel(self, value):
        print("Desired value: " + value)
        self.label.setText(str(value))
        self.updateLabelPosition(value)

    def updateLabelPosition(self, currentPosition):
        print("Updating label position")
        self.offset = currentPosition
        self.label.setGeometry(882 + (int(currentPosition) * 52), 69, 38, 18) # apparently currentposition is a string?? TODO: look into this
        # TODO: The offsetting makes it disappear????

class Agent(object):
    def __init__(self, name, baseposition, side, health : int):
        self.originalName = name
        self.name = name
        self.baseposition = baseposition
        if side not in ["L", "R"]:
            self.side = "L"
        self.side = side
        self.currentPosition = baseposition  # If this = None, they are dead
        self.health = health

    #HEAVY BETA CODE PLEASE TOUCH WITH CAUTION
    def createLabel(self, parentWindow, initNow):
        self.healthLabel = HealthLabel(parentWindow, self.health, self.baseposition, initNow)

    def getLabel(self):
        return self.healthLabel # redundant but hey im used to java and it might be cleaner when i eventually forget

    def __str__(self):
        return f"{self.originalName} at position {self.currentPosition}"

    def Info(self):
        return f"{self.originalName} at position {self.currentPosition}"
    def json(self):
        return {
            "name": self.originalName,
            "originalName": self.originalName,
            "currentPosition": self.currentPosition,
            "baseposition": self.baseposition,
            "health": self.health,
            "side": self.side,

        }

    def setPosition(self, position):
        self.currentPosition = position
        try:
            self.label.healthLabel.updateLabelPosition(self.currentPosition)
        except AttributeError:
            print("Label not created yet.")
            # This is because the overlay hasnt properly been started, and can likely be ignored. COME BACK TO ME THOUGH

class ValorantAgentTracker:
    def __init__(self):
        # Dictionary of agents and their associated colors
        self.valorantAgents = {
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
        self.validAgentsL = []
        self.validAgentsR = []

        # initialize values
        L, R = self.getAllAgents()

        for i in L:

            self.validAgentsL.append(Agent(L[i], i, "L", 150))

        for i in R:
            self.validAgentsR.append(Agent(R[i], i, "R", 150))

    def getAgentObject(self, name, team="R"):
        if team == "L":
            validAgents = self.validAgentsL
        elif team == "R":
            validAgents = self.validAgentsR
        else:
            raise ValueError("Invalid team provided.")

        for agent in validAgents:
            if agent.name == name:
                return agent

        return

    def checkFiles(self):
        # Iterate through every image in the "Correct Agents" directory
        for file in os.listdir("debugging-images/ValorantUI/Correct Agents"):
            f = os.path.join("debugging-images/ValorantUI/Correct Agents", file)
            image = Image.open(f)
            image = image.convert('RGB')
            agent = self.valorantAgents[image.getpixel((20, 20))]
            print(agent)

    def getAgent(self, position, team="L", screenshot=None):
        # position is 1 indexed.
        if team == "L":
            offsetX = 380 + (int(position) * 66)
        elif team == "R":
            offsetX = 1104 + (int(position) * 66)  # DONT TOUCH THESE VALUES, THEY ARE PIXEL PERFECT

        if screenshot is None:
            screenshot = capture_screenshot()
        region_y = 30
        region_width = 40
        region_height = 40

        screenshot = screenshot.convert('RGB')
        centerPixelX, centerPixelY = int(region_width / 2), int(region_height / 2)

        try:
            agent = self.valorantAgents[screenshot.getpixel((offsetX + centerPixelX, region_y + centerPixelY))]
        except KeyError:
            agent = "Dead"

        return agent

    def getAllAgents(self, screenshot=None):
        positionsL = {i: "" for i in range(1, 6)}
        positionsR = {i: "" for i in range(1, 6)}

        for i in positionsL:  # had to do this because of the way the agents are offset
            positionsL[i] = self.getAgent(6 - i, team="L", screenshot=screenshot)  # don't question it
        for i in positionsR:
            positionsR[i] = self.getAgent(i, team="R", screenshot=screenshot)

        print(positionsL)
        print(positionsR)
        return positionsL, positionsR  # This returns from the center

    # not gonna lie, looking back, no fuckin clue how this works

    def reorganizeAgents(self, validAgents, updatedPositions):
        updated_agents = set(updatedPositions.values())  # Agents currently detected
        all_agents = {agent.name: agent for agent in validAgents if agent.currentPosition is not None}

        # Find the agent that is missing (i.e., dead)
        dead_agent = None
        for agent in validAgents:
            if agent.name not in updated_agents and agent.currentPosition is not None:
                dead_agent = agent
                break

        if dead_agent:
            dead_agent.health = 0
            dead_agent.setPosition(None)  # Mark the agent as dead
            validAgents.remove(dead_agent)
            validAgents.append(dead_agent)  # Move the dead agent to the end
            print(f"Agent {dead_agent.originalName} is dead and moved to the end.")

        # Update positions of remaining agents
        for i in updatedPositions:
            current_name = updatedPositions[i]
            if current_name == "Dead":
                continue  # Skip the "Dead" placeholder

            try:
                agent = all_agents[current_name]
                agent.setPosition(i)
                print(f"Agent {agent.originalName} moved to position {i}.")
            except KeyError:
                print(f"Agent {current_name} not found in active agents.")

    def updateAgentPositions(self):
        screenshot = capture_screenshot()
        L, R = self.getAllAgents(screenshot)
        self.reorganizeAgents(self.validAgentsL, L)
        self.reorganizeAgents(self.validAgentsR, R)

        for agent in self.validAgentsL:
            print(agent.Info())
        for agent in self.validAgentsR:
            print(agent.Info())

        time.sleep(5)


if __name__ == "__main__":
    tracker = ValorantAgentTracker()



    input("Press Enter to start monitoring...")

    while True:
        screenshot = capture_screenshot()
        L, R = tracker.getAllAgents(screenshot)
        tracker.reorganizeAgents(tracker.validAgentsL, L)
        tracker.reorganizeAgents(tracker.validAgentsR, R)

        for agent in tracker.validAgentsL:
            print(agent.Info())
        for agent in tracker.validAgentsR:
            print(agent.Info())

        time.sleep(5)

# Things to do in this file:
# Check which agents have died and move their object
# Check which agents have died and set their health to 0
# Account for revives (no i want to die)