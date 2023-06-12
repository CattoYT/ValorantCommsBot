import pyautogui
import pytesseract
from PIL import Image, ImageFilter
import time
import numpy as np
import speaker as spk
import re


def capture_screenshot(x, y, width, height):
    screenshot = pyautogui.screenshot()
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

    # Apply anti-aliasing using the `ANTIALIAS` filter
    anti_alias_image = screenshot.resize((screenshot.width * 8, screenshot.height * 8), Image.ANTIALIAS)

    text = read_text(anti_alias_image)

    return text


def main():
    while True:
        time.sleep(3)
        health = getPlayerHealth()
        shield = getPlayerShield()

        if health:
            print("Health: " + str(health))
            if int(health) < 70:
                print("Attempting to speak...")
                spk.sayVoice(spk.getVoiceLine(1, 'keqing'))

        else:
            print("Failed to get health!")

        if shield:
            print("Shield: " + shield)
        else:
            print("Failed to get shield!")


if __name__ == '__main__':
    # TODO: Fix this bullshit + make detection for null or >50 shield
    # TODO: add detection for death
    # TODO: do the funny with some video on this cuz theres a market for it
    # TODO: add mio's voice
    # TODO: optimize the voicelines code by probably returning
    #  a certain string and only changing the actual directory (that made no sense)

    main()
