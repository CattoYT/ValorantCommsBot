import time

import cv2
import numpy as np
import pyautogui
import threading
from PIL import Image
from pytesseract import pytesseract

import main
import speaker as spk
from detectors import capture_screenshot


import sounddevice as sd
import soundfile as sf

from utils import find_device_id


# Specify the name of the audio device to print


def getKills():
    region_x = 1244   # X-coordinate of the top-left corner of the region
    region_y = 0  # Y-coordinate of the top-left corner of the region
    region_width = 537 # Width of the region
    region_height = 1080 # Height of the region


    if pyautogui.locateOnScreen('debugging-images/killname.png', confidence=0.8, region=(region_x, region_y, region_width, region_height)):
        return True
    else:
        return False
data, fs = sf.read('voices/mio/victory/victory - nice_thats_how_you_pull_off_a_win.wav', dtype='float32')




sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C'))
sd.wait()  # Wait for the playback to finish