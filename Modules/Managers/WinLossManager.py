import time
from multiprocessing import Process, Value

from pytesseract import pytesseract
import speaker as spk
import detectors
from Modules.BaseLiveManager import BaseLiveManager


class WLManager(BaseLiveManager):
    def __init__(self):
        """
        Manager for checking if the last round was a win or loss.
        """
        super().__init__()
        self.liveProcess = self.monitorWinLoss
        self.previousRoundResultState = Value('i', 0)

    @property
    def previousRoundResult(self):
        """
        Returns the last round's result as a string
        :return: str
        """
        return {
            0: "Loss",
            1: "Win"

        }.get(self.previousRoundResultState.value, "Unknown")


    def monitorWinLoss(self):
        """
        Checks the phase using tesseract and the credits counter in the bottom right. This is a liveProcess so it cn be ignored
        :return:
        """
        # THIS DOES CHANGE
        region_x = 1637
        region_y = 856
        region_width = 160
        region_height = 180

        while not self.stopEvent.is_set():
            sct_img = detectors.capture_screenshot()
            screenshot = sct_img.crop((region_x, region_y, region_x + region_width, region_y + region_height))
            text = pytesseract.image_to_string(screenshot, config=r'--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "')

            if not text:
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
        """
        WIP Function that will read the score at the top of the screen and determine what the last round result was based on that.
        :return:
        """
        # This will be how i manage winning and losing in the future, where it watches for changes in the top score instead of looking at the changes in credits
        # It should be a lot more consistent
        # won't be worked on for a while tho since theres little need


        pass





if __name__ == "__main__":
    wl = WLManager()
    wl.beginWinLossDetection()
    while True:
        print(wl.previousRoundResult)
        time.sleep(3)