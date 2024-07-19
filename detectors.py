import re

import cv2
import numpy as np
import pyautogui

from PIL import Image
from pytesseract import pytesseract

from Modules import utils


def capture_screenshot():
    region = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    # screenshot = Image.open('testimage.png')

    return region


def read_text(image):
    #text = pytesseract.image_to_string(image) # test the below line tmr, genned by gpt
    text = pytesseract.image_to_string(image, config=r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789')
    print(text)
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
    region_height = 19  # Height of the region

    screenshot = screenshot.crop((region_x, region_y, region_x + region_width, region_y + region_height))

    screenshot.save("debugging-images/shieldtest.png")

    #for once, this doesn't change color constantly :D
    # static white so its just white pixels
    mask = cv2.inRange(np.array(screenshot), (220, 220, 220), (255, 255, 255))
    anti_alias_image = Image.fromarray(mask).resize((screenshot.width * 8, screenshot.height * 8), Image.BICUBIC)


    text = read_text(anti_alias_image)

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
def getKills(me=True): # me is cuz i sometimes use name hider lol
    region_x = 1244   # X-coordinate of the top-left corner of the region
    region_y = 0  # Y-coordinate of the top-left corner of the region
    region_width = 537 # Width of the region
    region_height = 1080 # Height of the region
    if me:

        matches = pyautogui.locateAllOnScreen('debugging-images/killname-me.png', confidence=0.8, region=(region_x, region_y, region_width, region_height))
    else:
        matches = pyautogui.locateAllOnScreen('debugging-images/killname.png', confidence=0.8, region=(region_x, region_y, region_width, region_height))
    killcount = 0
    if matches:
        for i in matches:
            killcount +=1
        return killcount


    else:
        return None


def getAlive():
    if pyautogui.locateOnScreen('debugging-images/COMBAT_REPORT2.png', confidence=0.7):
        return False
    else:
        return True


#oh nyo still being added
def roundDetector():
    print('checking for round loss')
    if pyautogui.locateOnScreen('debugging-images/roundloss.png', confidence=0.9):
        return 'loss'

def getWinLoss():
    if pyautogui.locateOnScreen('debugging-images/defeat.png', confidence=0.8):
        return False
    if pyautogui.locateOnScreen('debugging-images/victory.png', confidence=0.8):
        return True