import time
import types

import win32gui
import win32con
import time
import cv2
import torch
from PIL import Image, ImageGrab
import numpy as np

model = torch.hub.load(R'yolov5', 'custom', path=R'valorant.pt', source='local', force_reload=True)

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def findEnemy():
    global enemyCount
    enemyCount = 0
    active_window_title = get_active_window_title()

    time.sleep(0.1)
    if "VALORANT" in active_window_title:
        img = ImageGrab.grab()



    # Inference
    if isinstance (img, types.NoneType):
        return False

    results = model(img)
    model.conf = 0.6
    foundshit = False

    try:
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


        # Draw bounding boxes and labels, thanks chatgpt lol
        for det in results.pred[0]:
            label = det[5]  # Class label
            conf = det[4]  # Confidence score
            bbox = det[:4]  # Bounding box coordinates


            if conf > model.conf:

                x_min, y_min, x_max, y_max = map(int, bbox)
                cv2.rectangle(img_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)


                label_text = f"{model.names[int(label)]} {conf:.2f}"
                cv2.putText(img_cv, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                foundshit = True
                enemyCount = enemyCount + 1
                print(enemyCount)



        cv2.imshow("Detection", img_cv)
        cv2.waitKey(1)

        if foundshit:
            return True
        else:
            return False
    except UnboundLocalError:
        print("Not tabbed into VALORANT!")
        return False


def initializePlayerDetector():

    if not cv2.getWindowProperty("Detection", cv2.WND_PROP_VISIBLE):
        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

    window_width = 960
    window_height = 540
    cv2.resizeWindow("Detection", window_width, window_height)



initializePlayerDetector()
while True:
    findEnemy()


