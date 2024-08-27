import re
import time
from multiprocessing import Process, Value

import pyautogui
from PIL import Image
from pytesseract import pytesseract

import speaker as spk
import detectors
from Modules.BaseLiveManager import BaseLiveManager


class RPManager(BaseLiveManager):
    def __init__(self):
        """
        Monitors the round phase, and plays voice lines based on the phase

        """
        super().__init__()
        self.liveProcess = self.checkPhase
        self.currentPhaseState = Value('i', 0)

    @property
    def currentPhase(self): # written by copilot because damn i don't understand lambdas but eh cool
        """
        Returns the current phase as a string
        :return:
        """
        return {
            0: "Buy",
            1: "Combat"
        }.get(self.currentPhaseState.value, "Unknown")

    def checkPhase(self):
        """

        Checks the round phase if the buy phase text is at the top of the screen,
        and changes if the round timer has at least 1 min on the clock
        :return:
        """
        region_x = 807
        region_y = 161
        region_width = 315
        region_height = 83
        # This scans the top overlay for the buy phase text (The big one with Round and which side you're on)
        while not self.stopEvent.is_set():
            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            text = pytesseract.image_to_string(screenshot, config=r'--psm 7 '
                                        r'-c tessedit_char_whitelist="BUY PHASE" ')
            if "BUY" in text:
                self.currentPhaseState.value = 0
                continue


            timerImg = sct_img.crop((924, 29, 924 + 72, 29 + 37))
            timerImg = timerImg.resize((timerImg.width * 2, timerImg.height * 2), Image.BICUBIC).convert('L')
            timer = pytesseract.image_to_string(timerImg, config=r'--psm 7 '
                                        r'-c tessedit_char_whitelist="1234567890:"')

            pattern = re.compile(r'^\d:\d{2}$')
            if pattern.match(timer):
                if timer[0] == "1":
                    self.currentPhaseState.value = 1





if __name__ == '__main__':
    detector = RPManager()
    detector.beginDetection()
    while True:
        print(detector.currentPhase)
        time.sleep(1)
