import soundfile as sf
import sounddevice as sd
import requests
import torch


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def get_file_duration(file_path):
    try:
        audio_info = sf.info(file_path)
        duration = audio_info.duration
        return duration
    except Exception as e:
        print("Error:", str(e))
        return None

def find_device_id(device_name):
    devices = sd.query_devices()
    for device in devices:
        if device['name'] == device_name:
            print(device['index'])
    return None

def isCudaAvailable():
    return torch.cuda.is_available()

def whatDevice():
    return torch.cuda.get_device_name(0)

print(isCudaAvailable())


def testColab():
    url = input("Give url: ")
    r = requests.post(f'{url}')