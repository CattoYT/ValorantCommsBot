import time
from multiprocessing import Process, Value

from pytesseract import pytesseract
import speaker as spk
import detectors


class WLManager():
    def __init__(self):
        self.previousRoundResultState = Value('i', 0)
        self.WinLossDetection = None

    @property
    def previousRoundResult(self):
        return {
            0: "Loss",
            1: "Win"

        }.get(self.previousRoundResultState.value, "Unknown")


    def monitorWinLoss(self):
        # THIS DOES CHANGE
        region_x = 1637
        region_y = 856
        region_width = 160
        region_height = 180

        while True:
            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            text = pytesseract.image_to_string(screenshot, config=r'--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "')

            if text:
                screenshot.save("yes.png")
                print(text)
            else:
                #print("No text detected")
                time.sleep(6)
                continue

            if "Loss" in text:
                spk.sayVoice(spk.getRandomFile(['loss', 'new-round']))
                self.previousRoundResultState.value = 0
                time.sleep(50)
            elif "Win" in text:
                self.previousRoundResultState.value = 1
                spk.sayVoice(spk.getRandomFile(['victory', 'new-round']))
                time.sleep(50)

    def gameScoreMonitor(self):
        # This will be how i manage winning and losing in the future, where it watches for changes in the top score instead of looking at the changes in credits
        # It should be a lot more consistent
        # won't be worked on for a while tho since theres little need
        pass

    def beginWinLossDetection(self):
        if self.WinLossDetection is None or not self.WinLossDetection.is_alive():
            self.WinLossDetection = Process(target=self.monitorWinLoss)
            self.WinLossDetection.daemon = True
            self.WinLossDetection.start()



if __name__ == "__main__":
    wl = WLManager()
    wl.beginWinLossDetection()
    while True:
        print(wl.previousRoundResult)
        time.sleep(3)