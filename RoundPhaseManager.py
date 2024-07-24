import time

import pyautogui
from pytesseract import pytesseract

import detectors


class RPDetector:
    def __init__(self):
        self.currentPhase = "Buy"
        pass
    def checkRoundPhase(self):
        region_x = 1683 # might have to change all of these coords depending on if valorant changes the order of the credits overlay
        region_y = 1012
        region_width = 121
        region_height = 26

        sct_img = detectors.capture_screenshot()
        screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))

        text = pytesseract.image_to_string(screenshot, config=r'--psm 8')
        if "Round Loss" in text:
            self.currentPhase = "Loss"
        elif "Round Won" in text:
            self.currentPhase = "Win"
