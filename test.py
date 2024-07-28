import time

import cv2
import numpy as np
from PIL import Image
import speaker as spk
import detectors

from ultralytics import YOLO
# - = enemy
# roboflow is an end to end = teammate
# exportd via roboflow = planted spike
# valorant = unplanted spike

model = YOLO("Models/best.pt")
cooldown = 0
while True:
    results = model(detectors.capture_screenshot(), conf=0.60)

    detections = results[0].boxes
    class_ids = detections.cls.cpu().numpy() if detections.cls is not None else []  # thanks copilot
    detected = 0
    for class_id in class_ids:
        if class_id == 1.0:
            detected += 1



    if detected >= 1:
        print("Heeh")
        if time.time() - cooldown > 30: # 30 seconds
            cooldown = time.time()
            spk.sayVoice(r"D:\Coding\python\ValorantCommsBot\voices\mio\new-round\respawn - more_enemies_what_do_we_do.wav")