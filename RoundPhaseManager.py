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
        self.previousRoundResult = None
        self.PhaseDetectionProcess = None
        self.WinLossDetection = None
        pass

    # this function is not currently really in use tbh
    def monitorWinLoss(self):
        region_x = 1683 # might have to change all of these coords depending on if valorant changes the order of the credits overlay
        region_y = 1012
        region_width = 121
        region_height = 26

        while True:

            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))

            text = pytesseract.image_to_string(screenshot, config=r'--psm 8')
            if "Round Loss" in text:
                spk.sayVoice(spk.getRandomFile('new-round', 'mio'))
                self.previousRoundResult = "loss"
                time.sleep(50)# arbitrary number just guessing the average round length so that this doesn't spam and doesn't check this too often since its just not necessary
            elif "Round Won" in text:
                self.previousRoundResult = "Win"
                spk.sayVoice(spk.getRandomFile('new-round', 'mio'))
                time.sleep(50)





    def checkPhase(self):
        region_x = 807 # I keep copypasting these variables lmaoo
        region_y = 161
        region_width = 315
        region_height = 83 # Checks for BuyPhase in the overlay

        while True:

            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            text = pytesseract.image_to_string(screenshot, config=r'--psm 8 '      
                                        r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ') # genned from copilot since i was lazy
            if "BUY" in text:
                self.currentPhase = "Buy"
                return
            # Check the timer and determine combat based on it


            region_x = 924 # I keep copypasting these variables lmaoo
            region_y = 29
            region_width = 72
            region_height = 37
            timerImg = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            timerImg = timerImg.resize((screenshot.width * 2, screenshot.height * 2), Image.BICUBIC).convert('L')
            timer = pytesseract.image_to_string(timerImg, config=r'--psm 8 '      
                                        r'-c tessedit_char_whitelist="1234567890:"')


            # regex written by copilot for checking the timer format
            pattern = re.compile(r'^\d:\d{2}$')

            if pattern.match(timer):
                if timer[0] == "1":
                    self.currentPhase = "Combat"
                    return

        # for future me, implementing the end of round will take a long time.
        # you gotta account for ace, team ace, thrifty, etc
        # probably leave it out for now, but oh well



    def beginPhaseDetection(self):


        if self.PhaseDetectionProcess is None or not self.PhaseDetectionProcess.is_alive():
            self.PhaseDetectionProcess = Process(target=self.checkPhase)
            self.PhaseDetectionProcess.daemon = True
            self.PhaseDetectionProcess.start()
            return
        return
    def beginWinLossDetection(self):
        if self.WinLossDetection is None or not self.WinLossDetection.is_alive():
            self.WinLossDetection = Process(target=self.monitorWinLoss)
            self.WinLossDetection.daemon = True
            self.WinLossDetection.start()
            return
        return





if __name__ == '__main__':
    detector = RPManager()
    while True:
        detector.beginWinLossDetection()
        time.sleep(5)