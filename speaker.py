import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard
import os
import random
import time


from Modules.utils import get_file_duration, find_device_id

play_lock = threading.Condition()
def play_audio(file_path, volume):


    play_lock.acquire()
    data, fs = sf.read(file_path, dtype='float32')

    #keyboard.press('v')
    sd.play(data, fs, device=find_device_id('CABLE Input (VB-Audio Virtual C'))
    #sd.play(data, fs)
    sd.wait()
    time.sleep(0.1)
    #keyboard.release('v')

    play_lock.release()

def sayVoice(file_path):
    # Create a new thread to play the audio

    audio_thread = threading.Thread(target=play_audio, args=(file_path, 0.4))
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

def getRandomFile(scenario, va):
    files = os.listdir(f'voices/{va}/{scenario}')
    if files:
        random_file = random.choice(files)
        file_path = os.path.join(f'voices/{va}/{scenario}/', random_file)
        #print(scenario, "|", file_path)
        return file_path


if __name__ == '__main__':
    sayVoice(getRandomFile('new-round', 'mio'))