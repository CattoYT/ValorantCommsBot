import cv2
import numpy as np
from mss.windows import MSS as mss
import win32gui
from PIL import Image
import torch

model = torch.hub.load(R'yolov5', 'custom', 'valorant-11.engine', source="local", force_reload=True)

def get_active_window_title():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def findEnemy(visualize=False):


    enemyCount = 0

    sct = mss()
    monitor = sct.monitors[2]
    sct_img = sct.grab(monitor)

    img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    model.conf = 0.5
    results = model(img)

    if visualize:
        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for det in results.pred[0]:
            label = det[5]  # Class label
            conf = det[4]  # Confidence score
            bbox = det[:4]  # Bounding box coordinates

            if conf > model.conf:
                x_min, y_min, x_max, y_max = map(int, bbox)
                cv2.rectangle(img_cv, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                label_text = f"{model.names[int(label)]} {conf:.2f}"
                cv2.putText(img_cv, label_text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                enemyCount += 1

        cv2.imshow("Detection", img_cv)
        cv2.waitKey(1)
    return enemyCount




def main_loop():
    while True:
        enemyCount = findEnemy()
        print(enemyCount)
        if cv2.waitKey(1) & 0xFF == ord('q') & cv2.getWindowProperty("Detection", cv2.WND_PROP_VISIBLE) == 0:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_loop()

    #still deprecated