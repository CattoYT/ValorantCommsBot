import json

import pytesseract
import time

import requests

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
        return f"({self.channel}) {self.user}{self.line}"



def readChat():
    # This one runs on a 5 second delay, might be able to run it with KillsManager
    screenshot = detectors.capture_screenshot()
    region_x = 10  # X-coordinate of the top-left corner of the region
    region_y = 804  # Y-coordinate of the top-left corner of the region
    region_width = 436  # Width of the region
    region_height = 242  # Height of the region

    screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))

    text = pytesseract.image_to_string(screenshot, config=r'--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789():<>?!& "')

    data = []

    for line in text.splitlines():
        no = False
        if "(Party)" in line:
            line = line.replace("(Party) ", "")
            channel = "Party"
        elif "(All)" in line:
            line = line.replace("(All) ", "")
            channel = "All"
        elif "(Team)" in line:
            line = line.replace("(Team) ", "")
            channel = "Team"
        else:
            no = True

        user = ""
        for char in line:
            if char == ":":
                line = line.replace(user, "")
                break
            else:
                user = user + char
        if not no:

            data.append(ValorantChat(channel, user, line))



    return data


# since this file returns a pretty nice data struct, and it seems computationally heavy, it might be agood idea to rewrite this one in a differnet language
# I know that exposing rust to python is decently easy, so il research that

import pydirectinput

if __name__ == "__main__":
    lastMsg = ValorantChat("", "", "")
    while True:
        data = readChat()
        # Condition hell, not fixing it
        if not data:
            continue

        for i in data:
            print(f"{i.raw()}")

        if data[-1].raw() != lastMsg.raw():
            print(data[-1].user)

            if data[-1].user == "kaenia":
                continue

            response = requests.post("https://cheaply-caring-pup.ngrok-free.app/", json=data[-1].json())

            print(response.text)
            # untested, make sure my regular inputs are still processed
            pydirectinput.press('enter')
            pydirectinput.write(f"{response.text}")
            pydirectinput.press('enter')

            lastMsg = data[-1]
        else:
            print("No new messages")


        time.sleep(1)