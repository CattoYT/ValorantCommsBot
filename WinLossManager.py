import time
from multiprocessing import Process

from pytesseract import pytesseract
import speaker as spk
import detectors


class WLManager():
    def __init__(self):
        self.previousRoundResult = "none"
        self.WinLossDetection = None




    def monitorWinLoss(self):
        # THIS DOES CHANGE
        region_x = 1683
        region_y = 1012
        region_width = 121
        region_height = 26

        while True:
            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))

            text = pytesseract.image_to_string(screenshot, config=r'--psm 8')
            print(text)
            if "Round Loss" in text:
                spk.sayVoice(spk.getRandomFile(['loss', 'new-round']))
                self.previousRoundResult = "loss"
                time.sleep(50)
            elif "Round Win" in text:
                self.previousRoundResult = "Win"
                spk.sayVoice(spk.getRandomFile(['victory', 'new-round']))
                time.sleep(50)

    def beginWinLossDetection(self):
        if self.WinLossDetection is None or not self.WinLossDetection.is_alive():
            self.WinLossDetection = Process(target=self.monitorWinLoss)
            self.WinLossDetection.daemon = True
            self.WinLossDetection.start()