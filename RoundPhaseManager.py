import re
import time
from multiprocessing import Process

import pyautogui
from PIL import Image
from pytesseract import pytesseract

import speaker as spk
import detectors

class RPManager:
    def __init__(self):
        self.currentPhase = "Buy"
        self.PhaseDetectionProcess = None




    def checkPhase(self):
        region_x = 807
        region_y = 161
        region_width = 315
        region_height = 83

        while True:
            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            text = pytesseract.image_to_string(screenshot, config=r'--psm 8 '
                                        r'-c tessedit_char_whitelist="1234567890:" ')
            if "BUY" in text:
                self.currentPhase = "Buy"
                return

            region_x = 924
            region_y = 29
            region_width = 72
            region_height = 37
            timerImg = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            timerImg = timerImg.resize((screenshot.width * 2, screenshot.height * 2), Image.BICUBIC).convert('L')
            timer = pytesseract.image_to_string(timerImg, config=r'--psm 8 '
                                        r'-c tessedit_char_whitelist="1234567890:"')

            pattern = re.compile(r'^\d:\d{2}$')
            print(timer)
            if pattern.match(timer):
                if timer[0] == "1":
                    self.currentPhase = "Combat"


    def beginPhaseDetection(self):
        if self.PhaseDetectionProcess is None or not self.PhaseDetectionProcess.is_alive():
            self.PhaseDetectionProcess = Process(target=self.checkPhase)
            self.PhaseDetectionProcess.daemon = True
            self.PhaseDetectionProcess.start()



if __name__ == '__main__':
    detector = RPManager()
    detector.beginPhaseDetection()

    while True:
        print(detector.currentPhase)
        time.sleep(0.5)