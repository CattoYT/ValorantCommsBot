import os
import subprocess
import sys

# Someone test this i dont want to lmao
def is_running_in_venv():

    python_executable = sys.executable
    venv_executable = os.path.join(sys.prefix, 'bin', 'python')

    return python_executable == venv_executable

if not is_running_in_venv():
    aa = input("You are not in a virtual environment. Are you sure you want to continue? (y/n).")
    if aa == "y":
        pass
    else:
        exit()


# Run pip install command
package_name = ["numpy", "cv2", "pyautogui", "PIL", "pytesseract", "soundfile", "sounddevice", "win32gui"]
for i in package_name:
    subprocess.run(["pip", "install", package_name])
subprocess.run(["git", "clone", "https://github.com/ultralytics/yolov5.git"])


try:
    import torch
except ImportError:
    thing = input("What version of pytorch u want to install? (cpu/cuda): ")
    if thing == "cpu":
        subprocess.run(["pip3", "install", "torch", "torchvision", "torchaudio"])
    elif thing == "cuda":
        subprocess.run(["pip3", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"])