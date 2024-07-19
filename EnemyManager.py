import time
from PIL import Image
import numpy as np
from mss.windows import MSS as mss

# TODO: Rewrite this file for yolov5 with tensorrt
class EnemyManger:
    def __init__(self):
        from ultralytics import YOLO
        self.model = YOLO("yolov8-valorant.pt")



    def findEnemy(self, image):
        self.model.track(image, show=True)

    def beginScreenRecording(self):

        import io
        with mss() as sct:
            # Monitor configuration for full screen capture
            monitor = sct.monitors[2]

            while True:
                # Capture the screen
                sct_img = sct.grab(monitor)

                # Convert to an array

                # Convert from BGRA to RGB


                # Pass the frame to the model for tracking

                results = self.model.predict(Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX'),
                                 conf=0.5,
                                 iou=0.5,
                                 device='cuda',
                                 show=True)

                print(results[0].boxes.cls) # TODO: fix this and print the amount of the 'enemy' label




enemyMGR = EnemyManger()
enemyMGR.beginScreenRecording()
