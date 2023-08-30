import time
import win32gui
import win32con
import time
import cv2
import torch
from PIL import Image, ImageGrab
import numpy as np

model = torch.hub.load(R'yolov5-master', 'custom', path=R'valorant.pt', source='local', force_reload=True)

# Create OpenCV window if it doesn't exist



def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def findEnemy():
    global enemyCount
    starttime = time.time()
    active_window_title = get_active_window_title()
    if "VALORANT" in active_window_title:
        time.sleep(0.1)
        img = ImageGrab.grab()

        # Inference
        results = model(img)
        model.conf = 0.6
        foundshit = False
        # Convert PIL image to OpenCV format for drawing
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


        # Draw bounding boxes and labels
        for det in results.pred[0]:
            label = det[5]  # Class label
            conf = det[4]  # Confidence score
            bbox = det[:4]  # Bounding box coordinates


            if conf > model.conf:
                # Draw bounding box
                x_min, y_min, x_max, y_max = map(int, bbox)
                cv2.rectangle(img_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Draw label
                label_text = f"{model.names[int(label)]} {conf:.2f}"
                cv2.putText(img_cv, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                foundshit = True
                enemyCount = enemyCount + 1
                print(enemyCount)


        # Show the image with bounding boxes
        cv2.imshow("Detection", img_cv)
        cv2.waitKey(1)

        if foundshit:
            return True
        else:
            return False


def initializePlayerDetector():
    # Create OpenCV window if it doesn't exist
    if not cv2.getWindowProperty("Detection", cv2.WND_PROP_VISIBLE):
        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

    # Set the desired window size (width, height)
    window_width = 960
    window_height = 540
    cv2.resizeWindow("Detection", window_width, window_height)



initializePlayerDetector()
while True:
    findEnemy()


