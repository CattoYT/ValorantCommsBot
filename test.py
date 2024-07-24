import cv2
import numpy as np
from PIL import Image

import detectors

from ultralytics import YOLO
# - = enemy
# roboflow is an end to end = teammate
# exportd via roboflow = planted spike
# valorant = unplanted spike

model = YOLO("best (1).pt")
cv2.namedWindow("valorante", cv2.WINDOW_NORMAL)
while True:
    results = model(detectors.capture_screenshot())
    annotated_frame = results[0].plot()

    print(results)
    cv2.imshow("valorante", annotated_frame)
    cv2.waitKey(1)