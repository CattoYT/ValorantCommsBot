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



def readChat():
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
    # text = pytesseract.image_to_string(screenshot, config=r'--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789():<>?!&- "')
    #
    # data = []
    #
    # for line in text.splitlines():
    #     no = False
    #     if "(Party)" in line:
    #         line = line.replace("(Party) ", "")
    #         channel = "Party"
    #     elif "(All)" in line:
    #         line = line.replace("(All) ", "")
    #         channel = "All"
    #     elif "(Team)" in line:
    #         line = line.replace("(Team) ", "")
    #         channel = "Team"
    #     else:
    #         no = True
    #
    #     user = ""
    #     for char in line:
    #         if char == ":":
    #             line = line.replace(user, "")
    #             break
    #         else:
    #             user = user + char
    #     if not no:
    #
    #         data.append(ValorantChat(channel, user, line))
    #
    #
    #
    # return data


# since this file returns a pretty nice data struct, and it seems computationally heavy, it might be agood idea to rewrite this one in a differnet language
# I know that exposing rust to python is decently easy, so il research that
# so that was a fucking lie

import pydirectinput
import keyboard

import re

# This can be completely separate from the main modules, since they really don't need to interact often
# If they do, i can just refactor it later into a class cuz idrc
def ChatModule():
    lastMsg = ValorantChat("", "", "")

    from Overlay import startSetup
    startSetup()
    time.sleep(1)  # Add a slight delay to ensure the overlay is initialized
    from Overlay import worker  # Import after the setup is done
    from Managers.RoundPhaseManager import RPManager


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
    ChatModule()