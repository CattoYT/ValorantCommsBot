import json

import pytesseract
import time
import io
import requests
import RustModules
import detectors


class ValorantChat:
    def __init__(self, channel, user, line):
        self.channel = channel
        self.user = user
        self.line = line

    def Empty(self):
        self.channel = ""
        self.user = ""
        self.line = ""

    def json(self):
        return json.dumps(
            {
                "channel": self.channel,
                "user": self.user,
                "line": self.line
            }
        )

    def raw(self):
        return f"({self.channel}) {self.user}: {self.line}"




import pydirectinput
import keyboard

import re

# This can be completely separate from the main modules, since they really don't need to interact often
# If they do, i can just refactor it later into a class cuz idrc

class ChatModule:
    def __init__(self, RoundPhaseManager=None, agentTracker=None):

        # for this init, PLEASE JUST PASS INSTANCES DO NOT LET THIS FILE MAKE THEM ITSELF BECAUSE I HAVE NO FUCKIN CLUE IF IT WORKS
        from qtOverlay import worker
        self.worker = worker

        if not RoundPhaseManager:
            from Modules.Managers.RoundPhaseManager import RPManager
            self.RPMgr = RPManager()
            self.RPMgr.beginDetection()
        else:
            self.RPMgr = RoundPhaseManager
        if not agentTracker:
            from Modules.OverlayModule.OverlayUtils import ValorantAgentTracker
            self.AgentTracker = ValorantAgentTracker()
        else:
            self.AgentTracker = agentTracker

        self.lastMsg = ValorantChat("", "", "")


    def readChat(self):
        # This one runs on a 5 second delay, might be able to run it with KillsManager
        screenshot = detectors.capture_screenshot()
        region_x = 10  # X-coordinate of the top-left corner of the region
        region_y = 804  # Y-coordinate of the top-left corner of the region
        region_width = 436  # Width of the region
        region_height = 242  # Height of the region

        screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))
        with io.BytesIO() as output:
            screenshot.save(output, format="PNG")
            data = RustModules.readChat(output.getvalue())
        return data



    # This is the main function for this class, where it reads the chat and sends the message to the server
    # It also runs the worker function.
    def updateChat(self):
        data = self.readChat()


        if not data:
            return None

        for i in data:
            print(f"{i.raw()}")

        if data[-1].raw() != self.lastMsg.raw():
            #print(data[-1].user)


            response = requests.post("https://cheaply-caring-pup.ngrok-free.app/", json=data[-1].json())

            print("LLM Response: " + response.text)
            # untested, make sure my regular inputs are still processed

            if "[HEALTHINDICATOR]" in response.text:
                # regex to extract the numbers in response.text
                # Find all numbers in the text
                numbers = re.findall(r'\d+', response.text)

                agent = re.search(r'(?<=\s).+?(?=\s)', response.text)

                if agent:
                    agent = agent.group(0)

                # This section may need a little work, since the chatmodule is separate now
                # START OF SHITTY SECTION

                agentObj = self.AgentTracker.getAgentObject(agent)
                agentObj.health = int(numbers[0])
                print(f"Updated {agentObj.originalName} health to {agentObj.health}")
                # END OF SHITTY SECTION


                if numbers:
                    print("Updating label... " + str(numbers[0]))
                    self.worker.update_label(agentObj.currentPosition, int(numbers[0]))  # Update the first label (index 0)
                    pass


            else:
                if "html" in response.text:
                    print("Server is down")
                    exit()

                # This can be integrated with RPManager to only act as a chatbot during buy phase
                if self.RPMgr.currentPhase == "Buy":
                    pass
                    # print("Typing Message...")
                    # pydirectinput.press('enter')
                    # keyboard.write(f"{response.text}")
                    # pydirectinput.press('enter')
            self.lastMsg = data[-1]
        else:
            print("No new messages")


def ChatModuleDeprecated():
    lastMsg = ValorantChat("", "", "")

    from qtOverlay import QTOverlay
    QTOverlay.startSetup()
    time.sleep(1)  # Add a slight delay to ensure the overlay is initialized
    from qtOverlay import worker  # Import after the setup is done
    from Modules.Managers.RoundPhaseManager import RPManager

    # for this, i should probably pass the original instance from the main class. for now, just making a new one.
    RPMgr = RPManager()
    RPMgr.beginDetection()
    while True:
        data = readChat()


        if not data:
            continue

        for i in data:
            print(f"{i.raw()}")

        if data[-1].raw() != lastMsg.raw():
            #print(data[-1].user)


            response = requests.post("https://cheaply-caring-pup.ngrok-free.app/", json=data[-1].json())

            print("LLM Response: " + response.text)
            # untested, make sure my regular inputs are still processed

            if "[HEALTHINDICATOR]" in response.text:
                # regex to extract the numbers in response.text
                # Find all numbers in the text
                numbers = re.findall(r'\d+', response.text)
                if numbers:
                    print("Updating label... " + str(numbers[0]))
                    worker.update_label(0, int(numbers[0]))  # Update the first label (index 0)
                    pass
            else:
                if "html" in response.text:
                    print("Server is down")
                    exit()

                # This can be integrated with RPManager to only act as a chatbot during buy phase
                if RPMgr.currentPhase == "Buy":
                    print("Typing Message...")
                    pydirectinput.press('enter')
                    keyboard.write(f"{response.text}")
                    pydirectinput.press('enter')
            lastMsg = data[-1]
        else:
            print("No new messages")


        time.sleep(4.5)
if __name__ == "__main__":
    chatObj = ChatModule()

    while True:
        chatObj.updateChat()
        time.sleep(5)
