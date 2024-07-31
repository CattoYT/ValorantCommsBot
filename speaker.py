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

def play_audio(file_path):
    # see MultiprocessingIsAMistake.py for explanation
    try:
        requests.get("127.0.0.1:3000?scenario="+file_path)
    except:
        pass

# def play_audio(file_path, volume=0.9):
#
#
#     play_lock.acquire()
#     data, fs = sf.read(file_path, dtype='float32')
#
#     data = data * volume
#     #keyboard.press('v')
#     #sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C'))
#     sd.play(data, fs)
#     sd.wait()
#     time.sleep(0.1)
#     #keyboard.release('v')
#
#     play_lock.release()

def sayVoice(file_path):
    # Create a new thread to play the audio

    audio_thread = threading.Thread(target=play_audio, args=(file_path))
    audio_thread.start()

def getRandomVoiceLine(scenario, va):
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