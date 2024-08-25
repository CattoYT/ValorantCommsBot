'''
This is a legacy file!
For future me: You should PROBABLY recode this
Only 2 files are still used from before the recode, which is this and speaker.py
Now, future me, you have two options.
1. You can recode this file for ease of use
2. Ignore it
Take your pick.
'''


import re

import cv2
import numpy as np
import pyautogui

from PIL import Image
from pytesseract import pytesseract
from mss.windows import MSS as mss

from Modules import utils

sct = mss()

def capture_screenshot():
    region = sct.grab(sct.monitors[2])
    region = Image.frombytes('RGB', region.size, region.bgra, 'raw', 'BGRX')
    #region = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    # screenshot = Image.open('testimage.png')

    return region


def read_text(image):
    #text = pytesseract.image_to_string(image) # test the below line tmr, genned by gpt
    text = pytesseract.image_to_string(image, config=r'--psm 8 -c tessedit_char_whitelist=0123456789')
    return text


def getPlayerHealth(screenshot):

    #after about 2 hours of suffering, i have concluded that im just going to ahve both systems. if it fails both times, then oh well the player is prob dead
    # i would recommend this code to never be touched again, it works and i dont want to break it
    region_x = 574
    region_y = 1003
    region_width = 77
    region_height = 46

    screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))
    anti_alias_image = screenshot.resize((screenshot.width * 6, screenshot.height * 6), Image.BICUBIC)
    text = read_text(anti_alias_image)  # try pure white

    # copilot decided to try hsv and oh well i guess im going to use hsv now
    # half done by me, half copilot
    if text == "":

        imageHSV = cv2.cvtColor(np.array(anti_alias_image), cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(imageHSV, utils.rgb2HSV(255, 255, 255, "L"), utils.rgb2HSV(255, 255, 255, "U"))

        text = read_text(Image.fromarray(mask)) # try pure white

    if text == "":
        LBYellow, UBYellow = utils.rgb2HSV(235, 238, 177, "B", tolerance=0)

        mask = cv2.inRange(imageHSV, LBYellow, UBYellow)  # yellow healdwth
        text = read_text(Image.fromarray(mask))

    anti_alias_image.save("debugging-images/healthtest.png")


    text = re.sub(r'\D', '', text)
    return text



def getPlayerShield(screenshot):
    # Shield location
    region_x = 545  # X-coordinate of the top-left corner of the region
    region_y = 1018  # Y-coordinate of the top-left corner of the region
    region_width = 19  # Width of the region
    region_height = 19# Height of the region

    screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))



    #for once, this doesn't change color constantly :D
    # static white so its just white pixels
    mask = cv2.inRange(np.array(screenshot), (220, 220, 220), (255, 255, 255))
    anti_alias_image = Image.fromarray(mask).resize((screenshot.width * 6, screenshot.height * 6), Image.BICUBIC)

    anti_alias_image.save("debugging-images/shieldtest.png")
    text = read_text(anti_alias_image)
    text = re.sub(r'\D', '', text) # without this line, it somehow reads a newline from narnia and triggered my ocd so hard i spend 45 minutes trying to fix it
    return text

#scans coords with color (checks if any teammates are dead)
def getDeaths(screenshot):
    region_x = 1764    # X-coordinate of the top-left corner of the region
    killfeedYCoords = [96, 135, 174, 213, 252, 291]   #
    region_width = 72   # Width of the region
    region_height = 34   # Height of the region

    for ycoord in killfeedYCoords:
        killfeed = screenshot.crop((region_x, ycoord, region_x + region_width, ycoord + region_height))


        killfeed.save("debugging-images/killfeedtest.png")
        image = cv2.imread("debugging-images/killfeedtest.png")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        target_color = utils.hex_to_rgb('#66c3a9') # 102, 195, 169

        # Create a mask of pixels matching the target color
        mask = cv2.inRange(image_rgb, target_color, target_color)

        # Check if any pixels matching the target color are found
        if np.any(mask):
            return True
        else:
            return False
    return False


#checks for appearances of my name in the area where kills should be
def getKills(name="me"): # me is cuz i sometimes use name hider lol
    region_x = 1244   # X-coordinate of the top-left corner of the region
    region_y = 93  # Y-coordinate of the top-left corner of the region
    region_width = 537 # Width of the region
    region_height = 370 # Height of the region
    if name == "me":

        matches = pyautogui.locateAllOnScreen('debugging-images/killnames/Me.png', grayscale=True, confidence=0.8, region=(region_x, region_y, region_width, region_height))
    elif name == "iopi":
        matches = pyautogui.locateAllOnScreen('debugging-images/killnames/iopi.png', grayscale=True, confidence=0.8, region=(region_x, region_y, region_width, region_height))

    elif name == "Serene":
        # fun easter egg about this image, it was taken on Breeze T side spawn and the rock texture keeps messing up detections i think
        matches = pyautogui.locateAllOnScreen('debugging-images/killnames/Serene.png', grayscale=True,confidence=0.8, region=(region_x, region_y, region_width, region_height))
    else:
        # literally just for fun since i remembered a meme
        def yeet(exception):
            raise exception
        yeet(ValueError("Invalid name"))
    return len(list(matches))



def getAlive():
    #the images used here LITERALLY JUST GOT CHANGED IN THE LAST PATCH LMAO
    #The new image uses pyautogui instead of pytesseract cuz the position changes and i really don't care enough
    # This gets my alive from the combat report, might migrate to the switch player screen instead

    region_x = 1611   # X-coordinate of the top-left corner of the region
    region_y = 191  # Y-coordinate of the top-left corner of the region
    region_width = 204 # Width of the region
    region_height = 391 # Height of the region

    if pyautogui.locateOnScreen('debugging-images/CombatReport.png', confidence=0.6,
                region=(region_x, region_y, region_width, region_height)
                                ):
        return False
    else:
        return True


#oh nyo still being added


def getWinLoss():
    if pyautogui.locateOnScreen('debugging-images/defeat.png', confidence=0.8):
        return False
    if pyautogui.locateOnScreen('debugging-images/victory.png', confidence=0.8):
        return True


def checkEnemies():
    # probably going to try using template matching to see which image is most like the ones detected in each position. The first ones detected will be their proper position, since their position is offset when a teammate dies
    # When a teammate dies, iacan offset the corect position by the amount of teammates dead
    # images will be taken from https://github.com/deepsidh9/Live-Valorant-Overlay/tree/main/app/templates/agent_templates
    # this really should be done in a faster language i don't want to play valorant at 2 fps
    for i in range(5):


        pass