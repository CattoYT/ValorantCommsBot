import re

import cv2
import numpy as np
import pyautogui

from PIL import Image
from pytesseract import pytesseract

import utils



def capture_screenshot(x, y, width, height):

    screenshot = pyautogui.screenshot()
    # screenshot = Image.open('testimage.png')
    region = screenshot.crop((x, y, x + width, y + height))
    return region


def read_text(image):
    text = pytesseract.image_to_string(image)
    return text


def getPlayerHealth():
    # health location
    region_x = 574  # X-coordinate of the top-left corner of the region
    region_y = 1003  # Y-coordinate of the top-left corner of the region
    region_width = 77  # Width of the region
    region_height = 46  # Height of the region

    screenshot = capture_screenshot(region_x, region_y, region_width, region_height)
    screenshot.save("debugging-images/healthtest.png")
    anti_alias_image = screenshot.resize((screenshot.width * 6, screenshot.height * 6), Image.ANTIALIAS)

    text = read_text(anti_alias_image)

    text = re.sub(r'\D', '', text)
    return text


def getPlayerShield():
    # Shield location
    region_x = 545  # X-coordinate of the top-left corner of the region
    region_y = 1018  # Y-coordinate of the top-left corner of the region
    region_width = 19  # Width of the region
    region_height = 19  # Height of the region

    screenshot = capture_screenshot(region_x, region_y, region_width, region_height)
    screenshot.save("debugging-images/healthtest.png")
    # Apply anti-aliasing using the `ANTIALIAS` filter
    anti_alias_image = screenshot.resize((screenshot.width * 8, screenshot.height * 8), Image.ANTIALIAS)

    text = read_text(anti_alias_image)

    return text

#scans coords with color
def getDeaths():
    region_x = 1764    # X-coordinate of the top-left corner of the region
    killfeedYCoords = [96, 135, 174, 213, 252, 291]   #
    region_width = 72   # Width of the region
    region_height = 34   # Height of the region
    target_color = (102, 195, 169)  # RGB value of the target color

    for ycoord in killfeedYCoords:
        killfeed = capture_screenshot(region_x, ycoord, region_width, region_height)
        killfeed.save("debugging-images/killfeedtest.png")
        image = cv2.imread("debugging-images/killfeedtest.png")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        target_color = utils.hex_to_rgb('#66c3a9')

        # Create a mask of pixels matching the target color
        mask = cv2.inRange(image_rgb, target_color, target_color)

        # Check if any pixels matching the target color are found
        if np.any(mask):
            #print coords of the pixel
            print(region_x, ycoord)
            return True
        else:
            return False
    return False


#checks for appearances of my name in the area where kills should be
def getKills():
    region_x = 1244   # X-coordinate of the top-left corner of the region
    region_y = 0  # Y-coordinate of the top-left corner of the region
    region_width = 537 # Width of the region
    region_height = 1080 # Height of the region

    matches = pyautogui.locateAllOnScreen('debugging-images/killname-me.png', confidence=0.9, region=(region_x, region_y, region_width, region_height))
    killcount = 0
    if matches:
        for i in matches:
            killcount +=1
        return killcount


    else:
        return None


def getAlive():
    if pyautogui.locateOnScreen('COMBAT_REPORT2.png', confidence=0.9):

        return False
    else:
        return True

    #oh nyo
def roundDetector():
    print('checking for round loss')
    if pyautogui.locateOnScreen('test.png', confidence=0.9):
        return 'loss'
    