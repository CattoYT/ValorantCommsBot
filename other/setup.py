import os
import subprocess
import sys

yes = input("Do you want to install all the packages? (y/n): ")
if yes == "y":
    pass
else:
    sys.exit()

# Run pip install command


subprocess.run(["pip", "install", "-r", "requirements.txt"])


'''

-i https://download.pytorch.org/whl/nightly/cu121
torch==2.3.0.dev20240110+cu121
torchvision==0.18.0.dev20240110+cu121

'''
try:
    import torch
except ImportError:
    thing = input("What version of pytorch u want to install? (cpu/cuda): ")
    if thing == "cpu":
        subprocess.run(["pip3", "install", "torch", "torchvision", "torchaudio"])
    elif thing == "cuda":
        subprocess.run(["pip3", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/nightly/cu121"])
