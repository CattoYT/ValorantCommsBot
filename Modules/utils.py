import time

import cv2
import numpy as np
import soundfile as sf
import sounddevice as sd
import requests
#import torch


def hex_to_rgb(hex_color):
    """
    Converts a hex color to an RGB tuple.
    :param hex_color: #xxxxxx
    :return:
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# copilot thanks
def rgb2HSV(r, g, b, bound, tolerance=0):
    """
    Convert an RGB color to HSV with a specified tolerance.

    :param r: Red component of the color (0-255)
    :param g: Green component of the color (0-255)
    :param b: Blue component of the color (0-255)
    :bound: Which bound u need
    :param tolerance: Tolerance value for color conversion
    ce
    """

    lower_bound_rgb = [r - tolerance, g - tolerance, b - tolerance]
    upper_bound_rgb = [r + tolerance, g + tolerance, b + tolerance]


    lower_bound_hsv = cv2.cvtColor(np.uint8([[lower_bound_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    upper_bound_hsv = cv2.cvtColor(np.uint8([[upper_bound_rgb]]), cv2.COLOR_RGB2HSV)[0][0]

    match bound:
        case "U":
            return upper_bound_hsv
        case "L":
            return lower_bound_hsv

        case "B":
            return lower_bound_hsv, upper_bound_hsv
        case _:
            return lower_bound_hsv, upper_bound_hsv




def get_file_duration(file_path):
    """
    Returns the length of the file in seconds?
    :param file_path:
    :return: int? (I literally dont remembeer
    """
    try:
        audio_info = sf.info(file_path)
        duration = audio_info.duration
        return duration
    except Exception as e:
        print("Error:", str(e))
        return None

def find_device_id(device_name):
    """
    Prints out audio device ids
    For some reason, sounddevice truncates some values, so copium and use the lowest number that makes sense for your device
    :param device_name:
    :return:
    """
    devices = sd.query_devices()
    for device in devices:
        if device['name'] == device_name:
            print(device['index'])
    return None

#not documenting these they are self explanatory
def isCudaAvailable():
    return torch.cuda.is_available()

def whatDevice():
    return torch.cuda.get_device_name(0)


def showImage(image):
    """
    Creates a cv2 window of an image, and closes after "=" is pressed
    :param image:
    :return:
    """
    while True:

        img = cv2.imread(image)

        cv2.imshow("Updated Image", img)

        if cv2.waitKey(1) & 0xFF == ord('='):
            break
        time.sleep(1)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    showImage('debugging-images/healthtest.png')