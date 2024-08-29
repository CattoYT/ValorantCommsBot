import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
import os
import random
import time
import requests

from Modules.utils import get_file_duration, find_device_id

play_lock = threading.Condition() # this will work fine for 3.13, however, I can't use this rn because multiprocessing will dupilcate the lock :/

# def play_audio(file_path):
#     """
#     This is a function that SHOULD NOT EXIST BUT 3.13 ISNT HERE YET IS IT PLEASE RELEASE IT
#     It sends a get request to a localhost server (MultiprocessingIsAMistake.py) to play the audio file
#     This should be commented out when 3.13 is released
#     An internal function, wrapped from sayVoice.
#     :param file_path:
#     :return:
#     """
#
#     # see MultiprocessingIsAMistake.py for explanation
#     try:
#         requests.get("127.0.0.1:3000?scenario="+file_path)
#     except:
#         pass
#
def play_audio(file_path, volume=0.9):
    """
    The better version of play_audio, which uses threading to play sounds.
    An internal function, wrapped from sayVoice.
    :param file_path: relative of
    :param volume: double
    :return:
    """

    play_lock.acquire()
    data, fs = sf.read(file_path, dtype='float32')

    data = data * volume
    #keyboard.press('v')
    #sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C')) # uncomment me and change the device name to play into the mic
    sd.play(data, fs)
    sd.wait()
    time.sleep(0.1)
    #keyboard.release('v')

    play_lock.release()

def sayVoice(file_path):
    """
    The function that should be used to play audio files. It creates a new thread to play the audio.
    :param file_path: Generally, the output of getRandomFile
    :return:
    """
    # Create a new thread to play the audio

    print(file_path)
    threading.Thread(target=play_audio, args=(file_path,)).start()

def getRandomVoiceLine(scenario, va):
    """
    Deprecated, and I don't even remember why
    :param scenario:
    :param va:
    :return:
    """

    if va == 'mio':
        getRandomFile(scenario, va)
        '''
        match scenario:
            case 'encouragement':
                files = os.listdir('voices/mio/encouragement')
                if files:
                    random_file = random.choice(files)
                    file_path = os.path.join('voices/mio/encouragement', random_file)
                    return file_path
            case 'death':
                
                files = os.listdir('voices/mio/death')
                if files:
                    random_file = random.choice(files)
                    file_path = os.path.join('voices/mio/death', random_file)
                    return file_path
                
                
            case 'teammateDeath':
        '''


def getRandomFile(scenario):
    """
    This function is used to get a random voice line from the specified character.
    The specific directory structure should be used to ensure that the code works, outlined in voices/README.md

    :param scenario: Event as a string <death, encouragement, health-recovered, etc>. A list can also be passed.
    :return: os.path from content root.
    """

    va = 'mio' # Change me to the character!

    # fixed by copilot to account for lists for multiple voice line scenarios
    files = []

    if isinstance(scenario, list):
        for i in scenario:
            files.extend([os.path.join(f'voices/{va}/{i}', file) for file in os.listdir(f'voices/{va}/{i}')])
    elif isinstance(scenario, str):
        files = [os.path.join(f'voices/{va}/{scenario}', file) for file in os.listdir(f'voices/{va}/{scenario}')]

    if files:
        return random.choice(files)
    return None


if __name__ == '__main__':
    sayVoice(getRandomFile(['health-recovered', 'teammate-death']))