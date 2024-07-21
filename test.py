import cv2
import numpy as np
from PIL import Image

import detectors

while True:
    img = detectors.capture_screenshot()

    img_np = np.array(img)
    height, width, _ = img_np.shape
    box_coords = (width - 70, 93, width - 30, 400)  # (x_min, y_min, x_max, y_max)

    # Set the specified area to black
    img_np[box_coords[1]:box_coords[3], box_coords[0]:box_coords[2]] = [0, 0, 0]
    img = Image.fromarray(img_np)

    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)



    cv2.imshow("Detection", img_cv)
    cv2.waitKey(1)